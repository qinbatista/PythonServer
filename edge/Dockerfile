FROM python:3.7-alpine

RUN apk add build-base libffi-dev openssl-dev

WORKDIR /usr/src/edge

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY edge.py .

STOPSIGNAL SIGINT

EXPOSE 9000

#CMD [ "python", "-u", "./edge.py" ]
