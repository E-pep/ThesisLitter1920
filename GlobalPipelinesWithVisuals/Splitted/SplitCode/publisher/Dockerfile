# FROM rpibaseimage2
FROM nano-cv-tf-mqtt
# FROM cloudbaseimage
RUN pip install pytz
RUN pip install --upgrade tensorflow-hub
COPY Models /
# COPY ThesisTestPicturesSetSmall /
COPY video_15-37.mp4 /
COPY video_15-37.xml /
RUN ls
ADD Split1PublisherDataset.py /
CMD ["./Split1PublisherDataset.py"]