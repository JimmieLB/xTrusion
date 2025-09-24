FROM python:3.13-slim-bookworm


COPY ./requirements.txt ./opt/app/requirements.txt
WORKDIR /opt/app
RUN pip install -r ./requirements.txt
COPY . /opt/app

CMD python3 server.py