from flask import render_template

from . import Log

@Log.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@Log.route('/logout')
def logout():
    return "登出页面"