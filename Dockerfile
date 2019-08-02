# Use an official Python runtime as a parent image
FROM python:3.7-alpine

WORKDIR /app

COPY ./src /app

RUN apk add tzdata
RUN python -m pip install pipenv
RUN python -m pipenv install --ignore-pipfile

# Make port 80 available to the world outside this container
# EXPOSE 80

# Define environment variable
# ENV NAME World

ENTRYPOINT ["pipenv", "run", "python", "-u", "daemon.py"]
