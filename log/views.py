from . import Log

@Log.route('/login', methods=['GET', 'POST'])
def login():
    return "登录页面"

@Log.route('/logout')
def logout():
    return "登出页面"