#!/bin/bash

export PYTHONPATH=${AUREA_HOME}/build/lib.linux-x86_64-2.7/:${TRENDS_HOME}/pylib/

AUREA_DIR=${AUREA_HOME}/scripts/testScripts/
cd ${AUREA_DIR}

python aurea.py -a normal.csv -b tumor.csv -l tsp -c config.xml