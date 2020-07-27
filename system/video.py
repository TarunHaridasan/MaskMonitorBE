#Imports
from camera.detection import Detection
import cv2

#Video class that managers and camera and polls for frames
class Video():
    #This method is used to instantiate the object of this class
    def __init__(self, source):
        self.cam = Detection(source)
        self.frame = None
        self.faces = []

    #This method is used to start polling for frames
    def start(self):
        while (True):
            #Capture each frame
            self.cam.getFrame()

            #Detect the faces in the frame
            self.faces = self.cam.detectFaces()

            #Save the resulting frame for multiple clients to access
            self.frame = self.cam.frame

            '''
            #show frame (debugging)
            cv2.imshow("Window",self.frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):                
                return self.stop() 
            '''

    #This method is used to stop polling for frames
    def stop(self):
        self.cam.release() #release camera
        self.cam.destroyAll() #destroy any opencv windows 