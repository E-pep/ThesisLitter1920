FROM cloudbaseimage
COPY model1_MobileV2 /
RUN pip install redis
ADD CloudOnlySubscriber.py /
RUN ls
CMD ["./CloudOnlySubscriber.py"]