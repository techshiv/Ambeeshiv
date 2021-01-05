FROM python:3.7

ADD maintry.py .

RUN pip3 install requests Flask paho-mqtt Flask-SocketIO Flask-PyMongo dnspython
RUN apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
#RUN sudo sudo apt-get update
#RUN sudo apt-get install mosquitto mosquitto-clients

CMD ["python3","./maintry.py"]