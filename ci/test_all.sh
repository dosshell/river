#!/bin/bash

MY_PATH="`dirname \"$0\"`"
cd $MY_PATH

./test_crlf.sh
crlf=$?

./test_flake8.sh
flake=$?

./test_unit_tests.sh
unit=$?

exit_code=0
echo "#############################################################"
if [ $crlf -eq 0 ]; then
    echo "CRLF OK"
else
    echo "CRLF FAILED"
    exit_code=1
fi

if [ $flake -eq 0 ]; then
    echo "FLAKE8 OK"
else
    echo "FLAKE8 FAILED"
    exit_code=1
fi

if [ $unit -eq 0 ]; then
    echo "UNIT TESTS OK"
else
    echo "UNIT TESTS FAILED"
    exit_code=1
fi

exit $exit_code
