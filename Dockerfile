FROM python:3.9.13

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apt-get update && pip install -r ./requirements.txt

RUN mkdir /app
COPY . /app
WORKDIR /app
EXPOSE 5000

CMD ["python", "api.py"]