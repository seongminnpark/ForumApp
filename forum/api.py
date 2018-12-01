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
from sqlalchemy import func
# from flask_login import login_required, current_user, login_user, logout_user
# from .form import LoginForm, RegistrationForm, UpdateAccountForm, PostForm, CommentForm, ViewTopicForm
from forum import app, db
from .model import User, Category, Post, Comment, Likes, Ban, Report, ReportReason, ReportHasReason
from flask import jsonify

import functools


# Function
@app.route('/')
def index():
    return render_template('index.html', title='index')

@app.route('/api/user', methods=['GET', 'POST'])
def user():

    token = request.headers.get("token")

    if request.method == 'POST':
        nameRaw = request.form.get('name')
        emailRaw = request.form.get('email')
        passwordRaw = request.form.get('password')
        avatarIdRaw = request.form.get('avatarId')
        token = nameRaw
        newUser = User(nameRaw, emailRaw, passwordRaw, token, 0, avatarIdRaw)
        db.session.add(newUser)
        db.session.commit()

    # Query profile.
    user = User.getUserByToken(token)

    if request.method == 'GET':
        if user == None:
            return returnError(404, "Invalid user token supplied while fetching profile.")

    postsQuery = Post.getPostsByUser(user.user_id)
    likedPostsQuery = Likes.getLikedPostsByUser(user.user_id)
    commentsQuery = Comment.getCommentsByUser(user.user_id)

    # Construct profile data.
    profile = {}
    profile["name"] = user.name
    profile["dateJoined"] = user.date_joined
    profile["avatarId"] = user.avatar_id
    profile["likesReceived"] = getLikesReceived(user.user_id)
    profile["statusId"] = Ban.getBannedStatus(user.user_id) 
    profile["email"] = user.email
    profile["isAdmin"] = True if user.is_admin == 1 else False

    likedPosts = []
    for likedPost in likedPostsQuery:
        likedPosts.append(likedPost.post_id)
    profile["likedPosts"] = likedPosts 

    posts = []
    for post in postsQuery:
        posts.append({
            "id": post.post_id,
            "title": post.title,
            "date": post.post_time,
            "likes": Likes.getPostLikeCount(post.post_id),
            "commentCount": Comment.getCommentCount(post.post_id)
        })
    profile["posts"] = posts

    comments = []
    for comment in commentsQuery:
        comments.append({
            "postId": comment.post_id,
            "postTitle": Post.getPostById(comment.post_id).title,
            "date": comment.post_time,
            "content": comment.content
        })
    profile["comments"] = comments

    # Construct response.
    responseJSON = {
        "token": user.token,
        "profile": profile
    }
    return jsonify(responseJSON)

@app.route('/api/login', methods=['POST'])
def login():

    emailRaw = request.form.get('email')
    passwordRaw = request.form.get('password')
    
    # Query profile.
    user = User.getUserByEmail(emailRaw)

    if not user or hashPassword(passwordRaw) != user.password_hash:
        return returnError(400, "Wrong email or password.")

    postsQuery = Post.getPostsByUser(user.user_id)
    likedPostsQuery = Likes.getLikedPostsByUser(user.user_id)
    commentsQuery = Comment.getCommentsByUser(user.user_id)

    # Construct profile data.
    profile = {}
    profile["name"] = user.name
    profile["dateJoined"] = user.date_joined
    profile["avatarId"] = user.avatar_id
    profile["likesReceived"] = getLikesReceived(user.user_id)
    profile["statusId"] = Ban.getBannedStatus(user.user_id) 
    profile["email"] = user.email
    profile["isAdmin"] = True if user.is_admin == 1 else False

    likedPosts = []
    for likedPost in likedPostsQuery:
        likedPosts.append(likedPost.post_id)
    profile["likedPosts"] = likedPosts 

    posts = []
    for post in postsQuery:
        posts.append({
            "id": post.post_id,
            "title": post.title,
            "date": post.post_time,
            "likes": Likes.getPostLikeCount(post.post_id),
            "commentCount": Comment.getCommentCount(post.post_id)
        })
    profile["posts"] = posts

    comments = []
    for comment in commentsQuery:
        comments.append({
            "postId": comment.post_id,
            "postTitle": Post.getPostById(comment.post_id).title,
            "date": comment.post_time,
            "content": comment.content
        })
    profile["comments"] = comments

    # Construct response.
    responseJSON = {
        "token": user.token,
        "profile": profile
    }
    return jsonify(responseJSON)

def getLikesReceived(user_id):
    query = (db.session.query(User,Post,Likes)
                .filter(Post.poster_id == User.user_id)
                .filter(Likes.post_id == Post.post_id)).all()
    return len(query)

def hashPassword(password):
    return password

@app.route('/api/posts', methods=['GET'])
def posts():

    if request.method == 'POST':
        pass

    filterLiked = True if request.args.get("liked") == 'true' else False
    filterCategoryId = request.args.get("categoryId")
    sortMethod = request.args.get("sortMethod")
    token = request.headers.get("token")

    if token:
        user = User.getUserByToken(token)

    # Query posts.
    postsQuery = Post.getAll()
    
    posts = []
    for post in postsQuery:

        # Filter liked posts.
        if (user and filterLiked and not Likes.userLikedPost(user.user_id, post.post_id)):
                continue

        # Filter by category id.
        if filterCategoryId:
            if (filterCategoryId != 'all' and str(post.category_id) != filterCategoryId):
                continue 
                

        postObject = constructPostTile(post)
        posts.append(postObject)
        
    # Construct response.
    responseJSON = {
        "posts": sortPosts(posts, sortMethod)
    }
    response = jsonify(responseJSON)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

def comparePostsByNewest(a, b):
    aTime = a['date']
    bTime = b['date']
    if aTime < bTime:
        return 1
    elif aTime == bTime:
        return 0
    else:
        return -1

def comparePostsByOldest(a, b):
    aTime = a['date']
    bTime = b['date']
    if aTime > bTime:
        return 1
    elif aTime == bTime:
        return 0
    else:
        return -1

def comparePostsByLikes(a, b):
    aLikes = a['likes']
    bLikes = a['likes']
    if aLikes > bLikes:
        return 1
    elif aLikes == bLikes:
        return 0
    else:
        return -1

def sortPosts(posts, sortMethod):
    if sortMethod == '0':
        return sorted(posts, key=functools.cmp_to_key(comparePostsByNewest))
    elif sortMethod == '1':
        return sorted(posts, key=functools.cmp_to_key(comparePostsByOldest))
    elif sortMethod == '2':
        return sorted(posts, key=functools.cmp_to_key(comparePostsByLikes))


@app.route('/api/post', defaults={'postId': 0}, methods=['POST'])
@app.route('/api/post/<int:postId>', methods=['GET'])
def post(postId):

    filterLiked = True if request.args.get("liked") == 'true' else False 
    filterCategoryId = request.args.get("categoryId")
    token = request.headers.get("token")

    if request.method == 'POST':
        poster = User.getUserByToken(token)

        if not poster:
            returnError(403, "Invalid user. Please log in again.")

        title = request.form.get('title')
        content = request.form.get('content')
        categoryId = request.form.get('categoryId')
        newPost = Post(title, content, poster.user_id, categoryId)
        db.session.add(newPost)
        db.session.commit()

        # Query posts.
        postsQuery = Post.getAll()
        
        posts = []
        for post in postsQuery:

            # Filter liked posts.
            if (user and filterLiked and not Likes.userLikedPost(user.user_id, post.post_id)):
                    continue

            # Filter by category id.
            if filterCategoryId:
                if (filterCategoryId != 'all' and str(post.category_id) != filterCategoryId):
                    continue 
                    

            postObject = constructPostTile(post)
            posts.append(postObject)

        # Construct response.
        responseJSON = {
            "posts": posts
        }

    if request.method == 'GET':
        post = Post.getPostById(postId)

        postObject = {}
        poster = User.getUserById(post.post_id)
        
        postObject["title"] = post.title
        postObject["date"] = post.post_time
        postObject["author"] = poster.name if poster != None else None
        postObject["content"] = post.content
        postObject["author_avatar_id"] = poster.avatar_id if poster != None else None
        postObject["likes"] = Likes.getPostLikeCount(post.post_id)

        commentsQuery = Comment.getComments(post.post_id)
        comments = []
        for comment in commentsQuery:
            commentObject = {}
            commenter = User.getUserById(comment.commenter_id)

            commentObject["name"] = commenter.name
            commentObject["avatarId"] = commenter.avatar_id
            commentObject["content"] = comment.content
            commentObject["date"] = comment.post_time

            comments.append(commentObject)
        
        postObject["comments"] = comments

        responseJSON = {
            "post": postObject
        }

    return jsonify(responseJSON)

@app.route('/api/comment', methods=['POST'])
def comment():

    token = request.headers.get("token")

    user = User.getUserByToken(token)

    if not user:
        returnError(403, "Invalid user. Please log in again.")

    postId = request.form.get('postId')
    content = request.form.get('content')
  
    newComment = Comment(content, user.user_id, postId)
    db.session.add(newComment)
    db.session.commit()

    post = Post.getPostById(postId)

    postObject = {}
    poster = User.getUserById(post.post_id)
    
    postObject["title"] = post.title,
    postObject["date"] = post.post_time,
    postObject["author"] = poster.name,
    postObject["content"] = post.content,
    postObject["author_avatar_id"] = poster.avatar_id,
    postObject["likes"] = Likes.getPostLikeCount(post.post_id),

    commentsQuery = Comment.getComments(post.post_id)
    comments = []
    for comment in commentsQuery:
        commentObject = {}
        commenter = User.getUserById(comment.commenter_id)

        commentObject["name"] = commenter.name
        commentObject["avatarId"] = commenter.avatar_id
        commentObject["content"] = comment.content
        commentObject["date"] = comment.post_time

        comments.append(commentObject)
    
    postObject["comments"] = comments

    responseJSON = {
        "post": postObject
    }

    return jsonify(responseJSON)

def constructPostTile(post):
    postObject = {}
    poster = User.getUserById(post.poster_id)
    
    postObject["id"] = post.post_id
    postObject["title"] = post.title
    postObject["date"] = post.post_time
    postObject["author"] = poster.name
    postObject["content"] = post.content
    postObject["author_avatar_id"] = poster.avatar_id
    postObject["category_id"] = post.category_id
    postObject["likes"] = Likes.getPostLikeCount(post.post_id)
    
    commentsQuery = Comment.getComments(post.post_id)
    commentAvatars = []
    for comment in commentsQuery:
        commenter = User.getUserById(comment.commenter_id)
        commentAvatars.append(commenter.avatar_id)

    postObject["comments"] = len(commentsQuery)
    postObject["commenter_avatar_ids"] = commentAvatars
    return postObject

@app.route('/api/reports', methods=['GET'])
def reports():

    token = request.headers.get("token")
    user = User.getUserByToken(token)

    if not user or not user.is_admin:
        returnError(403, "Only admins can view reports.")

    # Query reports.
    reportsQuery = Report.getAll()
    reports = []
    for report in reportsQuery:
        reportObject = {}

        reportObject["report_id"] =  report.report_id
        reportObject["reported_name"] = User.getUserById(Post.getPostById(report.post_id).poster_id).name
        reportObject["reporter_name"] = User.getUserById(report.reporter_id).name
        reportObject["report_date"] =  report.report_time
        reportObject["report_reason_ids"] = ReportHasReason.getReasonsForReport(report.report_id)
        reportObject["reported_post_id"] = report.post_id

        reports.append(reportObject)

    # Query bans.
    bansQuery = Ban.getAll()
    bans = []
    for ban in bansQuery:
        banObject = {}

        banObject["ban_id"] = ban.ban_id
        banObject["banned_name"] = User.getUserById(ban.banned_id).name
        banObject["banned_by"] = User.getUserById(ban.banner_id).name
        banObject["banned_date"] = ban.ban_time
        banObject["banned_reason_ids"] = ReportHasReason.getReasonsForReport(ban.report_id)

        bans.append(banObject)

    responseJSON = {
        "reports": reports,
        "bans": bans
    }

    return jsonify(responseJSON)

@app.route('/api/ban', methods=['POST'])
def ban():

    token = request.headers.get("token")
    user = User.getUserByToken(token)

    if not user or not user.is_admin:
        returnError(403, "Only admins can ban users.")
    
    # Extract report ids to ban.
    reportIdsRaw = request.form.get('reportIds').split(',')
    reportIds = [int(x) for x in reportIdsRaw]

    for reportId in reportIds:
        report = Report.getReportById(reportId)
        reported_id = Post.getPostById(report.post_id).poster_id

        if not Ban.getBannedStatus(reported_id):
            newBan = Ban(reported_id, user.user_id, report.report_id, 1)
            db.session.add(newBan)
        
        report.active = 0

    db.session.commit()

    # Query reports.
    reportsQuery = Report.getAll()
    reports = []
    for report in reportsQuery:
        reportObject = {}

        reportObject["report_id"] =  report.report_id
        reportObject["reported_name"] = User.getUserById(Post.getPostById(report.post_id).poster_id).name
        reportObject["reporter_name"] = User.getUserById(report.reporter_id).name
        reportObject["report_date"] =  report.report_time
        reportObject["report_reason_ids"] = ReportHasReason.getReasonsForReport(report.report_id)
        reportObject["reported_post_id"] = report.post_id

        reports.append(reportObject)

    # Query bans.
    bansQuery = Ban.getAll()
    bans = []
    for ban in bansQuery:
        banObject = {}

        banObject["ban_id"] = ban.ban_id
        banObject["banned_name"] = User.getUserById(ban.banned_id).name
        banObject["banned_by"] = User.getUserById(ban.banner_id).name
        banObject["banned_date"] = ban.ban_time
        banObject["banned_reason_ids"] = ReportHasReason.getReasonsForReport(ban.report_id)

        bans.append(banObject)

    responseJSON = {
        "reports": reports,
        "bans": bans
    }

    return jsonify(responseJSON)

@app.route('/api/unban', methods=['POST'])
def unban():

    token = request.headers.get("token")
    user = User.getUserByToken(token)

    if not user or not user.is_admin:
        returnError(403, "Only admins can ban users.")
    
    # Extract report ids to ban.
    banIdsRaw = request.form.get('banIds').split(',')
    banIds = [int(x) for x in banIdsRaw]

    for banId in banIds:
        ban = Ban.getBanById(banId)
        ban.active = 0
        
    db.session.commit()

    # Query reports.
    reportsQuery = Report.getAll()
    reports = []
    for report in reportsQuery:
        reportObject = {}

        reportObject["report_id"] =  report.report_id
        reportObject["reported_name"] = User.getUserById(Post.getPostById(report.post_id).poster_id).name
        reportObject["reporter_name"] = User.getUserById(report.reporter_id).name
        reportObject["report_date"] =  report.report_time
        reportObject["report_reason_ids"] = ReportHasReason.getReasonsForReport(report.report_id)
        reportObject["reported_post_id"] = report.post_id

        reports.append(reportObject)

    # Query bans.
    bansQuery = Ban.getAll()
    bans = []
    for ban in bansQuery:
        banObject = {}

        banObject["ban_id"] = ban.ban_id,
        banObject["banned_name"] = User.getUserById(ban.banned_id).name
        banObject["banned_by"] = User.getUserById(ban.banner_id).name
        banObject["banned_date"] = ban.ban_time
        banObject["banned_reason_ids"] = ReportHasReason.getReasonsForReport(ban.report_id)

        bans.append(banObject)

    responseJSON = {
        "reports": reports,
        "bans": bans
    }

    return jsonify(responseJSON)

@app.route('/api/report', methods=['POST'])
def report():

    token = request.headers.get("token")
    user = User.getUserByToken(token)

    if not user:
        return returnError(403, "Invalid user. Please log in again.")

    postId = request.form.get('postId')
    comment = request.form.getlist('comment')
    newReport = Report(user.user_id, postId, comment, 1)
    db.session.add(newReport)
    db.session.flush()
    db.session.refresh(newReport)

    reportReasonIdsRaw = request.form.get('reportReasonIds').split(',')
    reportReasonIds = [int(x) for x in reportReasonIdsRaw]

    for reasonId in reportReasonIds:
        newReason = ReportHasReason(newReport.report_id, reasonId)
        db.session.add(newReason)
    db.session.commit()

    return jsonify({}), 200

@app.route('/api/like', methods=['POST'])
def like():

    token = request.headers.get("token")

    user = User.getUserByToken(token)

    if not user:
        returnError(403, "Invalid user. Please log in again.")

    postId = request.form.get('postId')

    like = Likes.getLike(user.user_id, postId)
    
    if not like:
        newLike = Likes(user.user_id, postId)
        db.session.add(newLike)
    else:
        db.session.delete(like)
    db.session.commit()

    responseJSON = {
        "likedPosts": [x.post_id for x in Likes.getLikedPostsByUser(user.user_id)]
    }

    return jsonify(responseJSON)

@app.route('/api/stats', methods=['GET'])
def stats():

    postCountQuery = db.session.query(Post.poster_id, func.count(Post.post_id)).group_by(Post.poster_id).order_by(func.count(Post.post_id).desc()).first()

    likeCountQuery = db.session.query(Post.poster_id, func.count(Post.poster_id)).join(Likes).filter(Post.post_id == Likes.post_id).group_by(Post.poster_id).order_by(func.count(Post.poster_id).desc()).first()

    likePostQuery = db.session.query(Likes.post_id, func.count(Likes.post_id)).group_by(Likes.post_id).order_by(func.count(Likes.post_id).desc()).first()

    bansCountQuery = db.session.query(Ban.banned_id, func.count(Ban.ban_id)).group_by(Ban.banned_id).order_by(func.count(Ban.ban_id).desc()).first()

    responseJSON = {
        "post_count": len(Post.getAll()),
        "user_count": len(User.getAll()),
        "category_count": {
            "Announcement": Post.getPostCountByCategoryId(1),
            "Discussion": Post.getPostCountByCategoryId(2),
            "Questin": Post.getPostCountByCategoryId(3),
            "Guide": Post.getPostCountByCategoryId(4)
        },
        "most_posts_count": postCountQuery[1],
        "most_posts_name": User.getUserById(postCountQuery[0]).name,
        "most_likes_count": likeCountQuery[1],
        "most_likes_name": User.getUserById(likeCountQuery[0]).name,
        "most_likes_post_count": likePostQuery[1],
        "most_likes_post_name": User.getUserById(likePostQuery[0]).name,
        "most_bans_count": bansCountQuery[1],
        "most_bans_name": User.getUserById(bansCountQuery[0]).name
    }

    return jsonify(responseJSON)

def returnError(statusCode, message):
    return jsonify({"message": message}), statusCode 

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
