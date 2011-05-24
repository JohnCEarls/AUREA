"""
Creates a proper MANIFEST template

run with:

python build_Manifest.py > MANIFEST.in
"""
import os
print "include README"
print "include setup.py"
print "include ez_setup.py"
for root, _ , files in os.walk('src'):
    for file in files:
        print "include ",
        print os.path.join(root,file)
for root, _ , files in os.walk('workspace'):
    for file in files:
        print "include ",
        print os.path.join(root,file)

