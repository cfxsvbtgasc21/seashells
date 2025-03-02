from flask import abort, session, redirect, url_for


def login_required(func):
    """装饰器：确保用户登录"""
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            # 如果未登录，重定向到登录页面
            return redirect(url_for('Log.login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper