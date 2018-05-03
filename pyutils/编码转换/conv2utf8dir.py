#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import codecs
import chardet
import shutil


class Global:
    srcdir=r'D:\tmp\app\easyfilesvr\fileroot\shimy_src'
    tgtdir=r'D:\tmp\app\easyfilesvr\fileroot\shimy_src2'
    srctotal=0
    tgttotal=0
    faillist=[]


#被认为invalid的文件，将不被包含在工程目录里
def is_invalid_file(f=""):
    f=f.lower()
    suffixs=[".gitignore",".gitmodules",".travis.yml",".dat",".patch",".png","log","zip",".rc",".ico",".bmp","doc",".pyc"]
    for s in suffixs:
        if f.endswith(s):
            return True
    return False

def isTextFile(fn=''):
    fn=fn.lower()
    suffixs = [".hpp", ".c", ".xml", ".cpp", ".txt",".h"]
    for s in suffixs:
        if fn.endswith(s):
            return True
    return False



def readFileEncodeFlag(fn):
    data=''

    with open(fn,'r') as f:
        tmp = f.read(4096)
        while tmp:
            data += tmp
            tmp = f.read(4096)
        if not  data:
            return "EMPTY",""
    r=chardet.detect(data)
    # print r
    # from bs4 import UnicodeDammit
    # dammit = UnicodeDammit(data)
    # print ">",dammit.original_encoding
    if  'encoding' not in r:
            return "ERROR",data
    e= r['encoding']
    return e,data



def convUtf8File(src_file,tgt_file,again=0):
    print src_file," > ",tgt_file
    flag,data=readFileEncodeFlag(src_file)
    print flag

    if flag=="EMPTY":
        return
    if flag=="ERROR":
        Global.faillist.append( [src_file,flag])
        return

    if os.path.exists( tgt_file ):
        os.remove(tgt_file)

    if  flag=='utf-8':
        if tgt_file:
            with codecs.open(tgt_file, 'w') as f:
                f.write(data)
        Global.tgttotal += 1
        return
    if again==0:
        tmpfile=tgt_file+"_tmp"
        with codecs.open(tmpfile,'wb') as f:
            f.write(data)
        convUtf8File(tmpfile,tgt_file,1)
        os.remove( tmpfile)



        return
    if again==1:
        if tgt_file:
            data = data.decode(flag, 'ignore')
            with codecs.open(tgt_file, 'w', 'utf-8') as f:
                f.write(data)
                convUtf8File(tgt_file, "", 2)
        return
    Global.faillist.append( [src_file,flag])


#遍历rootDir，将得到的dir放在dirList里，将file放在fileList
def tsearch1(rootDir):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        # if is_invalid_file(path):
        #     continue
        if os.path.isdir(path):
            path2 = path.replace( Global.srcdir,Global.tgtdir)
            if not  os.path.exists(path2)  :
                os.makedirs(path2)
            tsearch1(path)
        else:
            path2 = path.replace(Global.srcdir, Global.tgtdir)
            if isTextFile(path):
                Global.srctotal += 1
                convUtf8File(path,path2)
            else:
                shutil.copyfile(path,path2)


def main():
    if not os.path.exists( Global.tgtdir):
        os.makedirs( Global.tgtdir)
    tsearch1(Global.srcdir)
    print Global.srctotal
    print Global.tgttotal
    print "FAIL==================FAIL=="
    for line in  Global.faillist:
        print line[0],line[1]
    # s=r'D:\tmp\app\easyfilesvr\fileroot\shimy_src2\protocol\cmdtype.h'
    # convUtf8File(s,s)



if __name__ == '__main__':
    main()