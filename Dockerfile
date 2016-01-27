FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /natr
WORKDIR /natr
RUN apt-get update && apt-get install -y libpq-dev build-essential python-dev && rm -rf /var/lib/apt/lists/*
ADD ./requires.txt /natr/
ADD ./requires_dev.txt /natr/
RUN pip install -r requires.txt
RUN pip install -r requires_dev.txt
ADD . /natr