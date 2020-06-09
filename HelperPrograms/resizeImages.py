from PIL import Image
import os
import sys

directory = "/home/paul/Documents/Thesis/Thesis19-20/Praktisch/docker_files/ThesisTestPicturesSet"
smalldir = "/home/paul/Documents/Thesis/Thesis19-20/Praktisch/docker_files/ThesisTestPicturesSetSmall/"

for file_name in os.listdir(directory):
  print("Processing %s" % file_name)
  image = Image.open(os.path.join(directory, file_name))

  x,y = image.size
  new_dimensions = (640, 480)
  output = image.resize(new_dimensions, Image.ANTIALIAS)

  output_file_name = os.path.join(smalldir + file_name)
  output.save(output_file_name, "JPEG", quality = 95)

print("All done")