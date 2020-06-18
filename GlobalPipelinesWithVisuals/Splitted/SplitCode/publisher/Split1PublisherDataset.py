import numpy as np
# import pytz
import tensorflow as tf

import cv2
import time
import paho.mqtt.client as paho
import logging
import base64
import json
# import tensorflow_hub as hub
from tensorflow.keras import layers
from datetime import datetime
import xml.etree.ElementTree as ET
import math
import socket

# ----------------------------------------      Turn on for the Jetson Nano ------------------------------------------------------------------

gpu_devices = tf.config.experimental.list_physical_devices('GPU')
for device in gpu_devices:
    tf.config.experimental.set_memory_growth(device, True)

print("Start GlobalVisualPublisher Splitted", flush=True)

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


# class for our timestamp for timing info
class Timestamp:
    def __init__(self, StampName, Time):
        self.StampName = StampName
        self.Time = Time


class DataSend:
    def __init__(self,SenderID, ImageID, Latitude, Longitude):
        self.SenderID = SenderID
        self.ImageID = ImageID
        self.Latitude = Latitude
        self.Longitude = Longitude

    def addIntermediateResult(self, IntermediateResult):
        self.IntermediateResult = IntermediateResult

    def addTimestamp(self, Stampstring):
        self.Timestamps = Stampstring

class TimestampList:
    def __init__(self):
        self.Timestamps = []

    def addTimestamp(self, StampName, Time):
        self.Timestamps.append(Timestamp(StampName, str(Time)))

    def clearList(self):
        self.Timestamps = []


# logger for debugging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s')

# tensorflow variables
IMSHOW_SIZE = (700, 500)
IMAGE_SHAPE = (160, 160)
class_names = ['litter', 'non-litter']
model = tf.keras.models.load_model('FirstModel10')

# MQTT global variables
broker = "54.172.14.181"
# port
port = 1883


def on_publish(client, userdata, result):
    logger.warning("Device 1 : Data published.")
    pass

x= str(socket.gethostname())
if __name__ == "__main__":
    client = paho.Client(x)
    client.on_publish = on_publish
    connectioncheck = client.connect(broker, port)
    print("Setting up connection of Publisher", flush=True)

    Timestampsl = TimestampList()
    time.sleep(20)

    client.loop_start()
    cap = cv2.VideoCapture('video_15-37.mp4')
    framecounter = 0
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            neededframe = math.floor(framecounter / 30)
            # Read in image
            # Make object to convert to JSON: start timestamp
            data = DataSend(x, framecounter, x_loclist[neededframe], y_loclist[neededframe])
            Timestampsl.addTimestamp("AfterReadIn", datetime.now().time())

            # Resize image for prediction
            img = cv2.resize(frame, IMAGE_SHAPE)
            img = np.array(img) / 255.0

            # predict and add class
            IntermediateResult = model.predict(img[np.newaxis, ...])
            data.addIntermediateResult(IntermediateResult.tolist())
            Timestampsl.addTimestamp("AfterPredictionSubmodel1", datetime.now().time())

            # Convert to JSON
            jsonFormatTimestampsl = json.dumps([ob.__dict__ for ob in Timestampsl.Timestamps])
            data.addTimestamp(jsonFormatTimestampsl)
            jsonFormatData = json.dumps(data.__dict__)
            # telemetry to send
            message = jsonFormatData
            # publish message
            client.publish("/data", message)
            Timestampsl.clearList()
            framecounter += 1
            cv2.waitKey(30)

    while True:
        test = 1

    client.loop_stop()
    client.disconnect()