from datetime import datetime
from typing import Any

from src.config import settings
from src.dto.api.task import TaskDTO
from src.dto.events.task import TaskCreatedEventDTO, TaskEventDTO, TaskNewAssigneeDTO, \
    TaskCompletedEventDTO, TaskStatusChangedDataDTO, TaskAssignedEventDTO
from src.enums.status import TaskStatus
from src.kafka.producer import EventsProducer
from src.models.task import Task
from src.repositories.task import TaskRepository
from src.repositories.user import UserRepository
from src.services.exceptions import TaskNotFound, WrongTaskStatus


class TaskService:
    def __init__(
            self,
            task_repo: TaskRepository,
            user_repo: UserRepository,
            producer: EventsProducer,
    ):
        self.task_repo = task_repo
        self.user_repo = user_repo
        self.producer = producer

    def get_task(self, task_id: int) -> TaskDTO:
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise TaskNotFound(f"Task {task_id} not found")

        task_dto = TaskDTO.from_orm(task)
        return task_dto

    def add_task(self, data: dict[str, Any]) -> TaskDTO:
        dto = TaskDTO.model_validate(data)
        task = self.task_repo.create_task(dto)
        old_assignee_public_id = task.assignee.public_id

        user, *_ = self.user_repo.get_random_employees(lock=True)
        self.task_repo.assign_to_user(user_id=user.id, task=task)
        data_event = TaskCreatedEventDTO(
            data=TaskEventDTO.from_orm(task),
            produced_at=datetime.utcnow(),
        )
        self.producer.send(value=data_event.model_dump_json(), topic=settings.data_streaming_topic)

        business_event = TaskAssignedEventDTO(
            data=TaskNewAssigneeDTO(
                public_id=task.public_id,
                old_assignee_public_id=old_assignee_public_id,
                new_assignee_public_id=user.public_id,
            ),
            produced_at=datetime.utcnow(),
        )
        self.producer.send(value=business_event.model_dump_json(), topic=settings.business_event_topic)
        return TaskDTO.from_orm(task)

    def complete_task(self, task_id: int) -> TaskDTO:
        task = self.task_repo.get_by_id(task_id, lock=True, of=Task)
        if not task:
            raise TaskNotFound(f"Task {task_id} not found")

        old_status = task.status
        self.task_repo.status_done(task=task)

        business_event = TaskCompletedEventDTO(
            data=TaskStatusChangedDataDTO(
                public_id=task.public_id,
                assignee_public_id=task.assignee.public_id,
                old_status=old_status,
                new_status=task.status,
            ),
            produced_at=datetime.utcnow(),
        )
        broker.publish(message=business_event.model_dump(mode="json"), topic=settings.business_event_topic)
        task_dto = TaskDTO.from_orm(task)
        return task_dto

    def assign_task(self, task_id: int) -> TaskDTO:
        task = self.task_repo.get_by_id(task_id, lock=True, of=Task)
        if not task:
            raise TaskNotFound(f"Task {task_id} not found")

        if task.status != TaskStatus.OPEN:
            raise WrongTaskStatus(
                f"Task {task_id} has wrong status {task.status}"
            )

        old_assignee_public_id = task.assignee.public_id
        user, *_ = self.user_repo.get_random_employees(lock=True)
        self.task_repo.assign_to_user(user_id=user.id, task=task)

        business_event = TaskAssignedEventDTO(
            data=TaskNewAssigneeDTO(
                public_id=task.public_id,
                old_assignee_public_id=old_assignee_public_id,
                new_assignee_public_id=user.public_id,
            ),
            produced_at=datetime.utcnow(),
        )
        broker.publish(message=business_event.model_dump(mode="json"), topic=settings.business_event_topic)
        return TaskDTO.from_orm(task)

    def reshuffle(self) -> list[int]:
        tasks = self.task_repo.get_all_opened()
        task_ids = [task.id for task in tasks]

        for task_id in task_ids:
            self.assign_task(task_id=task_id)
        return task_ids
