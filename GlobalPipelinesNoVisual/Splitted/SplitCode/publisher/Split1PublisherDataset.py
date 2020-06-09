import numpy as np
# import pytz
import tensorflow as tf
import socket

print("Why different sendtimes publisher224")
print(socket.gethostname(),flush=True)

import cv2
import time
import paho.mqtt.client as paho
import logging
import base64
import json
# import tensorflow_hub as hub
from tensorflow.keras import layers
from datetime import datetime

gpu_devices = tf.config.experimental.list_physical_devices('GPU')
for device in gpu_devices:
    tf.config.experimental.set_memory_growth(device, True)


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
IMAGE_SHAPE = (224, 224)
class_names = ['litter', 'non-litter']
model = tf.keras.models.load_model('FirstModel4_224')

# MQTT global variables
broker = "3.92.192.135"
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

    # model klaarstomen:

    imgString = '1.jpg'
    img = cv2.imread(imgString, 1)

    # Resize image for prediction
    img = cv2.resize(img, IMAGE_SHAPE)
    img = np.array(img) / 255.0

    # predict and add class
    result = model.predict(img[np.newaxis, ...])

    predicted_class = np.argmax(result[0], axis=-1)


    client.loop_start()
    for i in range(1, 41):
        # Read in image
        imgString = str(i) + '.jpg'
        img = cv2.imread(imgString, 1)

        # Make object to convert to JSON: start timestamp
        data = DataSend(x, i, 42, 12)
        Timestampsl.addTimestamp("AfterReadIn", datetime.now().time())

        # Resize image for prediction
        img = cv2.resize(img, IMAGE_SHAPE)
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

    while True:
        test = 1

    client.loop_stop()
    client.disconnect()