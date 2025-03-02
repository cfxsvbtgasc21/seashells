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
from flask_login import current_user

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


@blog.route('/user_posts/<username>',methods=['GET', 'POST'])
@login_required
def user_posts(username):
    # 查询当前用户发布的所有帖子
    posts = Post.query.filter_by(author_name=username).all()
    return render_template('user_posts.html', posts=posts)


@blog.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    # 查询帖子
    post = Post.query.get_or_404(post_id)
    # 检查用户是否有权限删除
    if post.author != g.user:
        return "您没有权限删除这个帖子", 403
    # 删除帖子
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.user_posts',username=g.user.username))

@blog.route('/post_detail', methods=['GET', 'POST'])
def post_detail():
    return "此功能预留"

