#!/bin/sh
set -e
python3 manage.py test $@
exit 0
