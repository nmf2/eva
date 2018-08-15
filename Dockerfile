FROM python:3.6-slim-stretch

RUN apt-get update

RUN apt-get install gcc -y

RUN mkdir -p /tmp

WORKDIR /tmp

COPY . /tmp/

RUN pip3 install -r requirements.txt

RUN python3 setup.py install

WORKDIR /

RUN rm -rf /tmp
