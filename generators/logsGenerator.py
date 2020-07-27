import time
import cv2
import base64
import json

#This generator periodically sends log data to the client(s)
def logsGenerator(camera):
    #while True:
    if len(camera.faces)>0:
        for face in camera.faces:
            #Convert image to base64
            buffer = cv2.imencode(".jpg", face[0])[1]
            encoded = base64.b64encode(buffer).decode("utf-8")
            
            #Get mask status on face
            isMask = int(face[1])

            #Format the JSON string
            data = json.dumps({"image": encoded, "isMask": isMask})
            yield(data)
    else:
        yield('{}')
    