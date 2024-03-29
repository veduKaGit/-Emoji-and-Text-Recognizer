# -*- coding: utf-8 -*-
"""captcha-solver-letters-submitted

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nSaNjTNB9jizHQVM2KfsW59k3s6rtiEG
"""

import cv2
import os  #to interact with os => perform directory management
import segmentation as seg  #segmentation.py => saved in the mosaic folder in drive => download it and use
from tensorflow.keras.models import load_model
import numpy as np

from google.colab import drive
drive.mount('/content/drive')

model_text = load_model('/content/drive/My Drive/model_only_letters_byclass_1.h5',compile=True) #emnist letters
model_emoji = load_model('/content/drive/My Drive/with_bitwise_and_thresh.h5',compile=True) #without aug

classes='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def predict(image):
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)  #coloured 2 grayscale
    img_paths = seg.extract_character(image)  #get numpy array of individual images after segmentation
    output = ' '

    for i in img_paths:
        m = []
        flag = 0
        img = cv2.imread(i,cv2.IMREAD_GRAYSCALE)  # i is image path, IMREAD_GRAYSCALE means it will be read in grayscale
        img = cv2.bitwise_not(img)                #invert pixels => white/black
        img = np.reshape(img,(28,28,1))/255       # (28*28*1) dimensions => 1 channel, /255 since normalize in range [0,1]
        m.append(img)
        m = np.array(m)
        result = np.argmax(model_text.predict(m))  #result => assigned INDEX of class with highest predicted probability
        predictions = model_text.predict(m)  #predictions=> assigned the OUTPUT from model
        p_max = np.amax(predictions)  #value of the max probability


        if(p_max<0.95):
          result = np.argmax(model_emoji.predict(m))   #if model_txt is working poor => take model_emoji
          predictions = model_emoji.predict(m)
          flag = 1
          
        if (flag==0):
          output += classes[result]
        else:
          output += classes[result+1]   #since mapping in emojis is from 1
    return output


def test():
      image_paths=['/content/drive/MyDrive/mosaic/818.jpg']
      for i in image_paths:
          image=cv2.imread(i)
          captcha_decoded = predict(image)
          print(captcha_decoded)

      image_paths=['/content/drive/MyDrive/mosaic/811.jpg']
      for i in image_paths:
          image=cv2.imread(i)
          captcha_decoded = predict(image)
          print(captcha_decoded)
      

if __name__=='__main__':
    test()
