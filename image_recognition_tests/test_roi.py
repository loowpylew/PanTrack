from asyncio.windows_events import NULL
from cv2 import VideoCapture
import pytesseract
import cv2
# Importing Image class from PIL module
from PIL import Image
from os import walk
import pandas as pd
import os, os.path
from pathlib import Path
import colorama 
import numpy as np 
from pynput.keyboard import  Controller
from cv2 import cvtColor

pytesseract.pytesseract.tesseract_cmd ="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
config = 'digits'

image = cv2.imread("roi.jpg")
img_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # pytesseract API only accepts image in RGB format 
         
# Tesseract options for txt format styles found within images: https://muthu.co/all-tesseract-ocr-options/
# Known as page segmentation (option 6: Assume a single uniform block of text)    
watermark_values = pytesseract.image_to_string(img_RGB, config ='--psm 4') 

print(watermark_values[0:3])

if watermark_values[0:3] == '60S':
    indication_flag = "Detected"
else: 
    indication_flag = "Not Detected"

print(indication_flag)

