#Imports
import numpy as np
import cv2
from camera.baseCamera import BaseCamera

#Detection class inherites the Base Camera class
class Detection(BaseCamera):
    #This function is used to instantiate the objects of this class
    def __init__(self, source):
        super().__init__(source)

        #Load the pretrained caffe models #D:\Windows\Downloads\codeathonBackend\camera\\
        self.net = cv2.dnn.readNetFromCaffe(".\camera\\faceData\deploy.prototxt", ".\camera\\faceData\\res10_300x300_ssd_iter_140000.caffemodel")
        self.maskNet = cv2.dnn.readNetFromCaffe(".\camera\maskData\deploy.prototxt", ".\camera\maskData\\face_mask.caffemodel")

        #Color constants
        self.red = (0, 0, 255)
        self.green = (0, 255, 0)

    #This function finds faces in the current frame
    def detectFaces(self):       
        #Resize images
        resizedFrame = cv2.resize(self.frame, (300, 300))

        #Pass image through network to recieve detections 
        blob = cv2.dnn.blobFromImage(resizedFrame, 1.0, (300, 300), (104.0, 177.0, 123.0), swapRB=False, crop=False)
        self.net.setInput(blob)
        detections = self.net.forward()

        faces = []

        #Loop through all detections  Detection = [batchId, classId, confidence, left, top, right, bottom]
        for detection in detections[0, 0]: 
            #Get confidence levels of each detection
            confidence = detection[2]

            #Filter out weak false detections
            if confidence < 0.3:
                continue

            #Compute the boundary box 
            box = detection[3: 7]
            left = int(box[0] * self.w)
            top = int(box[1] * self.h)
            right = int(box[2] * self.w)
            bottom = int(box[3] * self.h)

            #Crop the face out            
            face = self.frame[top-20:bottom+20, left-20:right+20].copy() #Might have to remove

            isMask = False
            message = None
            color = self.red

            #Check if a mask exists on the face and dray the text
            if face.size > 0:
                #Detect mask and show message
                isMask, message, color = self.detectMask(face)
                faces.append([face, isMask])
                cv2.putText(self.frame, message, (left, bottom+30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            #Draw box around face
            cv2.rectangle(self.frame, (left, top), (right, bottom), color, 3)
            #text = "Confidence: {:.2f}%".format(confidence * 100)
            #cv2.putText(self.frame, text, (left, top-20), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        return faces

    #This function is used to detect masks
    def detectMask(self, frame):
        #Preprocessing
        frame = cv2.resize(frame, (224, 224))      
        meanValues = (127.5, 127.5, 127.5)
        blob = cv2.dnn.blobFromImage(frame, 1, (224, 224), meanValues)
        
        #Pass image through the network
        self.maskNet.setInput(blob)
        detections = self.maskNet.forward("fc5")

        #Check if mask or not
        prob = detections[0]
        thresholdValue = -0.3
        if prob[0]>thresholdValue:
            return (True, "Mask Detected", self.green) #Face mask seen
        else:
            return (False, "No Mask Detected", self.red) #No face mask