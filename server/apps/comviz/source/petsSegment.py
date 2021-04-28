
import os
workpath = os.path.dirname(os.path.abspath(__file__))

import random


from IPython.display import Image, display
from tensorflow.keras.preprocessing.image import load_img
import PIL
from PIL import ImageOps

import numpy as np
import numpy.random as rnd

import cv2

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import load_img

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
rnd.seed(1973)
np.set_printoptions(suppress=True)


class PetsSegmentor:
    def __init__(self):
        
        os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
        physical_devices = tf.config.experimental.list_physical_devices('GPU')
        assert len(physical_devices) > 0, "Not enough GPU hardware devices available"
        config = tf.config.experimental.set_memory_growth(physical_devices[0], True)
        keras.backend.clear_session()
        self.img_size = (160, 160)
        self.model = keras.models.load_model(os.path.join(workpath,"oxford_segmentationv1.h5"), custom_objects={'LeakyReLU': layers.LeakyReLU})

    def predictor(filename):
        imgp = PIL.Image.open(filename).convert('RGB').resize(self.img_size, PIL.Image.BICUBIC)
        imgnp = np.array(imgp)
        y = self.model.predict(imgnp[np.newaxis])[0]
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        ax1.imshow(imgnp, interpolation='nearest')
        ax2.imshow(y, interpolation='nearest')
    
    def predictorWeb(self, imgp):
        imgnp = np.array(imgp)
        y = self.model.predict(imgnp[np.newaxis])[0]
        y = cv2.normalize(y, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        return y


    def segment(self, mirror=False):
        cam = cv2.VideoCapture(0)
        while True:
            ret_val, img = cam.read()
            if mirror: 
                img = cv2.flip(img, 1)
            img = cv2.resize(img, (160, 160), interpolation = cv2.INTER_CUBIC)
            
            imgp = self.predictorWeb(img)
            #cv2.imshow('my webcam1', img)
            cv2.imshow('my webcam2', imgp)
            
            #break
            if cv2.waitKey(1) == 27: 
                break  # esc to quit
        cv2.destroyAllWindows()


def main():
    pob = PetsSegmentor()
    pob.segment()

#main()




