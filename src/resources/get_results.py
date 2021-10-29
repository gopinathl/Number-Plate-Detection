# coding=utf-8
import os, shutil

import io
from base64 import encodebytes
from PIL import Image

from src.models.object_detection import ObjectDetection
from src.models.paddle_ocr import PlatePaddleOCR


class GetResultsResource:
    def __init__(self):
        self.output_images_path = r'/home/dell/Desktop/Number Plate Detection/Data_Folder/output images'

    def get_response_image(self, image_path):
        pil_img = Image.open(image_path, mode='r') # reads the PIL image
        byte_arr = io.BytesIO()
        pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
        encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
        return encoded_img

    def get(self):
        
        #Run object dedection
        objdet = ObjectDetection()
        objdet.main()

        #Run OCR
        pad = PlatePaddleOCR()
        license_plate_text = pad.main()
        if license_plate_text is None:
            license_plate_text = "License Plate is not visible!"


        ##reuslt  contains list of path images
        result = os.listdir(self.output_images_path)
        dest = r'/home/dell/Desktop/Number Plate Detection/static/output'
        try:
            os.mkdir(dest)
        except:
            for res in result:
                shutil.copy(os.path.join(self.output_images_path, res), os.path.join(dest, res))

        return license_plate_text, result

    
    def post(self):
        data_folder_path = r'/home/dell/Desktop/Number Plate Detection/Data_Folder'
        folders = ['annotations','car images','plate images','output images']
        folders_list = [os.path.join(data_folder_path,folder)for folder in folders]
        for folder in folders_list:
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))