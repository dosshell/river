# Use an official Python runtime as a parent image
FROM python:3.6-slim-stretch

WORKDIR /app

COPY ./src /app

# RUN apk add tzdata gcc build-base
# libpng-dev freetype-dev jpeg-dev libstdc++ gcc build-base python3-dev musl-dev freetype libpng
RUN python -m pip install pipenv
RUN python -m pipenv sync

# Make port 80 available to the world outside this container
# EXPOSE 80

# Define environment variable
# ENV NAME World

ENTRYPOINT ["pipenv", "run", "python", "-u", "daemon.py"]
