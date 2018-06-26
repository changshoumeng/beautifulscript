#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################
#   A clever person solves a problem. A wise person avoids it
#   Please call Me programming devil.
#
#
######################################################## #
import os
import codecs
import chardet

def convUtf8File(src_file,tgt_file,again=0):
    print "input:",src_file
    if not os.path.exists(src_file):
        print "not exits:",src_file
        return
    data=""
    with open(src_file,'r') as f:
        data=f.read()
    r=chardet.detect(data[:1024])
    print "detect:",r
    e= r['encoding']
    if  e=='utf-8':
        with codecs.open(tgt_file, 'w') as f:
            f.write(data)
        print "OK!"
        return

    if again==0:
        print "save as:", tgt_file
        with codecs.open(tgt_file,'w') as f:
            f.write(data)
        print "go on.."
        convUtf8File(tgt_file,tgt_file,1)
        return
    data = data.decode(e, 'ignore')
    with codecs.open(tgt_file, 'w', 'utf-8') as f:
        f.write(data)

    with open(tgt_file, 'r') as f:
        data = f.read()

    r = chardet.detect(data[:1024])
    print "final detect:", r
    print "OK!"

convUtf8File(r'D:\dev\Github\projectMgr\PyMLIB\userGroup\input\hive_data_param.csv',r'D:\dev\Github\projectMgr\PyMLIB\userGroup\input\hive_data_param2.csv')