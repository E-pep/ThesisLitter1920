FROM python:3.6

RUN pip3 install dash==1.8.0
RUN pip3 install pandas==0.24.2
RUN pip3 install gunicorn==19.9.0

COPY data /
COPY assets /assets/
RUN pip3 install redis
EXPOSE 8050
ADD PlotlyInterface.py /
CMD ["python3","./PlotlyInterface.py"]