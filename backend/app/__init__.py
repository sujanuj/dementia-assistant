from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost/ai_memory"
    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    return app