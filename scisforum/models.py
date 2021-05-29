from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from scisforum import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    face_access = db.Column(db.Boolean, nullable=True, default=False)
    encoding_file = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(60), nullable=False)
    access = db.Column(db.Boolean, nullable=False, default=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.access}')"


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


class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    start_time = db.Column(db.DateTime, nullable = False)
    end_time = db.Column(db.DateTime, nullable = False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    
    def __repr__(self):
        return f"Event('{self.title}', ' {self.creator_id}')"