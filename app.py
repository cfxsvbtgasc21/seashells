from datetime import timedelta
import random
from flask import Flask, render_template, g, session, redirect, url_for, request, jsonify
import flask
from exts import db,mail,limiter
from models import User
from flask_migrate import Migrate
from recognition import rec
from log import Log
from blog import blog
import threading
import config
import schedule
import time
import shutil
import os
import redis
# 在后台线程中运行定时任务
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # 使用随机生成的密钥替代硬编码密钥
# app.redis = redis.Redis(
#     host='localhost',
#     port=6379,
#     db=0,
#     decode_responses=True
# )
limiter.init_app(app)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)
# flask.session['email_code'] = '1234'
app.register_blueprint(rec, url_prefix='/rec')
app.register_blueprint(Log, url_prefix='/log')  # 为Log模块添加前缀
app.register_blueprint(blog, url_prefix='/blog')

UPLOAD_FOLDER = 'static/uploads'# 原始图片上传到的相对路径
app.jinja_env.filters['zip'] = zip
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制上传文件大小为16MB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
directory = 'uploads/' # 识别结果存储的相对路径
# 获取ip地址
app.secret_key = 'your_secret_key_here'
index_map = {
    0: "鲍鱼",
    1: "钉螺",
    2: "海虹",
    3: "海螺",
    4: "扇贝",
    5: "生蚝",
    6: "缢蛏",
    7: "青柳蛤",
    8: "白贝",
    9: "象拔蚌",
    10: "北极贝",
    11: "毛钳"
}
def cleanup_temp_dir(temp_dir):
    """清理临时目录中的所有文件"""
    print("deleting...")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    for filename in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')
    print("finished")
# 每10分钟清理一次
schedule.every(1).minutes.do(lambda: cleanup_temp_dir(UPLOAD_FOLDER))
schedule.every(1).minutes.do(lambda: cleanup_temp_dir(directory))

# 启动定时任务
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
# 在后台线程中运行定时任务
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()
@app.before_request
def before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(int(user_id))
        setattr(g, 'user', user)
    else:
        g.user = None
@app.context_processor
def my_context_processor():
    return {"user":getattr(g, 'user', None) }

@app.route('/introduction', methods=['POST', 'GET'])
def introduction():
    return render_template('1.html')
@app.route('/user_help', methods=['POST', 'GET'])
def user_help():
    return render_template('2.html')
@app.route('/authors', methods=['POST', 'GET'])
def authors():
    return render_template('3.html')
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')  # 生产环境禁用debug模式

