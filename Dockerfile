FROM python:3.9.13-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apk update && apk add gcc musl-dev python3-dev libffi-dev openssl-dev cargo \
&& pip install --upgrade pip \
&& pip install -r ./requirements.txt

WORKDIR /app
COPY . /app

EXPOSE 5000

CMD ["python", "api.py"]