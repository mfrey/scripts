#!/bin/bash

PYTHON_FILES=`find . -name '*.py'`

for FILE in $PYTHON_FILES; do
   python2.7 /usr/lib/python2.7/Tools/scripts/reindent.py $FILE
done
