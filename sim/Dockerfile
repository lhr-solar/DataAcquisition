FROM python:3.9-slim-buster AS base

RUN apt-get update
RUN apt-get install -y gcc

COPY ./ /telemetry
EXPOSE 65433

CMD [ "python3", "-u", "main.py" ]
