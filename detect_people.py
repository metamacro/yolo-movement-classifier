import glob
import os
import cv2
import numpy as np

from yolov4.tf import YOLOv4
from tracking.sort import *

yolo = YOLOv4()
mot_tracker = Sort()

yolo.config.parse_names("coco.names")
yolo.config.parse_cfg(os.path.join("config", "yolov4.cfg"))

yolo.make_model()
yolo.load_weights(os.path.join("weights", "yolov4.weights"), weights_type="yolo")

yolo.summary(summary_type="yolo")
yolo.summary()

# get raw images
imgs = [yolo.resize_image(cv2.imread(img)) 
        for img in sorted(glob.glob("frames/*.jpg"))]

LEN_TOTAL_FRAMES = len(str(len(imgs)))
PERSON_ID = 0

for nframe, img in enumerate(imgs):
    # all dimension parameters are scaled [0, 1] relative to the image size
    idx = {name: i for i, name in enumerate(('x', 'y', 'w', 'h', 't', 'p'))}
    # detect, filter only people
    people_bboxes = [bbox for bbox in yolo.predict(img, prob_thresh=0.5) 
                     if bbox[idx['t']] == PERSON_ID]

    # convert from scaled  parameter dimensions [0, 1] to a np array of top left, bottom left  [px]
    def scaled2bbox(bbox, X, Y):
        res = np.array((X, Y))
        topl = (res * (np.array(bbox[:2]) - np.array(bbox[2:4]) * 0.5))
        botr = (res * (np.array(bbox[:2]) + np.array(bbox[2:4]) * 0.5))
        return np.concatenate((topl, botr)).astype(np.int32)

    X, Y, _ = np.shape(img)
    # convert to rect format
    rect_bboxes = [list(scaled2bbox(bbox, X, Y))+[bbox[-1]] for bbox in people_bboxes]

    # update the tracker, can be ran without args if speed is an issue, quality should drop
    track_bboxes_ids = mot_tracker.update(np.array(rect_bboxes))

    # drawing rects, text
    for bbox in track_bboxes_ids:
        if np.isnan(bbox).any(): continue

        topl = list(map(int, bbox[:2]))
        botr = list(map(int, bbox[2:4]))
        pid = int(bbox[-1])

        img = cv2.rectangle(img, 
                            topl, 
                            botr, 
                            (255, 0, 0), 
                            2)

        cv2.putText(img,
                    f"person {pid}", 
                    topl,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.45,
                    (255, 0 ,0),
                    2)

    cv2.imwrite(os.path.join("out", f"frame{nframe:0{LEN_TOTAL_FRAMES}}.jpg"), img)

cv2.destroyAllWindows()
