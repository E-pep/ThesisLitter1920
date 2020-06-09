#FROM tensorflow/tensorflow:nightly-py3
FROM fnndsc/ubuntu-python3:latest
RUN apt-get update
RUN apt-get install -y libsm6 libxext6 libxrender-dev
RUN pip install --upgrade pip
RUN pip install scikit-image
RUN pip install opencv-python==3.4.8.29
RUN pip install paho-mqtt
RUN pip install tf-nightly-cpu

    # Replace 0 with your user / group id
    RUN export uid=1000 gid=1000
    RUN mkdir -p /home/developer
    RUN echo "developer:x:${uid}:${gid}:Developer,,,:/home/developer:/bin/bash" >> /etc/passwd
    RUN echo "developer:x:${uid}:" >> /etc/group
    RUN echo "developer ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
    RUN chmod 0440 /etc/sudoers
    RUN chown ${uid}:${gid} -R /home/developer
ADD mqttimagepublisher.py /
COPY streetlitter.jpg /
COPY car.jpg /
COPY litter3.jpg /
COPY video_15-37.mp4 /
COPY video_15-37.xml /
RUN ls
CMD ["./mqttimagepublisher.py"]
