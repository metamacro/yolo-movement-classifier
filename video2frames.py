import os
import sys

import cv2

def extract_frames(vidpath, framespath):
    vidcap = cv2.VideoCapture(vidpath)
    # for nframes comparison
    TOTAL_FRAMES = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    # for 0 padding, useful when reading data, easily sorted
    LEN_TOTAL_FRAMES = len(str(TOTAL_FRAMES))

    success, image = vidcap.read()
    nframes = 0
    while success:
        cv2.imwrite(os.path.join(framespath, f"frame{nframes:0{LEN_TOTAL_FRAMES}}.jpg"), image)
        success, image = vidcap.read()

        nframes +=1

    # if not: FUGGG :DDD
    return nframes if nframes == TOTAL_FRAMES else -1

if __name__ == "__main__":
    # example
    video_path = "dataset/runaway_1.mp4"
    frames_path = "frames/"

    print(extract_frames(video_path, frames_path))
    
