#!/bin/bash

#A little script to help automating building
#settings
version=1.6.1

#32bit vm
arch=intel
aurea_dir=/Users/magis1/Documents/Lab/JohnEarls/AUREA
drop_dir=/Users/magis1/Documents/Dropbox/builds

cd $aurea_dir
git pull
#2.7 build

rm -rf $aurea_dir/dist/*
rm -rf $aurea_dir/build/*

# Build version for python 2.6
source ~/Documents/VirtualEnv/env2.6/bin/activate
ARCHFLAGS="-arch i386 -arch x86_64" python setup.py sdist 
ARCHFLAGS="-arch i386 -arch x86_64" python setup.py bdist
mv $aurea_dir/dist/AUREA-$version.macosx-10.6-universal.tar.gz $aurea_dir/dist/AUREA-$version-py2.6-macosx-$arch.tar.gz 
ARCHFLAGS="-arch i386 -arch x86_64" python setup.py bdist_egg 
mv $aurea_dir/dist/AUREA-$version-py2.6-macosx-10.6-universal.egg $aurea_dir/dist/AUREA-$version-py2.6-macosx-$arch.egg

# Build version for python 2.7
source ~/Documents/VirtualEnv/env2.7/bin/activate
ARCHFLAGS="-arch i386 -arch x86_64" python setup.py sdist
ARCHFLAGS="-arch i386 -arch x86_64" python setup.py bdist
mv $aurea_dir/dist/AUREA-$version.macosx-10.4-intel.tar.gz $aurea_dir/dist/AUREA-$version-py2.7-macosx-$arch.tar.gz
ARCHFLAGS="-arch i386 -arch x86_64" python setup.py bdist_egg
mv $aurea_dir/dist/AUREA-$version-py2.7-macosx-10.4-intel.egg $aurea_dir/dist/AUREA-$version-py2.7-macosx-$arch.egg

# Copy to dropbox
cp $aurea_dir/dist/*macosx* $drop_dir 
