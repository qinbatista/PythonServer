FROM python:3.7-alpine

RUN apk add build-base libffi-dev openssl-dev

WORKDIR /usr/src/config

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

STOPSIGNAL SIGINT

EXPOSE 8000

#CMD [ "python", "-u", "./configuration_manager.py" ]
