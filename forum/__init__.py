#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/11/14 下午8:44 
# @Author : Gaoxiang Chen
# @Site :  
# @File : run.py.py
# @Software: PyCharm
# ---------------------

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://seongmin:12345@localhost/test1"
app.config['SECRET_KEY'] = '12345'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# login_manager = LoginManager(app)
# login_manager.init_app(app)
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'

from forum import api