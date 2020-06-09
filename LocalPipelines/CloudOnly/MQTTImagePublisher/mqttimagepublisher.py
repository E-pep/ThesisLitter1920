import numpy as np
import tensorflow as tf
print(tf.__version__)
import cv2
import time
import PIL.Image as Image
import matplotlib. pyplot as plt
import paho.mqtt.client as paho
import logging
import random
import base64
import json
from datetime import datetime
import xml.etree.ElementTree as ET
import math
import socket

class Timestamp:
    def __init__(self, StampName, Time):
        self.StampName = StampName
        self.Time = Time


class DataSend:
    def __init__(self, ImageID, Latitude, Longitude):
        self.ImageID = ImageID
        self.Latitude = Latitude
        self.Longitude = Longitude

    def addImageData(self, ImageData):
        self.ImageData = ImageData

    def addTimestamp(self, Stampstring):
        self.Timestamps = Stampstring

class TimestampList:
    def __init__(self):
        self.Timestamps = []

    def addTimestamp(self, StampName, Time):
        self.Timestamps.append(Timestamp(StampName, str(Time)))

    def clearList(self):
        self.Timestamps = []





logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s')


broker="mqtt"

#port
port=1883


def on_publish(client,userdata,result):
	logger.warning("Device 1 : Data published.")
	pass


# XML uitlezen

x_loclist =[]
y_loclist = []


tree = ET.parse('video_15-37.xml')
root = tree.getroot()

for x_loc in root.iter('x_loc'):
    print(x_loc.text)
    x_loclist.append(float(x_loc.text))


for y_loc in root.iter('y_loc'):
    y_loclist.append(float(y_loc.text))






if __name__ == "__main__":

    client = paho.Client("admin")
    client.on_publish = on_publish
    connectioncheck = client.connect(broker, port)
    print("Setting up connection of Publisher", flush=True)
    Timestampsl = TimestampList()
    time.sleep(10)

    cap = cv2.VideoCapture('video_15-37.mp4')
    framecounter = 0
    senderID = x= socket.gethostname()
    while (cap.isOpened()):
        # read in image
        ret, frame = cap.read()
        if ret == True:
            neededframe = math.floor(framecounter / 30)
            # Make object to convert to JSON: start timestamp
            data = DataSend(neededframe, x_loclist[neededframe], y_loclist[neededframe])
            Timestampsl.addTimestamp("AfterReadIn", datetime.now())

            retval, buffer = cv2.imencode('.png', frame)
            imagestring = base64.b64encode(buffer).decode('ascii')
            data.addImageData(imagestring)
            Timestampsl.addTimestamp("AfterImageEncode", datetime.now())

            # Convert to JSON

            jsonFormatTimestampsl = json.dumps([ob.__dict__ for ob in Timestampsl.Timestamps])
            data.addTimestamp(jsonFormatTimestampsl)
            jsonFormatData = json.dumps(data.__dict__)
            # telemetry to send
            message = jsonFormatData
            # publish message
            ret = client.publish("/data", message)
            Timestampsl.clearList()
            framecounter += 1
            cv2.waitKey(30)

    while (1):
        test =1





