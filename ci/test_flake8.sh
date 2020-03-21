#!/bin/bash

MY_PATH="`dirname \"$0\"`"
cd $MY_PATH/..

python3 -m pip install flake8
python3 -m flake8 --config=./src/.flake8
