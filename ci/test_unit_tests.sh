#!/bin/bash

MY_PATH="`dirname \"$0\"`"
cd $MY_PATH/../src

which pipenv

if [ $? -eq 1 ]; then
    python3 -m pip install pipenv
fi
python3 -m pipenv sync
python3 -m pipenv run python -m unittest
