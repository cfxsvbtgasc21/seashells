import flask
from . import Log
from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from .forms import RegisterForm,LoginForm,PasswordResetForm,PasswordResetRequestForm
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime, timedelta, timezone
from flask_wtf.csrf import generate_csrf
import random
from exts import db,mail
from flask_mail import Message

CAPTCHA_CODE = '1234'
@Log.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        csrf_token = generate_csrf()
        return render_template('login.html', csrf_token=csrf_token)
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.username.data
            password = form.password.data
            print(email, password)
            user = User.query.filter((User.email == email) | (User.username == email)).first()
            if not user:
                return redirect(url_for("Log.login"))
            if check_password_hash(user.password, password):
                print("验证通过")
                session['user_id'] = user.id
                return redirect("/")
            else:
                return redirect(url_for("Log.login"))
        else:
            print(form.errors)
            return redirect(url_for("Log.login"))

@Log.route('/logout')
def logout():
    session.pop('user_id', None)
    # flash('您已成功退出登录！', 'success')
    return redirect("/")
@Log.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        csrf_token = generate_csrf()
        return render_template('register.html', csrf_token=csrf_token)
    else:
        action = request.form.get('action')
        if action == 'send_code':  # 发送验证码
            print(request.form)
            email = request.form.get('email')
            if not email:
                return jsonify(code=400, message='empty email')

            # 生成6位随机验证码
            code = ''.join(random.choices('0123456789', k=6))

            # 存储验证码（有效期5分钟）
            flask.session['code'] = code
            flask.session['code_timestamp'] = datetime.now()
            # msg=Message(subject="海洋贝类智能识别系统注册",recipients=[email],body=f"验证码:{code}")
            # mail.send(msg)
            # 发送邮件（此处模拟打印到控制台）
            print(f'[模拟邮件] 验证码发送至 {email}: {code}')
            return jsonify(code=200, message='验证码已发送')

        else:  # 注册表单提交
            print(request.form)
            form = RegisterForm(request.form)
            print(flask.session.get('code'))
            # if form.checkcode.data != flask.session.get('code'):
            #     return jsonify(code=400, message='验证码错误')
            if form.validate():
                user = User(
                    username=form.username.data,
                    password=generate_password_hash(form.password.data),
                    email=form.email.data,
                    sex=form.gender.data,
                    birthday=form.birthday.data,
                    info=form.comment.data,
                    join_time=datetime.now()
                )
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('Log.logout'))
            else:
                error_messages = '; '.join(['; '.join(errors) for errors in form.errors.values()])
                print(error_messages)
                return jsonify(code=400, message=error_messages)


@Log.route('/password_reset', methods=['GET', 'POST'])
def password_reset():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            # 生成验证码
            code = ''.join(random.choices('0123456789', k=6))
            session['password_reset_code'] = code
            session['password_reset_email'] = email
            session['password_reset_code_expiration'] = datetime.now() + timedelta(minutes=5)
            print(code)
            # 发送验证码邮件
            # msg = Message('密码重置验证码', recipients=[email])
            # msg.body = f'您的验证码是：{code}，有效期为 5 分钟。'
            # mail.send(msg)
            flash('验证码已发送到您的邮箱，请在 5 分钟内完成验证。', 'success')
            return redirect(url_for('Log.verify_code'))
        else:
            flash('邮箱不存在，请检查！', 'danger')
    return render_template('password_reset.html')




@Log.route('/verify_code', methods=['GET', 'POST'])
def verify_code():
    if request.method == 'POST':
        code = request.form.get('code')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        session_code = session.get('password_reset_code')
        session_email = session.get('password_reset_email')
        session_expiration = session.get('password_reset_code_expiration')

        # 获取当前 UTC 时间
        current_time = datetime.now(timezone.utc)

        if session_expiration and current_time < session_expiration:
            if code == session_code:
                if password == confirm_password:
                    user = User.query.filter_by(email=session_email).first()
                    if user:
                        # 更新密码
                        user.password = generate_password_hash(password)
                        db.session.commit()
                        session.pop('password_reset_code', None)
                        session.pop('password_reset_email', None)
                        session.pop('password_reset_code_expiration', None)
                        flash('密码重置成功，请登录。', 'success')
                        return redirect(url_for('Log.login'))
                    else:
                        flash('用户不存在，请联系管理员。', 'danger')
                else:
                    flash('新密码与确认密码不一致！', 'danger')
            else:
                flash('验证码错误，请重新输入。', 'danger')
        else:
            flash('验证码已过期，请重新获取！', 'danger')
    return render_template('verify_code.html')