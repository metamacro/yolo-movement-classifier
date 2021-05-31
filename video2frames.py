import os
import sys
import argparse

import cv2

def extract_frames(vidpath, framespath):
    vidcap = cv2.VideoCapture(vidpath)
    # za usporedbu sa nframes
    TOTAL_FRAMES = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    # za padding s 0 prilikom spremanja, onda je slike lako sortirat po imenu
    LEN_TOTAL_FRAMES = len(str(TOTAL_FRAMES))

    success, image = vidcap.read()
    nframes = 0
    while success:
        cv2.imwrite(os.path.join(framespath, f"frame{nframes:0{LEN_TOTAL_FRAMES}}.jpg"), image)
        success, image = vidcap.read()

        nframes +=1

    # mora se broj frameova podudarat, inace: FUGGG :DDD
    return nframes if nframes == TOTAL_FRAMES else -1

if __name__ == "__main__":
    """
    Primjer koristenja:
       $ python3 main.py --vidpath video.mp4 --framespath frames/
    """
    a = argparse.ArgumentParser()
    a.add_argument("--vidpath", help="Path to the video.")
    a.add_argument("--framespath", help="Path to the extracted frames.")

    args = a.parse_args()
    print(args)

    print(extract_frames(args.vidpath, args.framespath))
    
