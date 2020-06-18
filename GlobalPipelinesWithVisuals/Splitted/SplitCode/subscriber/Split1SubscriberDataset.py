import numpy as np
# import pytz
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

# print("visuals for splitted code", flush=True)

logging.basicConfig(format='%(asctime)s %(message)s',filename='timings.log',level=logging.DEBUG)
broker="mqtt"

#port
port=1883

# config for redis

redisPublisher = redis.Redis(host="redis", port=6379, db=0)


# load in the submodel
model = tf.keras.models.load_model('SecondModel10')

# CSV file for writing stuff away
# csvFile = open("test.csv", 'w')
# writer = csv.writer(csvFile)
# writer.writerow(["SenderID","ImageID", "IsLitter", "Latitude", "Longitude", "AfterReadIn", "AfterPredictionSubmodel1","Received" ,"AfterPrediction"])
# csvFile.flush()



def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc), flush=True)
	client.subscribe("/data")


def on_message(client, userdata, message):
    tempString = str(message.payload.decode("utf-8"))
    y = json.loads(tempString)
    print("received:", y["ImageID"], flush=True)
    IntermediateResult = np.array(y["IntermediateResult"])

    stamps = json.loads(y["Timestamps"])
    stamps.append({'StampName': 'Received', 'Time': str(datetime.now().time())})

    result = model.predict(IntermediateResult)
    predicted_id = np.argmax(result, axis=-1)
    stamps.append({'StampName': 'AfterPrediction', 'Time': str(datetime.now().time())})
    # writer.writerow([y["ImageID"], predicted_id, y["Latitude"], y["Longitude"], stamps[0]["Time"], stamps[1]["Time"], stamps[2]["Time"], stamps[3]["Time"]])
    # csvFile.flush()
    # logging.info('SenderID: %s \t ImageID: %s \t Predicted: %s \t Latitude: %s \t Longitude: %s \t AfterReadIn: %s \t AfterPredictionSubmodel1: %s \t Received: %s \t AfterPrediction: %s', y["SenderID"], y["ImageID"], predicted_id, y["Latitude"], y["Longitude"], stamps[0]["Time"], stamps[1]["Time"], stamps[2]["Time"], stamps[3]["Time"])
    if predicted_id == 0:
        # Send over to visual container using Redis
        # print(str(y["SenderID"]), flush=True)
        # print(str(y["Latitude"]), flush=True)
        # print(str(y["Longitude"]), flush=True)

        stringToSend = str(y["SenderID"]) + "," + str(y["Latitude"]) + "," + str(y["Longitude"])
        print("litter found!", flush=True)
        redisPublisher.publish('mqtt_data', stringToSend)

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
        time.sleep(1./30)