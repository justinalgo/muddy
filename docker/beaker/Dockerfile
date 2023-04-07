FROM python:alpine

WORKDIR /usr/src/app

RUN pip install --no-input virtualenv && virtualenv venv && source venv/bin/activate

COPY docker/beaker/src/requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt
