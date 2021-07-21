import argparse
import os
import numpy as np
import cv2

from yolov4.tf import YOLOv4
from tracking.sort import *
import math


class PeopleTracker:
    def __init__(self, coco="coco.names", 
                 config="config/yolov4-tiny.cfg",
                 weights="weights/yolov4-tiny.weights",
                 prob_thresh=0.3,
                 color=(224, 143, 83)): # BGR

        self.yolo = YOLOv4()

        self.yolo.config.parse_names(coco)
        self.yolo.config.parse_cfg(config)

        self.yolo.make_model()

        self.yolo.load_weights(weights, weights_type="yolo")

        self.yolo.summary(summary_type="yolo")
        self.yolo.summary()

        self.tracker = Sort()

        self.color = color

        self.prob_thresh = prob_thresh
        self.PERSON_ID = 0

    def relative_to_absolute_bbox(self, bbox, X, Y):
        '''
        yolov4 bounding boxes are scaled, in other words they are in the range 
        [0, 1] for both width and height, this method converts the bounding boxes
        to absolute pixel coordinates based on the image width, height (X, Y)
        '''
        res = np.array((X, Y))

        topl = (res * (np.array(bbox[:2]) - np.array(bbox[2:4]) * 0.5))
        botr = (res * (np.array(bbox[:2]) + np.array(bbox[2:4]) * 0.5))

        return list(topl) + list(botr)

    def predict(self, image):
        '''
        Detects people from a image, returns a list of bounding boxes along 
        with the prediction probability
        '''
        # resize to yolo detection format
        img = self.yolo.resize_image(image)

        # indices for the detections 
        idx = {name: i for i, name in enumerate(('x', 'y', 'w', 'h', 't', 'p'))}
        detections = self.yolo.predict(img, prob_thresh=self.prob_thresh)

        # filter people relative bbox coordinates ([0, 1] based on image width, height)
        people_rel = [person for person in detections
                      if person[idx['t']] == self.PERSON_ID and person[idx['h']] and person[idx['w']]]

        # convert to absolute pixel values - top left, bottom right bbox coordinates
        X, Y, _ = np.shape(img)
        people_abs = [self.relative_to_absolute_bbox(person[:4], X, Y)+[person[-1]]
                       for person in people_rel]

        return people_abs

    def draw_text(self, image, text, topl, scale=0.4):
        font = cv2.FONT_HERSHEY_SIMPLEX

        (text_width, text_height) = cv2.getTextSize(text, font, fontScale=scale, thickness=1)[0]

        # offsets based on person bouding box thickness and position
        off = (2, 4)
        box_coords = (
            (topl[0]-1, topl[1]+1), 
            (topl[0] + text_width + off[0], topl[1] - text_height - off[1])
        )

        cv2.rectangle(image, 
                      box_coords[0], 
                      box_coords[1], 
                      self.color, 
                      cv2.FILLED)

        cv2.putText(image, 
                    text, 
                    (topl[0], topl[1]-off[1]//2), # 
                    font,
                    fontScale=scale,
                    color=(255, 255, 255), 
                    thickness=1,
                    lineType=cv2.LINE_AA)
    
    def draw(self, image, people, thickness=2, font_scale=0.5):
        '''
        Draws bounding boxes and text based on the people list, returns a copy of the image with
        the drawn bounding boxes
        '''
        img = self.yolo.resize_image(np.array(image))

        npeople = 0
        for person in people:
            topl = tuple(map(int, person[:2]))
            botr = tuple(map(int, person[2:4]))

            img = cv2.rectangle(img,
                                topl,
                                botr,
                                self.color,
                                thickness)

            self.draw_text(img, f"Osoba {int(person[-1])}", topl)
            npeople += 1

        #self.draw_text(img, f"Broj osoba: {npeople}", (0, np.shape(img)[1]), scale=0.8)

        return img

    def update(self, image):
        # predict people bounding boxes with YOLOv4
        people = self.predict(image)

        # update the new bounding boxes with SORT
        #print(people)
        if len(people):
            tracked = self.tracker.update(np.array(people))

            # draw the text + bounding boxes
            drawn = self.draw(image, tracked)

            return drawn, tracked
        else:
            return self.yolo.resize_image(image), None


def area_calculation(present):
    x1, y1, x3, y3 = present
    x2, y2, x4, y4 = x1, y3, x3, y1
    a = x1 * y2 - y1 * x2
    b = x2 * y3 - y2 * x3
    c = x3 * y4 - y3 * x4
    d = x4 * y1 - y4 * x1
    return math.sqrt(abs((a + b + c + d) / 2))


def dist_calculation(present, past):
    return math.sqrt((present[0] - past[0]) ** 2 + (present[1] - past[1]) ** 2)


def classification(current, previous):
    count = 0
    if previous is not None and current is not None:
        for present in current:
            for past in previous:
                if present[4] == past[4]:
                    count += 1
                    #  TODO racunanje tu, prve 2 brojke su gornja tocka, druge 2 su donja tocka, 4. je ID
                    dist = dist_calculation(present[:4], past[:4])
                    area = area_calculation(present[:4])
                    print(dist / area)
        print(len(previous), len(current), count)
    print("One of two most recent frames is None")


if __name__ == "__main__":
    pplt = PeopleTracker()

    # get raw images
    imgs = [cv2.imread(img)
            for img in sorted(glob.glob("frames/*.jpg"))]

    LEN_TOTAL_FRAMES = len(str(len(imgs)))
    for nframe, img in enumerate(imgs):
        tracked, people = pplt.update(img)
        if nframe > 0:
            classification(people, previous)
        previous = people
        #cv2.imshow("Tracked", tracked)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        cv2.imwrite(os.path.join("out", f"frame{nframe:0{LEN_TOTAL_FRAMES}}.jpg"), tracked)

    '''
    # SINGLE IMAGE EXAMPLE
    # read the image based on the image name positional argument
    parser = argparse.ArgumentParser()
    parser.add_argument("imgname")

    args = parser.parse_args()

    img = cv2.imread(args.imgname)

    # initialize the people tracker
    pplt = PeopleTracker()

    # update the people tracker and grab the new image and people info (x, y, w, h, ID)
    tracked_img, people_info = pplt.update(img)

    cv2.imshow("Tracked", tracked_img)

    # wait, as in not to exit immediately, cleanup
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''

