# FROM rpibaseimage2
# FROM nano-cv-tf-mqtt
FROM cloudbaseimage
ADD edgeonlymqttimagepublisher.py /
COPY model1_MobileV2 /
COPY ThesisTestPicturesSetSmall /
RUN ls
CMD ["./edgeonlymqttimagepublisher.py"]
