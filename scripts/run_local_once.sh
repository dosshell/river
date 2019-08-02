#!/bin/bash

MY_PATH="`dirname \"$0\"`"
cd $MY_PATH/../src

python3 -m pip install pipenv
python3 -m pipenv install --ignore-pipfile
python3 -m pipenv run python daemon.py --now -c ../settings.json
