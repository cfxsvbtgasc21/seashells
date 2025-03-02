import flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError
from models import User
from datetime import datetime
import re

class PostForm(FlaskForm):
    title = StringField(validators=[
        DataRequired(message="帖子标题不能为空"),
        Length(min=1, max=100, message="帖子标题长度1-100位")
    ])

    content = TextAreaField(validators=[
        DataRequired(message="帖子内容不能为空"),
        Length(min=1, max=1000, message="帖子内容长度1-1000字")
    ])
