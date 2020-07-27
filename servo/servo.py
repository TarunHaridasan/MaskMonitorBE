from gpiozero import Servo
from time import sleep
import requests

servo = Servo(17)

while True:
    response = requests.get('http://127.0.0.1:5000/video-logs')
    response = response.json()
    if response:
        if response['isMask']:
            print('A mask was detected!')
            servo.min()
            sleep(2)
            servo.max()
            sleep(2)
        else:
            print('NO mask was detected!')
    sleep(3)
