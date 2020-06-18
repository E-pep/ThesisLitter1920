import numpy as np
import time
import PIL.Image as Image
import matplotlib. pyplot as plt
import paho.mqtt.client as mqtt
import logging
import base64
import json
from datetime import datetime
import pytz
import csv
import redis

print("160 model, edgeonly with visuals")

logging.basicConfig(format='%(asctime)s %(message)s',filename='timings.log',level=logging.DEBUG)


# CSV file for writing stuff away
csvFile = open("test.csv", 'w')
writer = csv.writer(csvFile)
writer.writerow(["SenderID","ImageID", "Latitude", "Longitude", "AfterReadIn", "AfterPrediction", "Received"])
csvFile.flush()



broker="mqtt"

#port
port=1883

# config for redis

redisPublisher = redis.Redis(host="redis", port=6379, db=0)



def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc), flush=True)
	client.subscribe("/data")


def on_message(client, userdata, message):
    tempString = str(message.payload.decode("utf-8"))
    print("received: ", flush=True)
    y = json.loads(tempString)
    stamps = json.loads(y["Timestamps"])
    stamps.append({'StampName': 'Received', 'Time': str(datetime.now())})
    # logging.info('SenderID: %s \t ImageID: %s \t Predicted: %s \t Latitude: %s \t Longitude: %s \t AfterReadIn: %s \t AfterPrediction: %s \t Received: %s ', y["SenderID"], y["ImageID"], y["Litter"], y["Latitude"], y["Longitude"], stamps[0]["Time"], stamps[1]["Time"], stamps[2]["Time"])

# Send over to visual container using Redis
    print(str(y["SenderID"]), flush=True)
    print(str(y["Latitude"]), flush=True)
    print(str(y["Longitude"]), flush=True)

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
    time.sleep(1)


