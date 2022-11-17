FROM python:3.8

WORKDIR /app

COPY req.txt /app/req.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get  install -y libpq-dev \
                           postgresql \
                           postgresql-contrib \
                           netcat \
    && pip install --upgrade pip \
    && pip install -r /app/req.txt

COPY . /app/

RUN chmod +x /app/scripts/wait_db.sh
