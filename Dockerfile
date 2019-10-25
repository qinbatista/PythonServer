FROM ubuntu:latest

RUN apt-get update \
  && apt-get install -y python3.7 python3-pip \
  && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1 \
  && update-alternatives --config python3 \
  && python3 -V

COPY . /lukseun/

WORKDIR /lukseun

RUN ls -la

RUN python3 -m pip install -r requirements.txt

CMD ["python3", "start_servers.py"]
