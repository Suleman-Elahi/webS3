from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), nullable=False)  # S3 object key
    size = db.Column(db.Integer, nullable=False)     # File size in bytes
    file_type = db.Column(db.String(50), nullable=False)  # File type (e.g., image, video)
    url = db.Column(db.String(255), nullable=False)  # Public URL to the file

    def __init__(self, key, size, file_type, url):
        self.key = key
        self.size = size
        self.file_type = file_type
        self.url = url

    def __repr__(self):
        return f'<File {self.key}>'