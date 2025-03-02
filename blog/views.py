import flask
from . import blog
from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify,g
# from .forms import RegisterForm,LoginForm
from models import db, User,Post
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_wtf.csrf import generate_csrf
import random
from exts import db,mail
from flask_mail import Message
from decorators import login_required
from .forms import PostForm


# 从数据库中获取帖子数据
# posts = Post.query.all()
@blog.before_request
def before_request():
    """在请求前处理，传递用户上下文"""
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            flask.g.user = user  # 将用户对象传递到全局变量
        else:
            flask.g.user = None
    else:
        flask.g.user = None
@blog.route('/')
def show_blog():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('forum.html',posts=posts)
@blog.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            author_name=g.user.username,
            created_at=datetime.now()
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('blog.show_blog'))
    else:
        return render_template('post.html', form=form)

# @blog.route('/submit_post', methods=['GET','POST'])
# def submit_post():
#     return redirect(url_for('blog.blog'))
#
@blog.route('/post_detail', methods=['GET', 'POST'])
def post_detail():
    return "unknown details"

