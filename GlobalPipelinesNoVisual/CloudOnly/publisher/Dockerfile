FROM rpibaseimage2
# FROM nano-cv-tf-mqtt
# FROM cloudbaseimage
# RUN pip install pytz
# RUN pip install --upgrade tensorflow-hub
COPY ThesisTestPicturesSetSmall /
ADD CloudOnlyPublisher.py /
CMD ["./CloudOnlyPublisher.py"]