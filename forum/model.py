#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/11/14 下午3:32 
# @Author : Gaoxiang Chen
# @Site :  
# @File : model.py 
# @Software: PyCharm
# ---------------------


from datetime import datetime
from flask._compat import text_type
from flask_login import UserMixin
from forum import login_manager, db


@login_manager.user_loader
def load_user(user_id):
    return User.getUserById(user_id)



###USER
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    _password = db.Column(db.String(20))
    _email = db.Column(db.String(20), unique=True)
    posts = db.relationship("Post", backref="user")
    comments = db.relationship("Comment", backref="user")
    likes = db.relationship("Like", backref="user")

    def __init__(self, username, _password, _email):
        self.username = username
        self._password = _password
        self._email = _email

    @classmethod
    def all_users(self):
        return self.query.all()

    @classmethod
    def getUserById(self, uid):
        return self.query.get(uid)

    @classmethod
    def getEmail(self):
        return self._email

    def get_id(self):
        try:
            return text_type(self.uid)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')



###POST
class Post(db.Model):
    __tablename__ = 'posts'
    pid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    post_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    tid = db.Column(db.Integer, db.ForeignKey('topics.tid'), nullable=False)
    comments = db.relationship("Comment", backref="posts")
    likes = db.relationship("Like", backref="posts")


    def __init__(self, title, content, post_time, uid, tid):
        self.title = title
        self.content = content
        self.post_time = post_time
        self.uid = uid
        self.tid = tid



###Topic
class Topic(db.Model):
    __tablename__ = 'topics'
    tid = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(20))
    _description = db.Column(db.String(20))
    parent_id = db.Column(db.String(20))
    posts = db.relationship("Post", backref="topics")
    path = None

    def __init__(self, topic, _description, parent_id):
        self.topic = topic
        self._description = _description
        self.parent_id = parent_id

    @classmethod
    def all_topics(self):
        return self.query.all()

    @classmethod
    def getTopicById(self, tid):
        return self.query.get(tid)

    @classmethod
    def getTopicList(self):
        return [{t.topic} for t in Topic.all_topics()]


###Comments
class Comment(db.Model):
    __tablename__ = 'comments'
    cid = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    pid = db.Column(db.Integer, db.ForeignKey('posts.pid'), nullable=False)
    father_id = db.Column(db.Integer, db.ForeignKey('comments.cid'), nullable=True)

    def __init__(self, content, post_time, pid):
        self.content = content
        self.post_time = post_time
        self.pid = pid

    def get_id(self):
        try:
            return text_type(self.cid)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')


###Like
class Like(db.Model):
    __tablename__ = 'likes'
    lid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    pid = db.Column(db.Integer, db.ForeignKey('posts.pid'), nullable=False)
    post_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, uid, pid, post_time):
        self.uid = uid
        self.pid = pid
        self.post_time = post_time



