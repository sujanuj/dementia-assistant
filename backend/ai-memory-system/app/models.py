from app import db
from pgvector.sqlalchemy import Vector

class Memory(db.Model):
    __tablename__ = "conversation_memory"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String)
    message = db.Column(db.Text)
    embedding = db.Column(Vector(1536))