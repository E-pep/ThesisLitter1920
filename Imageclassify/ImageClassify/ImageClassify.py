import numpy as np
import tensorflow as tf
print(tf.__version__)
import cv2
import time
import PIL.Image as Image
import matplotlib. pyplot as plt

import tensorflow_hub as hub

from tensorflow.keras import layers
IMSHOW_SIZE = (700, 500)
IMAGE_SHAPE = (160, 160)
class_names = ['litter','non-litter']





model = tf.keras.models.load_model('1586456756')
#model.summary()

#test_image = tf.keras.utils.get_file('image.jpg','https://interactive-examples.mdn.mozilla.net/media/examples/grapefruit-slice-332-332.jpg')
#test_image = Image.open(test_image).resize(IMAGE_SHAPE)

# img = cv2.imread('litter3.jpg',1)
# drawing = cv2.resize(img,IMSHOW_SIZE)
#
# img = cv2.resize(img,IMAGE_SHAPE)
# img = np.array(img)/255.0
#
# result = model.predict(img[np.newaxis, ...])
# print('resulting shape:',result.shape)
#
# predicted_class = np.argmax(result[0], axis=-1)
# print('predicted_class:',predicted_class)
# predicted_class
#
# #drawing on the image
#
#
#
# # Write some Text
# font = cv2.FONT_HERSHEY_SIMPLEX
#
#
# if predicted_class == 0:
#   print("litter detected!")
#   cv2.putText(drawing, 'litter detected!', (0,80), font, 3, (0, 0, 255), 6, cv2.LINE_AA)
#
# else:
#   print("no litter detected")
#   cv2.putText(drawing, 'no litter detected', (0,80), font, 3, (0, 255, 0), 6, cv2.LINE_AA)



# cv2.imshow('image', drawing)
# k = cv2.waitKey(0)
#
# if k == 27:
#   cv2.destroyAllWindows()





if __name__ == "__main__":
  cap = cv2.VideoCapture('video_15-37.mp4')


  while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
      drawing = cv2.resize(frame, IMSHOW_SIZE)

      frame = cv2.resize(frame, IMAGE_SHAPE)
      frame = np.array(frame) / 255.0

      result = model.predict(frame[np.newaxis, ...])
      print('resulting shape:', result.shape)

      predicted_class = np.argmax(result[0], axis=-1)
      print('predicted_class:', predicted_class)
      predicted_class

      if predicted_class == 0:
        print("litter detected!")
        cv2.putText(drawing, 'litter detected!', (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 6, cv2.LINE_AA)
      else:
        print("NO litter detected!")
        cv2.putText(drawing, 'NO litter detected!', (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 6, cv2.LINE_AA)
      cv2.imshow('image', drawing)
      # Press Q on keyboard to  exit
      if cv2.waitKey(25) & 0xFF == ord('q'):
        break
    # Break the loop
    else:
        break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
