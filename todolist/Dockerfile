FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /labtodo
WORKDIR /labtodo
ADD requirements.txt /labtodo/
RUN pip install -r requirements.txt
ADD . /labtodo/
