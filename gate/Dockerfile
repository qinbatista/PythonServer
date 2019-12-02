FROM python:3.7-alpine

RUN apk add build-base libffi-dev openssl-dev

WORKDIR /usr/src/gate

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

STOPSIGNAL SIGINT

EXPOSE 8201
EXPOSE 8880

#CMD [ "python", "-u", "./gate.py" ]
