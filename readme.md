# Movement classification

The goal of this project would be movement classification of people, in other words, walking (normal and fast) and running.

Yolov4 will be used for detection.

# Yolov4 detection

## Yolo: Real-Time object detection
You only look once (YOLO) is a state-of-the-art, real-time object detection system. 

Currently the most advanced YOLO version is YOLOv4 which provides optimal speed and accuracy for object detection, therefore it will be used.

## Modules
Before starting, usage of a virtual environment is advised via the venv module:
```bash
$ python3 -m venv envname # to create the virtual env
$ source envname/bin/activate # activate it
$ deactivate # when done
```

For ease of use, the [tensorflow-yolov4](https://pypi.org/project/yolov4/) Python module was used, which is a YOLOv4 implementation in TensorFlow 2. 
For further documentation refer to the [project wiki](https://wiki.loliot.net/docs/lang/python/libraries/yolov4/python-yolov4-about/)

To install tensorflow-yolov4 install:

Dependencies:
```bash
$ python3 -m pip install opencv-python tensorflow
```
Note: If TensorFlow Lite needs to be used, refer to the (project wiki)[https://wiki.loliot.net/docs/lang/python/libraries/yolov4/python-yolov4-about/] for further instructions.


TensorFlow YOLOv4:
```bash
$ python3 -m pip install yolov4
```

Download the `yolov4-tiny` and `yolov4` weights` from the project wiki [weights download section](https://wiki.loliot.net/docs/lang/python/libraries/yolov4/python-yolov4-about/#download-weights).


Test tensorflow-yolov4 with the provided default test image, change model config, weights based on the one used (default is yolov4-tiny).
```bash
$ python3 test.py
```

## Test results
KACAVIS runaway_walk_1.mp4 frame 1471 was used:
YOLOv4             |  YOLOv4-tiny
:-------------------------:|:-------------------------:
![Yolov4](assets/passaway_walk_1_frame1471_yolov4.png)  |  ![Yolov4-tiny](assets/passaway_walk_1_frame1471_yolov4-tiny.png)


## Dataset
[FER's](https://www.fer.unizg.hr/?) dataset [KACAVIS](http://kacavis.zemris.fer.hr/).`

Download the dataset:
```bash
wget -O dataset/crowd_simulation_dataset.zip  http://kacavis.zemris.fer.hr/datasets/Crowd_simulation_dataset_videos.zip
```

## Pip freeze
To get the used module versions, in other words `$ python3 -m pip freeze`, take a look at:
```bash
./pip_freeze.txt
```

Tested on `Archlinux 5.12.x-arch1-1`, python version `Python 3.9.5`

If working on Arch change `python3` to `python` everywhere.
