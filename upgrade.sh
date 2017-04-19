#!/usr/bin/env bash
#Teach wisedom to my machine
#zhangtao
set -x

PROJECT=~/fs/dev/clcpp
SERVER=$PROJECT/tianqi

cp -f  $SERVER/update/*_dev ./
rm -rf ../lib
cp -r  $SERVER/update/lib  ../
