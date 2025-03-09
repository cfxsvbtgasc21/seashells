import flask
from . import Log
from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from .forms import RegisterForm,LoginForm,PasswordResetForm,PasswordResetRequestForm
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, timezone
from flask_wtf.csrf import generate_csrf
import random
from exts import db,mail,limiter
from flask_mail import Message
import redis

redis_client =redis.Redis(host='192.168.43.169', port=6379, password='620302')

@Log.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute",methods=['POST'])
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
                return jsonify({'status': 'error', 'message': '用户名或密码错误'})
            if check_password_hash(user.password, password):
                print("验证通过")
                session['user_id'] = user.id
                session.pop('failed_attempts', None)
                return jsonify({'status': 'success', 'message': '登录成功'})
            else:
                return jsonify({'status': 'error', 'message': '用户名或密码错误'}),401
        else:
            return jsonify({'status':'error','message':'非法用户名或密码'}),401


@Log.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect("/")


@Log.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        csrf_token = generate_csrf()
        return render_template('register.html', csrf_token=csrf_token)
    else:
        form = RegisterForm(request.form)
        print(request.form)
        #连接数据库
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
            return jsonify(code=200, message="注册成功")
        else:
            error_messages = '; '.join(['; '.join(errors) for errors in form.errors.values()])
            print(error_messages)
            return jsonify(code=400, message=error_messages)

@Log.route('/register/send_code', methods=['POST'])
@limiter.limit("1 per minute",methods=['POST'])
def register_send_code():
    print(request.form)
    email = request.form.get('email')
    form=PasswordResetRequestForm(request.form)
    if form.validate():
        # 生成6位随机验证码
        code = ''.join(random.choices('0123456789', k=6))
        try:
            with redis.Redis(host='192.168.43.169', port=6379, password='620302') as redis_client:
                redis_client.set(email, code)
                redis_client.expire(email, 60)
        except Exception as e:
            return jsonify(code=500, message=f'Redis connection error: {e}')
        # msg=Message(subject="海洋贝类智能识别系统注册",recipients=[email],body=f"验证码:{code}")
        # mail.send(msg)
        # 发送邮件（此处模拟打印到控制台）
        print(f'[模拟邮件] 验证码发送至 {email}: {code}')
        return jsonify(code=200, message='验证码已发送')
    else:
        error_messages = '; '.join(['; '.join(errors) for errors in form.errors.values()])
        print(error_messages)
        return jsonify(code=400, message=error_messages)


@Log.route('/password_reset', methods=['GET', 'POST'])
def password_reset():
    if request.method == 'POST':
        print(request.form)
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        print(email,user)
        session['passwordResetEmail'] = email
        if user:
            # 生成验证码
            code = ''.join(random.choices('0123456789', k=6))
            try:
                with redis.Redis(host='192.168.43.169', port=6379, password='620302') as redis_client:
                    redis_client.set(email, code)
                    redis_client.expire(email, 60)
            except Exception as e:
                return jsonify(code=500, message=f'Redis connection error: {e}')
            print(code)
            # 发送验证码邮件
            # msg = Message('密码重置验证码', recipients=[email])
            # msg.body = f'您的验证码是：{code}，有效期为 5 分钟。'
            # mail.send(msg)
            # flash('验证码已发送到您的邮箱，请在 5 分钟内完成验证。', 'success')
            return jsonify(code=200, message='验证码已发送')
        else:
            return jsonify(code=400, message='邮箱不存在，请检查！')
    csfr_token = generate_csrf()
    return render_template('password_reset.html',csrf_token=csfr_token)

@Log.route('/verify_code', methods=['GET', 'POST'])
def verify_code():
    csrf_token = generate_csrf()
    if request.method == 'POST':
        # email = request.form.get('email')
        email = session.get('passwordResetEmail')
        form = PasswordResetForm(request.form)
        # 验证
        if form.validate():
            code = request.form.get('code')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            try:
                with redis.Redis(host='192.168.43.169', port=6379, password='620302') as redis_client:
                    # 获取存储在 Redis 中的验证码和过期时间
                    stored_code = redis_client.get(email)
                    if stored_code:
                        stored_code = stored_code.decode('utf-8')
                        if code == stored_code:
                            if password == confirm_password:
                                user = User.query.filter_by(email=email).first()
                                if user:
                                 # 更新密码
                                    user.password = generate_password_hash(password)
                                    db.session.commit()
                                    redis_client.delete(email)
                                    session.pop('passwordResetEmail', None)
                                    return jsonify(code=200, message='密码重置成功，请登录。')
                                else:
                                    return jsonify(code=400, message='用户不存在，请联系管理员。')
                            else:
                                    return jsonify(code=400, message='新密码与确认密码不一致！')
                        else:
                                return jsonify(code=400, message='验证码错误，请重新输入。')
                    else:
                            return jsonify(code=400, message='验证码已过期，请重新获取！')
            except Exception as e:
                return jsonify(code=500, message=f'Redis connection error: {e}')
        else:
            error_messages = '; '.join(['; '.join(errors) for errors in form.errors.values()])
            print(error_messages)
            return jsonify(code=400, message=error_messages)
    return render_template('verify_code.html',csrf_token=csrf_token)
@Log.route('/resend_code', methods=['POST'])
@limiter.limit("1 per minute",methods=['POST'])
def resend_code():
    # 从 session 中获取邮箱地址
    email = session.get('passwordResetEmail')
    if not email:
        return jsonify(code=400, message='未找到需要重置密码的邮箱地址。')

    # 生成新的验证码
    new_code = str(random.randint(100000, 999999))
    print(new_code)
    try:
        with redis.Redis(host='192.168.43.169', port=6379, password='620302') as redis_client:
            # 存储新的验证码到 Redis，设置过期时间为 5 分钟
            redis_client.set(email, new_code, ex=300)

        # 这里应该调用发送邮件的逻辑，将验证码发送到用户邮箱
        # send_email(email, '您的验证码', f'您的验证码是：{new_code}')

        return jsonify(code=200, message='验证码已重新发送，请查收邮件。')
    except Exception as e:
        return jsonify(code=500, message=f'Redis connection error: {e}')