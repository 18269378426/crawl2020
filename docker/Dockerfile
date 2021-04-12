FROM python:3.6-slim-buster
COPY ./scrapyd.conf /etc/scrapyd/
EXPOSE 6800
WORKDIR /app
ADD requirements.txt /app
RUN pip install pip -U
RUN pip install -r requirements.txt

ADD . /app