import numpy as np
import cv2
import time
import paho.mqtt.client as paho
import logging
import random
import base64
import json
from datetime import datetime
import socket


print("stomme zendtijd ResizeOnEdge")
print(socket.gethostname(),flush=True)

class Timestamp:
    def __init__(self, StampName, Time):
        self.StampName = StampName
        self.Time = Time


class DataSend:
    def __init__(self, SenderID,ImageID, Latitude, Longitude):
        self.SenderID = SenderID
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


broker="54.90.196.140"

#port
port=1883


def on_publish(client,userdata,result):
	logger.warning("Device 1 : Data published.")
	pass



x= str(socket.gethostname())
IMAGE_SHAPE = (160, 160)

if __name__ == "__main__":

    client = paho.Client(x)
    client.on_publish = on_publish
    connectioncheck = client.connect(broker, port)
    print("Setting up connection of Publisher", flush=True)
    Timestampsl = TimestampList()
    time.sleep(20)
    client.loop_start()
    for i in range(1, 41):
        imgString = str(i) + '.jpg'
        img = cv2.imread(imgString, 1)
        img = cv2.resize(img, IMAGE_SHAPE)
        data = DataSend(x,i, 42, 12)
        Timestampsl.addTimestamp("AfterReadIn", datetime.now().time())

        retval, buffer = cv2.imencode('.jpg', img)
        imagestring = base64.b64encode(buffer).decode('ascii')
        data.addImageData(imagestring)
        Timestampsl.addTimestamp("AfterImageEncode", datetime.now().time())

        # Encapsulating data
        # Convert to JSON
        jsonFormatTimestampsl = json.dumps([ob.__dict__ for ob in Timestampsl.Timestamps])
        data.addTimestamp(jsonFormatTimestampsl)
        jsonFormatData = json.dumps(data.__dict__)
        # telemetry to send
        message = jsonFormatData
        # publish message


        ret = client.publish("/data", message)
        Timestampsl.clearList()

    while True:
        test = 1


    client.loop_stop()
    client.disconnect()