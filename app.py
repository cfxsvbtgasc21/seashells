from flask import Flask, render_template
import socket
from log import Log
import threading
import schedule
import time
import shutil
import os
# 在后台线程中运行定时任务
app = Flask(__name__)
from recognition import rec
app.register_blueprint(rec, url_prefix='/rec')
app.register_blueprint(Log, url_prefix='/log')  # 为Log模块添加前缀
UPLOAD_FOLDER = 'static/uploads'# 原始图片上传到的相对路径
app.jinja_env.filters['zip'] = zip
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制上传文件大小为16MB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)  # 使用随机生成的密钥替代硬编码密钥
directory = 'uploads/' # 识别结果存储的相对路径
# 获取ip地址
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
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
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')
if __name__ == '__main__':
    app.run(port=5000, debug=True)  # 生产环境禁用debug模式

