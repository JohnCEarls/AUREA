#!/bin/bash

#A little script to help automating building
#settings
version=1.6.7

#64bit workstation
arch=x86_64
base_dir=/home/earls3/secondary/Price
drop_dir=/home/earls3/Dropbox/Price/builds

cd $base_dir/AUREA
git pull
#2.7 build

rm -rf $base_dir/AUREA/dist/*
rm -rf $base_dir/AUREA/build/*

#see: https://www.evernote.com/shard/s21/sh/c51b3bbe-a343-444b-82a0-a4aba5ac6a33/ac395eb1e0e90b6243f4235d094e58ca
source ~/env/AUREA27/bin/activate
python setup.py sdist 
python setup.py bdist
cp $base_dir/AUREA/dist/AUREA-$version.linux-$arch.tar.gz $base_dir/AUREA/dist/AUREA-$version-py2.7.linux-$arch.tar.gz 
python setup.py bdist_egg 
rm -f $base_dir/AUREA/dist/AUREA-$version.linux-$arch.tar.gz

source ~/env/AUREA26/bin/activate
python setup.py bdist_egg 
python setup.py bdist           
cp $base_dir/AUREA/dist/AUREA-$version.linux-$arch.tar.gz $base_dir/AUREA/dist/AUREA-$version-py2.6.linux-$arch.tar.gz
rm -f /home/earls3/Price/AUREA/dist/AUREA-$version.linux-$arch.tar.gz

cp $base_dir/AUREA/dist/* $drop_dir 
