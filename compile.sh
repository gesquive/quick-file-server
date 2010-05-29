#!/bin/bash
# compile.sh
# GusE 2010-05-27 V1.0
#
# Compresses source files into the project file

EXE=quick-file-server.py

for filename in virtual/*; do
    name=$(basename $filename)
    contents=`python -c "import re; print open('$filename', 'r').read().encode('base64').replace('\n', '')"`
    # echo "VIRTUAL_FILES['$name'] = '$contents'"
    sed -i "s|^VIRTUAL_FILES\['$name'\] = '.*'$|VIRTUAL_FILES\['$name'\] = '$contents'|g" $EXE
    # echo "s/^FILES\['$name'\]='.*'$/FILES\['$name'\]='$contents'/g"
done
