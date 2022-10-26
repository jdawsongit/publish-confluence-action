FROM python:3.10-slim-buster

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN pip install requests pycmarkgfm

WORKDIR /action
COPY ./src .

ENTRYPOINT [ "python" ]
CMD [ "/action/main.py" ]
