from datetime import datetime
from scisforum import db, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import relationship


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    msg_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    msg_to_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    msg_time = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    msg_by = relationship("User", foreign_keys=[msg_by_id])
    msg_to = relationship("User", foreign_keys=[msg_to_id])

    def __repr__(self):
        return f"Message('{self.msg_by_id}', ' {self.msg_to_id}', ' {self.msg_time} ')"