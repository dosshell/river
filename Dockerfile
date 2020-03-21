# Use an official Python runtime as a parent image
FROM python:3.6-slim-stretch

WORKDIR /app/src

COPY ./src /app/src
COPY ./dep /app/dep

RUN python -m pip install pipenv
RUN python -m pipenv sync

ENTRYPOINT ["pipenv", "run", "python", "-u", "river.py"]
