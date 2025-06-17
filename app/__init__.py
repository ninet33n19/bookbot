from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    from app.core.config import Config

    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from app.routes import upload, jobs
    app.register_blueprint(upload.bp)
    app.register_blueprint(jobs.bp)

    return app
