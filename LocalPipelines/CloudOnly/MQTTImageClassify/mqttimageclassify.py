import numpy as np
import tensorflow as tf
print(tf.__version__)
import cv2
import time
import PIL.Image as Image
import matplotlib. pyplot as plt
import paho.mqtt.client as mqtt
import logging
import base64
import json
import tensorflow_hub as hub
from datetime import datetime
import csv
import redis

from tensorflow.keras import layers
IMSHOW_SIZE = (700, 500)
IMAGE_SHAPE = (160, 160)
class_names = ['litter','non-litter']

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s')
logging.basicConfig(filename='received.log',level=logging.DEBUG)

imagesource = np.zeros(shape=(1920,1080))

model = tf.keras.models.load_model('/1586456756')
broker="mqtt"

#port
port=1883


# config for redis

redisPublisher = redis.Redis(host="redis", port=6379, db=0)
# subscribe to classical music



def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc), flush=True)
	client.subscribe("/data")


def on_message(client, userdata, message):
    tempString = str(message.payload.decode("utf-8"))
    #print(tempString, flush=True)

    y = json.loads(tempString)
    print("testen decode", flush=True)
    #print(y["ImageID"], flush=True)
    #y["Timestamps"].append({'StampName': 'test', 'Time': '2020-01-27 5152'})
    z = json.loads(y["Timestamps"])
    z.append({'StampName': 'Received', 'Time': str(datetime.now())})
    stringToSend = str(y["ImageID"]) + "," + str(y["Latitude"]) + "," + str(y["Longitude"])




    img2 = base64.b64decode(y["ImageData"])
    buf_arr = np.fromstring(img2, dtype=np.uint8)
    imagesource = cv2.imdecode(buf_arr, cv2.IMREAD_UNCHANGED)
    #
    #
    #
    # drawing = cv2.resize(imagesource, IMSHOW_SIZE)
    imagesource = cv2.resize(imagesource, IMAGE_SHAPE)
    imagesource = np.array(imagesource) / 255.0
    result = model.predict( imagesource[np.newaxis, ...])
    #
    #
    print('ImageID:', y["ImageID"], flush=True)
    #
    predicted_class = np.argmax(result[0], axis=-1)
    print('predicted_class:', predicted_class, flush=True)
    z.append({'StampName': 'AfterPrediction', 'Time': str(datetime.now())})

    if predicted_class == 0:
        redisPublisher.publish('mqtt_data', stringToSend)

    print(z,flush=True)
    logger.info(z)






    # predicted_class
    #
    # # Write some Text
    # font = cv2.FONT_HERSHEY_SIMPLEX
    #
    if predicted_class == 0:
        print("litter detected!", flush=True)
        # cv2.putText(drawing, 'litter detected!', (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 6, cv2.LINE_AA)
    #
    else:
        print("no litter detected", flush=True)
        # cv2.putText(drawing, 'no litter detected', (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 6, cv2.LINE_AA)
    #
    # cv2.imshow('image', drawing)
    # cv2.waitKey(25)



#start of our main loop --------------------------------------------------------------------------------------------

if __name__ == "__main__":

	broker_address = "mqtt"
	# broker_address="iot.eclipse.org"
	print("creating new instance", flush=True)
	client = mqtt.Client("P1")  # create new instance
	client.on_message = on_message  # attach function to callback
	print("connecting to broker", flush=True)
	client.connect(broker_address)  # connect to broker
	client.subscribe("/data")
	client.loop_start()  # start the loop
	print("Subscribing to topic", "/data", flush=True)

while True:
    time.sleep(1)





