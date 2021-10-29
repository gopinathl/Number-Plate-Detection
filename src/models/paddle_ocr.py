from paddleocr import PaddleOCR, draw_ocr # main OCR dependencies
from matplotlib import pyplot as plt # plot images
import cv2 #opencv
import os # folder directory navigation
import glob
import numpy as np # linear algebra
import json
from PIL import Image # to read images
import re

class PlatePaddleOCR:
    def __init__(self):
        self.image_path = r'/home/dell/Desktop/Number Plate Detection/Data_Folder/car images'
        self.annotation_path = r'/home/dell/Desktop/Number Plate Detection/Data_Folder/annotations'
        self.plate_path = r'/home/dell/Desktop/Number Plate Detection/Data_Folder/plate images'
        self.paddle_ocr_font_path = os.path.join(r'/home/dell/Desktop/Number Plate Detection/Data_Folder/fonts', 'latin.ttf')
        self.output_images_path = r'/home/dell/Desktop/Number Plate Detection/Data_Folder/output images'

    def bounding_box(self):
        with open(self.annotation_path + '/data.json') as json_file:
            data = json.load(json_file)
            xmin = data['detection_boxes'][0]
            ymin = data['detection_boxes'][1]
            xmax = data['detection_boxes'][2]
            ymax = data['detection_boxes'][3]
            
        return (xmin, ymin, xmax, ymax)

    def extract_plate(self):
        all_images = [_ for _ in os.listdir(self.image_path) if _.endswith('.png') or _.endswith('.jpg') or _.endswith('.jpeg')]
        image_path = [os.path.join(self.image_path, image) for image in all_images][0]
        if image_path is not None:
            bbox = self.bounding_box()
            im = Image.open(image_path)
            im = im.crop(bbox)
            save_path = os.path.join(self.plate_path, image_path.split('/')[-1])
            im.save(save_path)
            
            #save image with bounding box
            img = cv2.imread(image_path) 

            # reorders the color channels
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
            start_point = (bbox[0], bbox[1]) 
            end_point = (bbox[2], bbox[3]) 
            
            # Blue color in BGR 
            color = (255, 0, 0) 
            
            # Line thickness of 2 px 
            thickness = 2
            
            # Using cv2.rectangle() method 
            # Draw a rectangle with blue line borders of thickness of 2 px 
            bb_image = cv2.rectangle(img, start_point, end_point, color, thickness)
            cv2.imwrite(os.path.join(self.output_images_path,'car_bb.png'), bb_image)

            return save_path
        else:
            return None

    def extract_plate_text(self, image_path):
        # Setup model
        ocr_model = PaddleOCR(lang='en', use_angle_cls=True)
        
        # Run the ocr method on the ocr model
        result = ocr_model.ocr(image_path)
        
        # Extracting detected components
        boxes = [res[0] for res in result] 
        texts = [res[1][0] for res in result]
        scores = [res[1][1] for res in result]

        # imports image
        img = cv2.imread(image_path) 

        # reorders the color channels
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
        
        # draw annotations on image
        annotated = draw_ocr(img, boxes, texts, scores, font_path=self.paddle_ocr_font_path)
        cv2.imwrite(os.path.join(self.output_images_path,'plate_bb.png'), annotated)
        return texts

    def post_proc_ocr(self, texts):
        #Join multiple lines of of number plate text
        if len(texts) > 1:
            license_plate_text = ' '.join(texts)
        elif len(texts) ==0:
            license_plate_text = None
        else:
            license_plate_text = texts[0]

        #Remove special characters
        if license_plate_text is not None:
            text = ''
            for k in license_plate_text.split("\n"):
                text+= re.sub(r"[^a-zA-Z0-9]+", ' ', k)
            license_plate_text = text
        
        return license_plate_text

    def main(self):
        
        license_plate_text = "Number Plate not Found !"
        save_path = self.extract_plate()
        if save_path is not None:
            texts = self.extract_plate_text(save_path)
        if save_path is not None and texts is not None:
            license_plate_text = self.post_proc_ocr(texts)
            #print("Number Plate: ", license_plate_text)

        return license_plate_text
    

