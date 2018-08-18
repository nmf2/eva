FROM python:3.5-slim-stretch

RUN apt-get update

RUN apt-get install -y gcc

RUN mkdir -p /tmp

COPY requirements.txt /tmp/

RUN cd /tmp \
    && pip3 install --no-cache-dir -r requirements.txt

COPY . /tmp/

RUN cd /tmp \
    && python3 setup.py install

RUN rm -rf /tmp

RUN python -m nltk.downloader punkt stopwords
