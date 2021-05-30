import cv2

from yolov4.tf import YOLOv4

yolo = YOLOv4()

yolo.config.parse_names("coco.names")
yolo.config.parse_cfg("config/yolov4-tiny.cfg")

yolo.make_model()
yolo.load_weights("weights/yolov4-tiny.weights", weights_type="yolo")
yolo.summary(summary_type="yolo")
yolo.summary()

yolo.inference(media_path="test.jpg")
