#!/bin/sh
 
mydir="$(dirname "$0")"
rootdir="$(readlink -f "$mydir/../")"

# Activate venv
orgdir=$PWD
cd $mydir/../src;
v=$(pipenv --venv)
cd $orgdir
. $v/bin/activate

# RUN
python -u "$rootdir/src/river.py" "$@"

