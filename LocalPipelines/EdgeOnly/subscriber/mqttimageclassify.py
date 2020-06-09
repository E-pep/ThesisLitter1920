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
import csv

## GUI #######################################################################################################################

# Import required libraries
import pickle
import copy
import pathlib
import math
import datetime as dt

#global GUI variable
latl = []
lonl = []

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s')


# CSV file for writing stuff away
csvFile = open("test.csv", 'w')
writer = csv.writer(csvFile)
writer.writerow(["ImageID", "Latitude", "Longitude", "AfterReadIn", "AfterPrediction"])
csvFile.flush()
broker="mqtt"

#port
port=1883



def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc), flush=True)
	client.subscribe("/data")


def on_message(client, userdata, message):
    tempString = str(message.payload.decode("utf-8"))
    y = json.loads(tempString)
    latl.append(y["Latitude"])
    lonl.append(y["Longitude"])
    # print("message received", flush=True)
    stamps = json.loads(y["Timestamps"])
    print(stamps[0], flush=True)
    print(stamps[1], flush=True)
    writer.writerow([y["ImageID"], y["Latitude"], y["Longitude"], stamps[0]["Time"], stamps[1]["Time"]])
    csvFile.flush()


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
    # app.run_server(host= '0.0.0.0',debug=True, port=8050)
    while True:
        time.sleep(1)







