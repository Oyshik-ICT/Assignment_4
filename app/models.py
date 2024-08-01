from app import db
from datetime import datetime,timezone
from enum import Enum

class UserRole(Enum):
    ADMIN = 'Admin'
    USER = 'User'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.USER, nullable=False)
    create_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    update_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<User {self.username}>'