FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /natr
WORKDIR /natr
ADD ./requires.txt /natr/
RUN pip install -r requires.txt
ADD . /natr