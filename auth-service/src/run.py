from flask import Flask

from src.config import settings
from src.database import db

if __name__ == "__main__":
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.sqlalchemy_database_uri
    db.init_app(app)
    app.run(host=settings.api_host, port=settings.api_port)
