from flask import render_template

from . import Log

@Log.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@Log.route('/logout')
def logout():
    print("登出页面")
    return render_template('login.html')
@ Log.route('/register')
def register():
    return render_template('register.html')