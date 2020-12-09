from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, login

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    content = db.Column(db.String(10000), index=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    forumID = db.Column(db.Integer, db.ForeignKey('forum.id'))
    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String(10000), index=True, unique=True)
    postID = db.Column(db.Integer, db.ForeignKey('post.id'))
    def __repr__(self):
        return '<Reply {}>'.format(self.body)

class Forum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_title = db.Column(db.String(140), index=True)
    author = db.Column(db.String(140), index=True)
    posts = db.relationship("Post", backref="forum", lazy="dynamic")
    def __repr__(self):
        return '<Forum {}>'.format(self.body)

class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(64), index=True, unique=True)
        password_hash = db.Column(db.String(128), index=True)
        forums = db.relationship("Forum", backref="user", lazy="dynamic")
        posts = db.relationship("Post", backref="user", lazy="dynamic")
        def __repr__(self):
            return '<User {}>'.format(self.name)
        def set_password(self, password):
            self.password_hash = generate_password_hash(password)
        def check_password(self, password):
            return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))