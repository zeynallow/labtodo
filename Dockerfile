FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /labtodo
WORKDIR /labtodo
COPY requirements.txt /labtodo/
RUN pip install -r requirements.txt
COPY . /labtodo/