#!/bin/bash

#A little script to help automating building
#settings
version=1.6.1

#32bit vm
arch=i386
aurea_dir=/Users/johnearls/AUREA
drop_dir=/Users/magis1/Documents/Dropbox/builds
base_env=/Users/johnearls/env/AUREA2

cd $aurea_dir
git pull
#2.7 build

rm -rf $aurea_dir/dist/*
rm -rf $aurea_dir/build/*
# Build version for python 2.6
source /Users/johnearls/env/AUREA26/bin/activate
ARCHFLAGS="-arch i386" python setup.py bdist
#make sure we know the py version
mv $aurea_dir/dist/AUREA-$version.macosx-10.5-i386.tar.gz $aurea_dir/dist/AUREA-$version-py2.6-macosx-10.5-$arch.tar.gz 
ARCHFLAGS="-arch i386" python setup.py bdist_egg 

deactivate
# Build version for python 2.7

source /Users/johnearls/env/AUREA27/bin/activate
ARCHFLAGS="-arch i386" python setup.py bdist
mv $aurea_dir/dist/AUREA-$version.macosx-10.5-i386.tar.gz $aurea_dir/dist/AUREA-$version-py2.7-macosx-10.5-$arch.tar.gz 
ARCHFLAGS="-arch i386" python setup.py bdist_egg
deactivate
# Copy to dropbox
#cp $aurea_dir/dist/*macosx* $drop_dir 
