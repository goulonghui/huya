FROM python:3.6.5-slim

WORKDIR /usr/src/app

ADD . .

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /data/log

CMD [ "python", "./app.py" ]
#CMD [ "tail", "-f", "/etc/hosts" ]

EXPOSE 5000