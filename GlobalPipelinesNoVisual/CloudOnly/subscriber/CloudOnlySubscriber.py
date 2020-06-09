import numpy as np
# import pytz
import tensorflow as tf
print(tf.__version__)
import cv2
import time
import paho.mqtt.client as mqtt
import logging
import base64
import json
from datetime import datetime
import csv

print("stomme zendtijd ResizeOnEdge")

from tensorflow.keras import layers
IMAGE_SHAPE = (224, 224)
class_names = ['litter','non-litter']

logging.basicConfig(format='%(asctime)s %(message)s',filename='timings.log',level=logging.DEBUG)

imagesource = np.zeros(shape=(693,1200))

model = tf.keras.models.load_model('1588534373')
broker="mqtt"

#port
port=1883


# CSV file for writing stuff away
csvFile = open("test.csv", 'w')
writer = csv.writer(csvFile)
writer.writerow(["SenderID","ImageID", "IsLitter", "Latitude", "Longitude", "AfterReadIn", "AfterImageEncode","Received" ,"AfterPrediction"])
csvFile.flush()



def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc), flush=True)
	client.subscribe("/data")


def on_message(client, userdata, message):
    start = datetime.now().time()
    tempString = str(message.payload.decode("utf-8"))
    #print(tempString, flush=True)

    y = json.loads(tempString)
    stamps = json.loads(y["Timestamps"])
    stamps.append({'StampName': 'Received', 'Time': str(datetime.now().time())})

    img2 = base64.b64decode(y["ImageData"])
    buf_arr = np.fromstring(img2, dtype=np.uint8)
    imagesource = cv2.imdecode(buf_arr, cv2.IMREAD_UNCHANGED)
    # imagesource = cv2.resize(imagesource, IMAGE_SHAPE)
    imagesource = np.array(imagesource) / 255.0
    result = model.predict( imagesource[np.newaxis, ...])
    predicted_class = np.argmax(result[0], axis=-1)
    stamps.append({'StampName': 'AfterPrediction', 'Time': str(datetime.now().time())})
    stop = datetime.now().time()
    logging.info('SenderID: %s \t ImageID: %s \t Predicted: %s \t Latitude: %s \t Longitude: %s \t AfterReadIn: %s \t AfterImageEncode: %s \t Received: %s \t AfterPrediction: %s', y["SenderID"], y["ImageID"], predicted_class, y["Latitude"], y["Longitude"], stamps[0]["Time"], stamps[1]["Time"], stamps[2]["Time"], stamps[3]["Time"])

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