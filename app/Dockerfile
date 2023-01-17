FROM python:3.9-slim-buster AS base

RUN apt-get update
RUN apt-get install -y gcc

COPY ./ /app
RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt
EXPOSE 65432

CMD [ "python3", "-u", "main.py" ]
