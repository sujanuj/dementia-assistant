from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    
    # Uses DATABASE_URL from environment (Railway sets this automatically)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 
        'postgresql://localhost/ai_memory'  # fallback for local dev
    )
    
    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    return app
