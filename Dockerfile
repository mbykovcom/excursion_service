FROM python:3.7

RUN mkdir -p /usr/src/app
COPY .. /usr/src/app
WORKDIR /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80