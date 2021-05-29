# Yolov3 detection

## Yolo: Real-Time object detection
[Yolo description source.](https://pjreddie.com/darknet/yolo/)

You only look once (YOLO) is a state-of-the-art, real-time object detection system. 
On a Pascal Titan X it processes images at 30 FPS and has a mAP of 57.9% on COCO test-dev.


YOLOv3 is extremely fast and accurate. In mAP measured at .5 IOU YOLOv3 is on par with Focal Loss but about 4x faster. 

Moreover, you can easily tradeoff between speed and accuracy simply by changing the size of the model, no retraining required!

## Modules
Before starting, usage of a virtual environment is advised via the venv module:
```bash
$ python3 -m venv envname # to create the virtual env
$ source envname/bin/activate # activate it
$ deactivate # when done
```

For ease of use, the [yolo34py](https://pypi.org/project/yolo34py/) Python module was used, which is a wrapper on the YOLO 3.0 implementation by [pjreddie](https://pjreddie.com/).

To install yolo34py, first install:
```bash
$ python3 -m pip install requests cython numpy opencv-python
```

For the CPU only version:
```bash
$ python3 -m pip install yolo34py
```

For the GPU version:
```bash
$ python3 -m pip install yolo34py-gpu
```

Download the base model files:
```bash
$ bash ./init/download_models.sh
```
If need be:
```bash
$ chmod u+x ./init/download_models.sh
```

## Test yolov34py
```bash
$ python3 test_yolov34py.py
```

## Using yolov3-tiny
Download the yolov3-tiny model files:
```bash
$ wget -O weights/yolov3-tiny.weights https://pjreddie.com/media/files/yolov3-tiny.weights
$ wget -O cfg/yolov3-tiny.cfg https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3-tiny.cfg
```
Change `Detector(...)` parameters in `test_yolo34.py` to `yolov3-tiny.cfg` and `yolov3-tiny.weights`

## Datasets
The test image `assets/PennPed00001.png` is from the [Penn-Fudan database.](https://www.cis.upenn.edu/~jshi/ped_html/)

## Pip freeze
Example of working module versions. `$ python3 -m pip freeze`:
```bash
certifi==2020.12.5
chardet==4.0.0
Cython==0.29.23
idna==2.10
numpy==1.20.3
opencv-python==4.5.2.52
requests==2.25.1
urllib3==1.26.5
yolo34py==0.2
```
Tested on `Archlinux 5.12.7-arch1-1`, python version `Python 3.9.5`
