FROM python:3.9-alpine

WORKDIR /usr/src/app

ADD . .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /data/log

CMD [ "python", "./app.py" ]

EXPOSE 5000