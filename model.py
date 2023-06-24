from numpy.ma.core import shape
import random
import numpy as np
import tensorflow as tf
from keras.datasets import mnist
from keras.datasets import fashion_mnist
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense 
import matplotlib.pyplot as plt 
from keras import layers
from keras import Sequential
from keras.models import  model_from_json
import cv2        


 # load json and create model
json_file = open('files/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("files/model.h5")
print("Loaded model from disk")

def getpic(filename):
        img = cv2.imread(filename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        rectangles = [cv2.boundingRect(c) for c in contours]
        sorted_rectangles = sorted(rectangles, key=lambda r: r[2]*r[3], reverse=True)
        # max_rect = max(rectangles, key=lambda r: r[2]*r[3])
        sorted_rectangles = sorted(rectangles, key=lambda r: r[2]*r[3], reverse=True)
        max_rects = sorted_rectangles[:2]
        img_address=[]
        for i, rect in enumerate(max_rects):
          x, y, w, h = rect
          center_x = x + w/2
          center_y = y + h/2
          # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
          # cv2.circle(img, (int(center_x), int(center_y)), 5, (0, 0, 255), -1)

          # برش  مستطیل
          cropped = img[y:y+h, x:x+w]
          
          cv2.imwrite(f'Imagederect{i}.png', cropped)
          img_address.append(f'Imagederect{i}.png')
        
        return img_address

def addborder(filename):
          img = cv2.imread(filename)
          height, width, _ = img.shape
          border_size = 85
          border_color = (0, 0, 0)
          img_with_border = cv2.copyMakeBorder(img, border_size, border_size, border_size, border_size, cv2.BORDER_CONSTANT, value=border_color)
          
          cv2.imwrite(f"{filename}", img_with_border)
          return f"{filename}"

def make_square(image_path, square_size=440):
    img = cv2.imread(image_path)
    height, width, _ = img.shape
    if height == width:
        return img
    elif height > width:
        top_bottom = height - width
        top = top_bottom // 2
        bottom = top_bottom - top
        img_with_border = cv2.copyMakeBorder(img, top, bottom, 0, 0, cv2.BORDER_CONSTANT, None, value=[0, 0, 0])
    else:
        left_right = width - height
        left = left_right // 2
        right = left_right - left
        img_with_border = cv2.copyMakeBorder(img, 0, 0, left, right, cv2.BORDER_CONSTANT, None, value=[0, 0, 0])
    resized_img = cv2.resize(img_with_border, (square_size, square_size))
    cv2.imwrite("resize.png",resized_img)
    return "resize.png"

def testmodel(filename):
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (28, 28))
    img = img.astype('float32') / 255.0
    img = img.reshape(1, 28*28)
    pred = loaded_model.predict(img)
    print(np.argmax(pred))
    class_names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    pred_class_name = class_names[np.argmax(pred)]
    print('Predicted class:', pred_class_name)
    return pred_class_name