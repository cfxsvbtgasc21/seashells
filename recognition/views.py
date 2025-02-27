from flask import Flask, render_template, request, redirect, send_from_directory, url_for, jsonify
import flask
import image_recognition as im
from werkzeug.utils import secure_filename
import os
# from app import index_map,UPLOAD_FOLDER
UPLOAD_FOLDER = 'static/uploads'# 原始图片上传到的相对路径
directory = 'uploads/' # 识别结果存储的相对路径
from . import rec
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
@rec.route('/', methods=['POST', 'GET'])
def hello_world():
    if flask.request.method == 'GET':
        return render_template("index.html")
@rec.route('/sub', methods=['POST', 'GET'], endpoint='sub')
def red():
    return redirect(url_for('rec.home'))
@rec.route('/home', methods=['POST', 'GET'])
def home():
    if flask.request.method == 'GET':
        return render_template("sub.html")
    else:
        # 添加CSRF保护检查
        if not flask.request.referrer or not flask.request.referrer.startswith(request.host_url):
            return {"error": "非法请求来源"}, 403

        if 'image' not in request.files:
            return {"error": "没有上传文件"}, 400

        file = request.files['image']
        if not file or not file.filename:
            return {"error": "没有选择文件"}, 400

        # 验证文件类型和大小
        if not allowed_file(file.filename):
            return {"error": "不支持的文件类型"}, 400

        try:
            filename = secure_filename(file.filename)
            # 确保上传目录存在
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            # 生成随机文件名以防止文件名冲突
            file_extension = os.path.splitext(filename)[1]
            filename = f"{os.urandom(16).hex()}{file_extension}"

            file_path = os.path.join(UPLOAD_FOLDER, filename)

            # 验证文件路径
            if not os.path.abspath(file_path).startswith(os.path.abspath(UPLOAD_FOLDER)):
                return {"error": "非法文件路径"}, 400

            file.save(file_path)
            results = im.image_rec(file_path)
            sub_results = im.get_subimage(results, file_path, "static/" + directory, filename)  # 返回图片地址名称
            recognition_results = im.get_image_info(results, index_map)
            flask.session['recognition_results'] = recognition_results
            flask.session['sub_results'] = sub_results
            return redirect(url_for('rec.process', filename=filename))
        except Exception as e:
            rec.logger.error(f"上传失败: {str(e)}")
            return {"error": "服务器处理失败"}, 500


@rec.route('/process/<filename>')
def process(filename):
    try:
        global directory
        full_path = directory + filename
        recognition_results = flask.session.get('recognition_results', [])
        sub_results = flask.session.get('sub_results', [])
        d = 'static/' + directory
        allfiles = [d + f for f in sub_results]
        allfiles.append(d + filename)
        print(filename, directory, sub_results, full_path, recognition_results, allfiles, "\n")
        return render_template('image_display.html',
                               file_name=filename,
                               base_path=directory,
                               sub_results=sub_results,
                               image_path=full_path,
                               image_info=recognition_results,
                               files_to_delete=allfiles
                               )
    except Exception as e:
        return render_template('image_display.html', image_data=None, error=str(e))


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}  # 移除了gif支持，因为可能存在安全风险
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@rec.route('/delete_files', methods=['POST'])
def delete_files():
    data = request.json
    file_paths = data.get('file_paths', [])  # 获取需要删除的文件路径列表

    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
                print(f"Deleted: {file_path}")
            else:
                print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
    return jsonify({"status": "success"})

