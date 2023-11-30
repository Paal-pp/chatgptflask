from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db =SQLAlchemy()


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    last_login = db.Column(db.TIMESTAMP)

    # 与 ChatRecord 的关系
    chat_records = db.relationship('ChatRecord', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class ChatRecord(db.Model):
    __tablename__ = 'chat_records'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text)
    response = db.Column(db.Text)
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    session_id = db.Column(db.String(255))

    def __repr__(self):
        return f'<ChatRecord {self.id} by User {self.user_id}>'


