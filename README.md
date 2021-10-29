# Number-Plate-Detection

The massive integration of information technologies, under different aspects of the modern world, has led to the treatment of vehicles as conceptual resources in information systems. Since an autonomous information system has no meaning without any data, there is a need to reform vehicle information between reality and the information system.

This project helps detecting the number plates from vehicles of different countries and extracts the number plate text which can be used for commercial purposes. For this purpose, state-of-the art object detection and optical charater recognition algorithms are being used.

## Results

![results](https://user-images.githubusercontent.com/34036465/139430083-3772bf1f-cf2a-4b04-bc8a-d985eee641a8.png)

The first step is to identify where the number plate is present withing the input image (shown on the right) followed by extracting the text (shown on the right).

## Dataset
The dataset used for modelling is obtained from a kaggle competition. Link for which is mentioned below.

Dataset link: https://www.kaggle.com/andrewmvd/car-plate-detection

## Models used

1. Number Plate Detection: EfficientDet D1 640x640 model from the tensorflow object detection model zoo was used. Many other models such as SSDMobileNet, Faster RCNN was experimented with but the EfficientDet model proved to be more accurate and easily scalable 
     Model Zoo link : https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md
2. Optical Character Recognition: PaddleOCR is a ultra-light weight OCR model used by engineers of Baidu and trained on millions of images
     Paddle OCR repo: https://github.com/PaddlePaddle/PaddleOCR
     
## Installation

1. Install Tensorflow Object Detection API from the official documentation. Refer https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/install.html
2. Installation of other packages are included in the requirements.txt    
```bash
pip install -r requirements.txt
```
   For paddleOCR gpu version, refer https://www.paddlepaddle.org.cn/install/quick

## Running application
Setup the environment and run the following command:
```bash
python3 app.py
```
     
     
 

