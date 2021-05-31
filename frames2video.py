import cv2
import glob

frames_path_glob = "out/*.jpg"
imgs = [cv2.imread(img) for img in sorted(glob.glob(frames_path_glob))]
height, width, layers = imgs[0].shape

# 23 fps, movie experience :)
video = cv2.VideoWriter("video.avi", 0, 23, (width, height))

for img in imgs:
    video.write(img)

cv2.destroyAllWindows()
video.release()
