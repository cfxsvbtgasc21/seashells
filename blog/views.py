import flask
from . import blog
from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
# from .forms import RegisterForm,LoginForm
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_wtf.csrf import generate_csrf
import random
from exts import db,mail
from flask_mail import Message


# 从数据库中获取帖子数据
# posts = Post.query.all()
@blog.route('/')
def show_blog():
    return render_template('forum.html',posts=None)
@blog.route('/post')
def post():
    return render_template('post.html')

# @blog.route('/submit_post', methods=['GET','POST'])
# def submit_post():
#     return redirect(url_for('blog.blog'))
#
# @blog.route('/post_detail', methods=['GET', 'POST'])
# def post_detail():
#     return redirect(url_for('blog.blog'))

    # title = request.form['title']
    # content = request.form['content']
    # author = current_user.username  # 假设用户已登录
    # new_post = Post(title=title, content=content, author=author)
    # db.session.add(new_post)
    # db.session.commit()
