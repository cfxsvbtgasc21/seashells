from pathlib import Path
import move_results
index_map={
    0:"鲍鱼",
    1:"钉螺",
    2:"海虹",
    3:"海螺",
    4:"扇贝",
    5:"生蚝",
    6:"缢蛏",
    7:"青柳蛤",
    8:"白贝",
    9:"象拔蚌",
    10:"北极贝",
    11:"毛钳"
}
from ultralytics import YOLO
import cv2
if __name__ == '__main__':
    model=YOLO("./best.pt",task="detect")
    results=model.predict(source="./test_pictures/1.jpg",save=True,project='runs/detect',
        name='exp')
    yolov8_results_dir = 'runs/detect/exp'
    base_save_path = r'E:\Py_project\ultralytics-main\ultralytics-main\results'
    move_results.save_yolov8_results(Path(yolov8_results_dir), base_save_path)
    for result in results:
        boxes = result.boxes.xyxy  # 边界框坐标
        scores = result.boxes.conf  # 置信度分数
        classes = result.boxes.cls  # 类别索引
        class_names = [index_map[int(cls)] for cls in classes]
        for box, score, class_name in zip(boxes, scores, class_names):
            print(f"Class: {class_name}, Score: {score:.2f}, Box: {box}")