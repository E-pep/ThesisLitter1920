FROM cloudbaseimage
COPY Models /
RUN pip install redis
ADD Split1SubscriberDataset.py /
CMD ["./Split1SubscriberDataset.py"]