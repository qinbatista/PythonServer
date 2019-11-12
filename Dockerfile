FROM python:3.7.4

WORKDIR /usr/src/lukseun

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./start_servers.py" ]
