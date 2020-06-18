# FROM rpibaseimage2
# FROM nano-cv-tf-mqtt
FROM cloudbaseimage
COPY model1_MobileV2 /
COPY ThesisTestPicturesSetSmall /
ADD video_15-37.mp4 /
ADD video_15-37.xml /
RUN ls
ADD edgeonlymqttimagepublisher.py /
CMD ["./edgeonlymqttimagepublisher.py"]
