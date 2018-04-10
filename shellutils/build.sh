#!/bin/bash
#Teach Wisedom to My Machine
#zhangtao

set -x

date ;

echo "Prepare to Build.."
rm -rf  common  protocol bin lib update
ln -s ../common common
ln -s ../protocol protocol
mkdir lib
mkdir bin


echo "Copy Depended Library Files.."
cp -f ../lib/libcommon2.so lib/
cp -f ../lib/libcorebase.so lib/
cp -f ../lib/libnet.so lib/
cp -f ../lib/libdbpool.so lib/
cp -f ../lib/libhiredis.a lib/
cp -f ../lib/libjson.a lib/
cp -f ../lib/libcurl.so lib/
cp -f ../lib/libmysqlclient_r.so lib/

echo "Begin Make.."
make clean;make -j 4;make install
make clean ;

result=`ls bin|wc -l`
if [ "$result" -eq "0" ];then
        echo "##########################################"
        echo "Maybe Build Failed!!"
        echo "##########################################"
        exit 0
fi

mkdir -p update/lib
cp -r lib/*.so   update/lib/
cp -f bin/*_dev  update
echo "==================Update All Files==========================="
ls -lrt update


cd ..
date ;