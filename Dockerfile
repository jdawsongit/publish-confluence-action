FROM python:3.10-slim-buster

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

WORKDIR /tmp
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /action
COPY ./src .

ENTRYPOINT [ "python" ]
CMD [ "/action/main.py" ]
