#!/usr/bin/python
import os
import re
import shutil

r = re.compile(r'\w+\.php')
for filename in os.listdir('.'):
    if filename[-3:] == 'php':
        shutil.copyfile(filename, filename[:-3] + 'html')
