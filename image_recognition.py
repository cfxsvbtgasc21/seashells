from pathlib import Path
from ultralytics import YOLO
import move_results
from PIL import Image
import os
def image_rec(path):
    model = YOLO("./best.pt", task="detect")
    results = model.predict(source=path, save=True, project='runs/detect',
                            name='exp')
    yolov8_results_dir = 'runs/detect/exp'
    base_save_path = r'uploads'
    move_results.save_yolov8_results(Path(yolov8_results_dir), base_save_path)
    return results

def get_subimage(results, path, save_path, filename):
    file_names = []  # 创建一个空列表来存储文件名
    for result_index, result in enumerate(results):
        boxes = result.boxes.xyxy  # 边界框坐标
        image_path = path
        image = Image.open(image_path)
        for box_index, box in enumerate(boxes):
            x1, y1, x2, y2 = map(int, box)
            # 裁剪图像区域
            cropped_image = image.crop((x1, y1, x2, y2))
            # 为每个裁剪的图像生成唯一的文件名
            unique_filename = f"{filename}_{result_index}_{box_index}{Path(filename).suffix}"
            # 保存裁剪后的图像
            cropped_image.save(os.path.join(save_path, unique_filename))
            file_names.append(unique_filename)
        # 关闭图像以释放资源
        image.close()
    return file_names

def get_image_info(results,index_map):
    recognition_results = list()
    for result in results:
        scores = result.boxes.conf  # 置信度分数
        classes = result.boxes.cls  # 类别索引
        class_names = [index_map[int(cls)] for cls in classes]
        for score, class_name in zip( scores, class_names):
            recognition_results.append(f"{class_name} (置信度: {score:.2f})")
    return recognition_results
