import numpy as np
import tensorflow as tf

print(tf.__version__)
import cv2
import time
import PIL.Image as Image
import matplotlib.pyplot as plt
import paho.mqtt.client as paho
import logging
import random
import base64
import json
import tensorflow_hub as hub
import pprint
from tensorflow.keras import layers
from datetime import datetime


# class for our timestamp for timing info
class Timestamp:
    def __init__(self, StampName, Time):
        self.StampName = StampName
        self.Time = Time


class DataSend:
    def __init__(self, ImageID, Latitude, Longitude):
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
model = tf.keras.models.load_model('/1585347732first')

# MQTT global variables
broker = "mqtt"
# port
port = 1883


def on_publish(client, userdata, result):
    logger.warning("Device 1 : Data published.")
    pass


if __name__ == "__main__":
    client = paho.Client("admin")
    client.on_publish = on_publish
    connectioncheck = client.connect(broker, port)
    print("Setting up connection of Publisher", flush=True)

    Timestampsl = TimestampList()
    time.sleep(20)

    for i in range(20):
        # Read in image
        img = cv2.imread('litter3.jpg', 1)

        # Make object to convert to JSON: start timestamp
        data = DataSend(0, 42, 12)
        Timestampsl.addTimestamp("AfterReadIn", datetime.now())

        # Resize image for prediction
        drawing = cv2.resize(img, IMSHOW_SIZE)
        img = cv2.resize(img, IMAGE_SHAPE)
        img = np.array(img) / 255.0

        # predict and add class
        IntermediateResult = model.predict(img[np.newaxis, ...])
        print('Sender Intermediate size', IntermediateResult.shape, flush=True)
        data.addIntermediateResult(IntermediateResult.tolist())
        Timestampsl.addTimestamp("AfterPredictionSubmodel1", datetime.now())

        # Convert to JSON

        jsonFormatTimestampsl = json.dumps([ob.__dict__ for ob in Timestampsl.Timestamps])
        data.addTimestamp(jsonFormatTimestampsl)
        jsonFormatData = json.dumps(data.__dict__)
        # telemetry to send
        message = jsonFormatData
        # publish message
        ret = client.publish("/data", message)

        Timestampsl.clearList()

        # y = json.loads(jsonFormatData)
        # print("testen decode")
        # z = json.loads(y["Timestamps"])
        # print(z)












