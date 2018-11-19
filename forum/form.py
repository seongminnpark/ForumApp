#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/11/14 下午4:06 
# @Author : Gaoxiang Chen
# @Site :  
# @File : form.py 
# @Software: PyCharm
# ---------------------


from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from model import User, Topic


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm_password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField()

    def validate_username(self, username):
       user = User.query.filter_by(username=username.data).first()
       if user:
            raise ValidationError("That username is taken. Please choose a different one.")

    def validate_email(self, email):
       user = User.query.filter_by(_email=email.data).first()
       if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm_password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user._email:
            user = User.query.filter_by(_email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')



class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    topic = SelectField('Topic', choices=[(t.tid, t.topic) for t in Topic.all_topics()], coerce=int)
    submit = SubmitField('Post')



class CommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class ViewTopicForm(FlaskForm):
    topic = SelectField('Topic', choices=[(t.tid, t.topic) for t in Topic.all_topics()], coerce=int)
    submit = SubmitField('Sure')