import os
import shutil
from datetime import datetime
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')
from ultralytics import YOLO

#
# def get_next_folder(base_path):
#     # 获取当前日期
#     date_str = datetime.now().strftime('%Y%m%d')
#
#     # 获取所有以当前日期开头的目录
#     existing_folders = [f for f in os.listdir(base_path) if f.startswith(date_str)]
#
#     # 提取编号并找到下一个编号
#     if existing_folders:
#         existing_numbers = [int(f[-4:]) for f in existing_folders]
#         next_number = max(existing_numbers) + 1
#     else:
#         next_number = 1
#
#     # 生成下一个目录名称
#     next_folder_name = f"{date_str}{next_number:04d}"
#
#     return next_folder_name
#
#
# def merge_label_files(labels_folder, output_file):
#     # 打开输出文件，以追加模式
#     with open(output_file, 'a') as out_file:
#         # 遍历 labels 文件夹中的所有 .txt 文件
#         for filename in os.listdir(labels_folder):
#             if filename.endswith('.txt'):
#                 # 读取当前 .txt 文件的内容
#                 with open(os.path.join(labels_folder, filename), 'r') as label_file:
#                     content = label_file.read()
#                 # 将内容写入输出文件
#                 out_file.write(content)


def save_yolov8_results(results_dir, base_save_path):
    # 基本路径
    base_path = Path(base_save_path)
    base_path.mkdir(exist_ok=True)
    # 创建子目录 "检测后图片"
    images_folder =Path(base_save_path)
    # 将YOLOv8的结果移动到新目录中的子目录
    for item in os.listdir(results_dir):
        source = os.path.join(results_dir, item)
        destination = images_folder / item
        shutil.move(source, destination)
    shutil.rmtree(results_dir)