from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError
from models import User
from datetime import datetime
import redis

class RegisterForm(FlaskForm):
    # 字段名称必须与HTML中的name属性完全一致（包括大小写和短横线）
    username = StringField(validators=[
        DataRequired(message="用户名不能为空"),
        Length(min=3, max=25, message="用户名长度3-25位"),

    ])

    password = PasswordField(validators=[
        DataRequired(message="密码不能为空"),
        Length(min=8, max=20, message="密码长度8-20位"),
        Regexp(r'^(?=.*[A-Za-z])(?=.*[\d\W])[A-Za-z\d\W]{8,20}$', message="密码需包含至少两种组合（字母、数字、字符）")
    ])

    password2 = PasswordField(validators=[
        DataRequired(message="请确认密码"),
        EqualTo('password', message="两次密码不一致")
    ])

    email = StringField(validators=[
        DataRequired(message="邮箱不能为空"),
        Email(message="邮箱格式错误"),
        Length(max=120, message="邮箱过长")
    ])

    gender = RadioField(choices=[('man','男'), ('woman','女')], validators=[
        DataRequired(message="请选择性别")
    ])

    birthday = DateField(format='%Y-%m-%d', validators=[
        DataRequired(message="请选择生日")
    ])

    comment = TextAreaField(validators=[
        Length(max=500, message="简介不能超过500字")
    ])

    # checkcode = StringField(validators=[
    #     DataRequired(message="验证码不能为空"),
    #     Length(min=4, max=4, message="验证码必须为4位")
    # ])

    # 注意：email-code需要转换为Python合法的字段名
    email_code = StringField(
        '邮箱验证码',
        name='email-code',
        validators=[
            DataRequired(message="邮箱验证码不能为空"),
            Length(min=6, max=6, message="验证码必须为6位")
        ]
    )

    def validate_email_code(self, field):
        user_code = field.data
        # 从 session 中获取之前发送的验证码
        with redis.Redis(host='192.168.43.169', port=6379, password='620302') as redis_client:
            stored_captcha = redis_client.get(self.email.data)

            print(stored_captcha,user_code)
            if not stored_captcha:
                raise ValidationError('验证码已过期')
            else:
                stored_captcha = stored_captcha.decode('utf-8')
                if stored_captcha != self.email_code.data:
                    raise ValidationError('验证码错误')
                else:
                    redis_client.delete(self.email.data)
    def validate_birthday(self, field):
        now=datetime.now()
        if now.date()<field.data:
            raise ValidationError('生日设置非法')
    # 自定义验证方法
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')

class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired(message="用户名不能为空")])
    password = StringField(validators=[Length(min=8, max=20, message="密码格式错误！")])


class PasswordResetRequestForm(FlaskForm):
    email = StringField('邮箱地址', validators=[DataRequired(message="邮箱不能为空"), Email(message="邮箱格式错误")])

class PasswordResetForm(FlaskForm):
    code = StringField('验证码', validators=[DataRequired(), Length(min=6, max=6)])
    password = PasswordField('新密码', validators=[
        DataRequired(message="密码不能为空"),
        Length(min=8, max=20, message="密码长度8-20位"),
        Regexp(r'^(?=.*[A-Za-z])(?=.*[\d\W])[A-Za-z\d\W]{8,20}$', message="密码需包含至少两种组合（字母、数字、字符）")
    ])
    confirm_password = PasswordField('确认新密码', validators=[DataRequired(), EqualTo('password')])