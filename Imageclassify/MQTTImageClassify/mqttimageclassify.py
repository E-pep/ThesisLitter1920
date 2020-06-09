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

import tensorflow_hub as hub

from tensorflow.keras import layers
IMSHOW_SIZE = (700, 500)
IMAGE_SHAPE = (224, 224)
class_names = ['litter','non-litter']

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s')

imagesource = np.zeros(shape=(693,1200))

model = tf.keras.models.load_model('/1575372199')
broker="mqtt"

#port
port=1883



def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc), flush=True)
	client.subscribe("/data")


def on_message(client, userdata, message):
    tempString = str(message.payload.decode("utf-8"))
    print("message topic=", message.topic, flush=True)
    print("message qos=", message.qos, flush=True)
    print("message retain flag=", message.retain, flush=True)
    print(tempString[:80], flush=True)
    img2 = base64.b64decode(tempString)
    buf_arr = np.fromstring(img2, dtype=np.uint8)
    imagesource = cv2.imdecode(buf_arr, cv2.IMREAD_UNCHANGED)



    drawing = cv2.resize(imagesource, IMSHOW_SIZE)
    imagesource = cv2.resize(imagesource, IMAGE_SHAPE)
    imagesource = np.array(imagesource) / 255.0
    result = model.predict( imagesource[np.newaxis, ...])

    #ik geraak ni tot hier?????

    print('resulting shape:', result.shape, flush=True)

    predicted_class = np.argmax(result[0], axis=-1)
    print('predicted_class:', predicted_class, flush=True)
    predicted_class

    # Write some Text
    font = cv2.FONT_HERSHEY_SIMPLEX

    if predicted_class == 0:
       print("litter detected!")
       cv2.putText(drawing, 'litter detected!', (0, 80), font, 3, (0, 0, 255), 6, cv2.LINE_AA)

    else:
       print("no litter detected")
       cv2.putText(drawing, 'no litter detected', (0, 80), font, 3, (0, 255, 0), 6, cv2.LINE_AA)

    cv2.imshow('image', drawing)
    cv2.waitKey(25)



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





#     testimage = cv2.imread('streetlitter.jpg', 1)
#
#     drawing = cv2.resize(testimage, IMSHOW_SIZE)
#     testimage = cv2.resize(testimage, IMAGE_SHAPE)
#     testimage = np.array(testimage) / 255.0
#     result = model.predict(testimage[np.newaxis, ...])
#
# #ik geraak ni tot hier?????
#
#
#
# print('resulting shape:', result.shape, flush=True)
#
# predicted_class = np.argmax(result[0], axis=-1)
# print('predicted_class:', predicted_class, flush=True)
# predicted_class
#
# # Write some Text
# font = cv2.FONT_HERSHEY_SIMPLEX
#
# if predicted_class == 0:
#    print("litter detected!")
#    cv2.putText(drawing, 'litter detected!', (0, 80), font, 3, (0, 0, 255), 6, cv2.LINE_AA)
#
# else:
#    print("no litter detected")
#    cv2.putText(drawing, 'no litter detected', (0, 80), font, 3, (0, 255, 0), 6, cv2.LINE_AA)




while True:
    # cv2.imshow('image', drawing)
    # cv2.waitKey(25)
    time.sleep(1)





