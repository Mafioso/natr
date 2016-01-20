FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /natr
WORKDIR /natr
RUN apt-get update && apt-get install -y build-essential python-dev && rm -rf /var/lib/apt/lists/*
ADD ./requires.txt /natr/
RUN pip install -r requires.txt
RUN pip install uwsgi
ADD . /natr