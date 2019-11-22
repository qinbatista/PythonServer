FROM python:3.7-alpine

RUN apk add build-base libffi-dev openssl-dev

WORKDIR /usr/src/worker

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

STOPSIGNAL SIGINT

CMD [ "python", "-u", "./worker.py" ]
