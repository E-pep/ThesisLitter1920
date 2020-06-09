# FROM rpibaseimage2
# FROM nano-cv-tf-mqtt
FROM cloudbaseimage
# RUN pip install pytz
# RUN pip install --upgrade tensorflow-hub
COPY Models /
COPY ThesisTestPicturesSetSmall /
RUN ls
ADD Split1PublisherDataset.py /
CMD ["./Split1PublisherDataset.py"]