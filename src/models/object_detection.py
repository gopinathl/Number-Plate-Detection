import os, shutil
import os
import requests
import cv2
import numpy as np
import json

class ObjectDetection:
    def __init__(self):
        self.img_dir = r'/home/dell/Desktop/Number Plate Detection/Data_Folder/car images'
        img = os.listdir(self.img_dir)
        self.img_path = os.path.join(self.img_dir, img[0])
        self.bb_path = r'/home/dell/Desktop/Number Plate Detection/Data_Folder/annotations'

        self.HOST = 'localhost'  # Edit this if using a remote host to serve the model
        self.MODEL = 'effdet1'  # Use 'rfcn' for R-FCN or 'ssd-mobilenet' for SSD-MobileNet
        self.SERVER_URL = 'http://{}:8501/v1/models/{}:predict'.format(self.HOST, self.MODEL)

    def format_results(self, output_dict):
        result_dict = {}

        num_detections = int(output_dict['num_detections'])
        result_dict['num_detections'] = num_detections
        result_dict['detection_boxes'] = np.array(output_dict['detection_boxes'])[:num_detections, :]
        #result_dict['detection_classes'] = np.array(output_dict['detection_classes'])[:num_detections].astype(np.uint8)
        result_dict['detection_scores'] = np.array(output_dict['detection_scores'])[:num_detections][0]

        return result_dict


    def get_detections(self, image_np):
        predict_request = '{"instances" : %s}' % np.expand_dims(image_np, 0).tolist()
        result = requests.post(self.SERVER_URL, data=predict_request)
        detections = self.format_results(result.json()['predictions'][0])

        return detections

    def denormalize_coordinates(self, detections,h,w):
        boxes=[]
        for box in detections['detection_boxes']:
            y_min = int(box[0] * h)
            x_min = int(box[1] * w)
            y_max = int(box[2] * h)
            x_max = int(box[3] * w)
            box = [x_min, y_min, x_max, y_max]
            boxes.append(box)
        detections['detection_boxes'] = box

        return detections

    def run_model(self):

        img = cv2.imread(self.img_path)
        image_np = np.array(img)
        height, width = image_np.shape[:2]
        detections = self.get_detections(image_np)
        detections = self.denormalize_coordinates(detections, height, width)
        return detections

    def main(self):
        ded_boxes=self.run_model()
        with open(self.bb_path+'/data.json', 'w') as f:
            json.dump(ded_boxes, f)
        #print(ded_boxes)

