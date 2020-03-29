# Use an official Python runtime as a parent image
FROM python:3.6-slim-stretch

WORKDIR /app

COPY ./src /app/src
COPY ./dep /app/dep
COPY ./scripts /app/scripts

RUN python -m pip install pipenv
RUN cd src && python -m pipenv sync

ENTRYPOINT ["/app/scripts/run_local.sh"]

