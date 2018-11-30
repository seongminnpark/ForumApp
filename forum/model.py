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
    name = db.Column(db.String(20))
    email = db.Column(db.String(20))
    password_hash = db.Column(db.String(20))
    token = db.Column(db.String(20))
    is_admin = db.Column(db.Integer)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow())
    avatar_id = db.Column(db.Integer)

    def __init__(self, name, email, password_hash, token, is_admin, avatar_id):
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.token = token
        self.is_admin = is_admin
        self.avatar_id = avatar_id

    @classmethod
    def getAll(self):
        return self.query.all()

    @classmethod
    def getUserById(self, user_id):
        return self.query.get(user_id)
    
    @classmethod
    def getUserByToken(self, token):
        return self.query.filter(User.token == token).first()

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

    def __init__(self, title, content, poster_id, category_id):
        self.title = title
        self.content = content
        self.poster_id = poster_id
        self.category_id = category_id

    @classmethod
    def getPostsByUser(self, user_id):
        return self.query.filter(Post.poster_id == user_id).all()
    
    @classmethod
    def getPostById(self, post_id):
        return self.query.filter(Post.post_id == post_id).first()
    
    @classmethod
    def getAll(self):
        return self.query.all()

###Comment
class Comment(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    commenter_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)

    def __init__(self, content, commenter_id, post_id):
        self.content = content
        self.commenter_id = commenter_id
        self.post_id = post_id

    def get_id(self):
        try:
            return text_type(self.cid)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    @classmethod
    def getComments(self, post_id):
        return self.query.filter(Comment.post_id == post_id).all()

    @classmethod
    def getCommentCount(self, post_id):
        return self.query.filter(Comment.post_id == post_id).count()



###Likes
class Likes(db.Model):
    __tablename__ = 'likes'
    likes_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)
    like_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, user_id, post_id, like_time):
        self.uid = user_id
        self.pid = post_id
        self.post_time = like_time
    
    @classmethod
    def getLikedPostsByUser(self, user_id):
        return self.query.filter(Likes.user_id == user_id).all()
    
    @classmethod
    def getPostLikeCount(self, post_id):
        return self.query.filter(Likes.post_id == post_id).count()
    
    @classmethod
    def userLikedPost(self, user_id, post_id):
        return self.query.filter(Likes.user_id == user_id).filter(Likes.post_id == post_id) != None

###Ban
class Ban(db.Model):
    __tablename__ = 'ban'
    ban_id = db.Column(db.Integer, primary_key=True)
    banned_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    banner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    ban_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    active = db.Column(db.Integer, default=1)

    def __init__(self, banned_id, banner_id, ban_time, active):
        self.banned_id = banned_id
        self.banner_id = banner_id
        self.ban_time = ban_time
        self.active = active
    
    @classmethod
    def getBannedStatus(self, user_id):
        query = self.query.filter(Ban.banned_id == user_id).first()
        print(query)
        print(None and None)
        if query != None and not query.active: return 1
        else: return 0

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



# ###Topic
# class Topic(db.Model):
#     __tablename__ = 'topics'
#     tid = db.Column(db.Integer, primary_key=True)
#     topic = db.Column(db.String(20))
#     _description = db.Column(db.String(20))
#     parent_id = db.Column(db.String(20))
#     posts = db.relationship("Post", backref="topics")
#     path = None

#     def __init__(self, topic, _description, parent_id):
#         self.topic = topic
#         self._description = _description
#         self.parent_id = parent_id

#     @classmethod
#     def all_topics(self):
#         return self.query.all()

#     @classmethod
#     def getTopicById(self, tid):
#         return self.query.get(tid)

#     @classmethod
#     def getTopicList(self):
#         return [{t.topic} for t in Topic.all_topics()]


