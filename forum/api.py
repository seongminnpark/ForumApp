#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/11/14 下午4:10 
# @Author : Gaoxiang Chen
# @Site :  
# @File : api.py 
# @Software: PyCharm
# ---------------------
from datetime import datetime

from flask import render_template, request, redirect, url_for, flash
# from flask_login import login_required, current_user, login_user, logout_user
# from .form import LoginForm, RegistrationForm, UpdateAccountForm, PostForm, CommentForm, ViewTopicForm
from forum import app, db
from .model import Topic, User, Category, Post, Comment, Like, Ban, Report
from flask import jsonify


# Function
@app.route('/')
def index():
    return render_template('index.html', title='index')


@app.route('/api/test')
def test():
    d = {}
    d["ok"] = True
    return jsonify(d)

# @app.route('/home')
# def home():
#     form = ViewTopicForm()
#     posts = Post.query.order_by(Post.post_time.desc()).all()
#     if form.validate_on_submit():
#         posts = Post.query.filter_by(tid=form.topic.data).first().order_by(Post.post_time.desc())
#     return render_template('home.html', title='index', posts=posts, form=form)


# @app.route('/home')
# def home():
#     topics = Topic.query.filter(Topic.parent_id == None).order_by(Topic.tid)
#     # posts = Post.query.order_by(Post.post_time.desc()).paginate(page, POSTS_PER_PAGE, False).items
#     users = User.query.all()
#     return render_template("home.html", topics=topics, users = users)


# @app.route('/topic')
# def topic():
#     tid = int(request.args.get("topic"))
#     topic = Topic.query.filter(Topic.tid == tid).first()
#     if not topic:
#         return error("That topic does not exist!")
#     posts = Post.query.filter(Post.tid == tid).order_by(Post.pid.desc()).limit(50)
#     if not topic.path:
#         topic.path = generateLinkPath(topic.tid)
#     topics = Topic.query.filter(Topic.parent_id == tid).all()
#     return render_template("topic.html", topic=topic, posts=posts, topics=topics, path=topic.path)



# def error(errormessage):
#     return "<b style=\"color: red;\">" + errormessage + "</b>"



# # Account
# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(username=form.username.data, _password=form.password.data, _email=form.email.data)
#         db.session.add(user)
#         db.session.commit()
#         flash('Your account has been created! You are now able to log in', 'success')
#         return redirect(url_for('login'))
#     return render_template('register.html', title='Register', form=form)


# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(_email=form.email.data).first()
#         if user._password == form.password.data:
#             login_user(user, remember=form.remember.data)
#             return redirect("/home")
#         else:
#             flash('Login Unsuccessful. Please check email and password', 'danger')
#     return render_template('login.html', title='Login', form=form)


# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('home'))


# @app.route("/account", methods=['GET', 'POST'])
# @login_required
# def account():
#     form = UpdateAccountForm()
#     if form.validate_on_submit():
#         current_user.username = form.username.data
#         current_user._email = form.email.data
#         current_user._password = form.password.data
#         db.session.commit()
#         flash('Your account has been updated!', 'success')
#         return redirect(url_for('home'))
#     elif request.method == 'GET':
#         form.username.data = current_user.username
#         form.email.data = current_user._email
#     return render_template('account.html', title='Account', form=form)


# # Post
# @login_required
# @app.route('/new_post', methods=['POST', 'GET'])
# def new_post():
#     form = PostForm()
#     topic = Topic.query.filter(Topic.tid == form.topic.data).first()
#     if form.validate_on_submit():
#         post = Post(title=form.title.data, content=form.content.data, post_time=datetime.utcnow(), uid=current_user.uid,
#                     tid=form.topic.data)
#         current_user.posts.append(post)
#         topic.posts.append(post)
#         db.session.add(post)
#         db.session.commit()
#         flash('Your post has been created!', 'success')
#         posts = Post.query.filter(Post.pid == post.pid).order_by(Post.pid.desc())
#         return redirect("/viewpost?post=" + str(post.pid))
#     return render_template('create_post.html', title='New Post',
#                            form=form)


# @app.route('/viewpost')
# def viewpost():
#     pid = int(request.args.get("post"))
#     post = Post.query.filter(Post.pid == pid).first()
#     if not post:
#         return error("That post does not exist!")
#     comments = Comment.query.filter(Comment.pid == pid).order_by(Comment.cid.desc())  # no need for scalability now
#     return render_template("viewpost.html", post=post, comments=comments)


# @login_required
# @app.route('/new_comment', methods=['POST', 'GET'])
# def comment():
#     form = CommentForm()
#     pid = int(request.args.get("post"))
#     post = Post.query.filter(Post.pid == pid).first()
#     if not post:
#         return error("That post does not exist!")
#     comment = Comment(content=form.content.data, post_time=datetime.utcnow(), pid=pid)
#     current_user.comments.append(comment)
#     post.comments.append(comment)
#     db.session.commit()
#     return redirect("/viewpost?post=" + str(pid))


# @login_required
# @app.route('/like', methods=['POST', 'GET'])
# def like():
#     pid = int(request.args.get("post"))
#     print(pid)
#     post = Post.query.filter(Post.pid == pid).first()
#     if not post:
#         return error("That post does not exist!")
#     likes = Like.query.filter(Like.pid == pid).first()
#     if (likes and likes.uid == current_user.uid):
#         error("You already like it!")
#     else:
#         like = Like(uid=current_user.uid, pid=pid, post_time=datetime.utcnow())
#         current_user.likes.append(like)
#         post.likes.append(like)
#         db.session.commit()
#     return redirect("/viewpost?post=" + str(pid))


# def generateLinkPath(tid):
#     links = []
#     topic = Topic.query.filter(Topic.tid == tid).first()
#     parent = topic.query.filter(Topic.tid == topic.parent_id).first()
#     links.append("<a href=\"/topic?topic=" + str(topic.tid) + "\">" + topic.topic + "</a>")
#     while parent is not None:
#         links.append("<a href=\"/topic?topic=" + str(parent.tid) + "\">" + parent.topic + "</a>")
#         parent = Topic.query.filter(Topic.tid == parent.parent_id).first()
#     links.append("<a href=\"/\">Forum Index</a>")
#     link = ""
#     for l in reversed(links):
#         link = link + " / " + l
#     return link

#
# @app.route('/topic', methods=['POST', 'GET'])
# def topic():
#     topics = Topic.queryAll()
#     post = Post.query.filter().first()
#     if not post:
#         return error("That post does not exist!")
#     likes = Like.query.filter(Like.uid == current_user.uid).first()
#     if (likes and likes.pid == pid):
#         error("You already like it!")
#     else:
#         like = Like(uid = current_user.uid, pid = pid, post_time = datetime.utcnow())
#         current_user.likes.append(like)
#         post.likes.append(like)
#         db.session.commit()
#     return redirect("/viewpost?post=" + str(pid))
