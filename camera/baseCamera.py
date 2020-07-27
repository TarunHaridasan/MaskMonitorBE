#Imports
import numpy as np
import cv2
import time

#Base Camera Class
class BaseCamera():
    #This function is used to instantiate the objects of this class
    def __init__(self, source):
        self.cap = cv2.VideoCapture(source)
        self.frameSuccess, self.frame = self.cap.read()
        self.h = self.frame.shape[0] 
        self.w = self.frame.shape[1] 
        self.source = source            
        
    #This function is used to release the camera
    def release(self):
        self.cap.release()

    #This function is used to close all windows
    def destroyAll(self):
        cv2.destroyAllWindows()

    #This function extracts the current frame from the capture
    def getFrame(self):
        self.frameSuccess, self.frame = self.cap.read()
        return self.frame

    #This function displays the last extracted frame
    def showFrame(self):
        if self.frameSuccess:
            cv2.imshow(self.winName, self.frame)
        else:
            print("Error... Connection Lost?") 
