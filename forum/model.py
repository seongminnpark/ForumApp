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
# from forum import login_manager, db
from forum import db


# @login_manager.user_loader
# def load_user(user_id):
#     return User.getUserById(user_id)



###USER
class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20))
    password_hash = db.Column(db.String(20))
    token = db.Column(db.String(20))
    isAdmin = db.Column(db.Integer)

    def __init__(self, email, password_hash, token, isAdmin):
        self.email = email
        self.password_hash = password_hash
        self.token = token
        self.isAdmin = isAdmin

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

# ###UserRole
# class UserRole(db.Model):
#     __tablename__ = 'user_role'
#     role_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20))

#     def __init__(self, role_id, name):
#         self.role_id = role_id
#         self.name = name

# ###UserIsRole
# class UserIsRole(db.Model):
#     __tablename__ = 'user_is_role'
#     user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
#     role_id = db.Column(db.Integer, db.ForeignKey('user_role.role_id'))

#     def __init__(self, user_id, role_id):
#         self.user_id = user_id
#         self.role_id = role_id

###Category
class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __init__(self, category_id, name):
        self.category_id = category_id
        self.name = name

###Post
class Post(db.Model):
    __tablename__ = 'post'
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    post_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    poster_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=False)

    def __init__(self, post_id, title, content, post_time, poster_id, category_id):
        self.post_id = post_id
        self.title = title
        self.content = content
        self.post_time = post_time
        self.poster_id = poster_id
        self.category_id = category_id

###Comment
class Comment(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    commenter_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)

    def __init__(self, content, post_time, commenter_id, post_id):
        self.content = content
        self.post_time = post_time
        self.commenter_id = commenter_id
        self.post_id = post_id

    def get_id(self):
        try:
            return text_type(self.cid)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')



###Like
class Like(db.Model):
    __tablename__ = 'like'
    likes_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)
    like_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, user_id, post_id, like_time):
        self.uid = user_id
        self.pid = post_id
        self.post_time = like_time

###Ban
class Ban(db.Model):
    __tablename__ = 'ban'
    ban_id = db.Column(db.Integer, primary_key=True)
    banned_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    banner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    ban_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, banned_id, banner_id, ban_time):
        self.banned_id = banned_id
        self.banner_id = banner_id
        self.ban_time = ban_time

###Report
class Report(db.Model):
    __tablename__ = 'report'
    report_id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)
    report_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)

    def __init__(self, reporter_id, post_id, report_time, content):
        self.reporter_id = reporter_id
        self.post_id = post_id
        self.report_time = report_time
        self.content = content



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


