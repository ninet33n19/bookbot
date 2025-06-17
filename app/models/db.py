from app import db
from sqlalchemy.dialects.postgresql import JSON

class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.String, primary_key=True)
    filename = db.Column(db.String, nullable=False)
    path = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    result = db.Column(JSON)
