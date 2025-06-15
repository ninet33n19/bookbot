from app import db

class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.String, primary_key=True)
    filename = db.Column(db.String, nullable=False)
    path = db.Column(db.String, nullable=False)
