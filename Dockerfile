FROM python:3

ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Bishkek

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app/
