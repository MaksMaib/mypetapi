FROM python:3.10
FROM pytorch/pytorch:1.12.0-cuda11.3-cudnn8-runtime

RUN mkdir -p /docker-fastapi

WORKDIR /docker-fastapi
COPY . /docker-fastapi
RUN pip install -r requirements-docker.txt
