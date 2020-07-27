import cv2

#This generator reads and sends frames to client as a byte array
def videoGenerator(camera):
    while (True):
        jpgData=cv2.imencode('.jpg', camera.frame)[1]
        stringData=jpgData.tostring()
        yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')



