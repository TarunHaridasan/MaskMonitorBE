#Imports
from flask import Flask, Response
import time
import threading

#Import systems scripts
from system.video import Video

#Import generators (video and logs)
import generators

#Initialize the camera on seperate thread
camera = Video(0)
t1 = threading.Thread(target=camera.start)

#Initialize Flask server on seperate thread
app = Flask(__name__)
t2 = threading.Thread(target = app.run, kwargs = {"host":"192.168.2.24", "port":5000})

#Routes
@app.route("/video-feed")
def index():
    return Response(generators.videoGenerator(camera),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/video-logs")
def logs():
    return Response(generators.logsGenerator(camera), mimetype="application/json")

@app.route("/status")
def status():
    return "Success"
    
#Start threads
t1.start()
print("[INFO] Camera Started!")
t2.start()
print("[INFO] Server Started!")