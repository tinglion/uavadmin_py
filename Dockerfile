FROM python:3.12
# FROM python:3.11-slim
# FROM ubuntu:18.04

WORKDIR /app
COPY ./hello.py ./

RUN apt update
RUN apt-get install vim wget curl git default-mysql-client -y

# --no-cache-dir
# RUN pip install -r requirements.txt

CMD exec python hello.py 
