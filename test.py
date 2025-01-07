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

        # annotated_img = result.plot()

        # 显示图像
        #cv2.imshow('Detected Image', annotated_img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        # print(result.boxes.cls)
        # print(index_map[result.boxes.cls])
    # print(results)
    # 对单个图像进行预测并保存结果
    # im1 = Image.open("bus.jpg")
    # results = model.predict(source=im1, save=True)  # save plotted images

    # get_save_dir()里改生成的识别图片路径 Path对象

    # 对图像数组进行预测

    # im2 = cv2.imread("bus.jpg")
    # results = model.predict(source=[im1, im2], save=True, save_txt=True)  # 保存预测图像和标签

    # 对视频或实时摄像头进行预测
    # results = model.predict(source="0")  # 0 代表摄像头
