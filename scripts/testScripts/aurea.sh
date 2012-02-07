#!/bin/bash

export PYTHONPATH=/mnt/price1/vcassen/AUREA/build/lib.linux-x86_64-2.7/:/mnt/price1/vcassen/trends/pylib/

AUREA_DIR=/mnt/price1/vcassen/AUREA/scripts/testScripts/
cd ${AUREA_DIR}

python aurea.py -a normal.csv -b tumor.csv -l tsp -c config.xml