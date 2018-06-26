#!/bin/sh
#author:programming devil
#ldd-linux-green-software
#http://blog.csdn.net/zhazhiqiang/article/details/32728871



if [ $# -ne 1 ]; then
		echo "You should specify a dynamically executable file"
		exit 1
fi                                                                                     e
 
if [ ! -x $1 ]; then
		echo "You should specify a executable file"
		exit 1;
fi
 
path=$1
 
############# check file type #############
result=$(ldd $path)
 
filter=$(file $path|grep dynamically|grep executable)
 
if [ -z "$filter" ]; then
		echo "$path is not a dynamically executable file!"
		file $path
		exit 1
fi
 
########### mkdir for .so files ############
packagename=$(basename $path)-pack
mkdir -p $packagename
 
IFS="
"
 
######### copy .so files ############
for line in $result; do
		sofile=notexitsfile
		if [ -z "$(echo $line | grep =)" ]; then
				sofile=$(echo $line | awk '{print $1}')
		else
				# has soft link
				sofile=$(echo $line | awk '{print $3}')
		fi
 
		if [ ! -f $sofile ]; then
				echo "ERROR FILE: $sofile"
		else
				echo "copying $sofile now..."
				cp $sofile $packagename
		fi
done
 
cp $path $packagename
echo DONE 
