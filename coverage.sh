#!/bin/sh
set -e
python3 -m coverage run ./manage.py test $@
python3 -m coverage report
python3 -m coverage html
exit 0
