FROM python:3.8-alpine3.13

MAINTAINER Ivan Buneev

RUN apk update
RUN apk add --no-cache python3-dev \
                       build-base \
                       libc6-compat \
                       libffi-dev \
                       zlib-dev \
                       musl-dev \
                       jpeg-dev \
                       procps \
                       libressl-dev \
                       gcc \
                       cargo \
                       libxslt-dev \
                       libxml2-dev \
                       openssl-dev \
                       linux-headers
                       
RUN mkdir /code
WORKDIR /code
RUN pip3 install --upgrade pip

ADD requirements.txt /code/
RUN pip3 install -r requirements.txt --no-cache-dir
ADD . /code/

WORKDIR /code/src

ENV PYTHONUNBUFFERED=1
ENV DEBUG=0

CMD ["python3", "server.py"]

