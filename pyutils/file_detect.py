#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
1.检查文件类型，文件中内容的类型
2.收集中文编码问题，解决编码常见问题
'''

import sys,os

print "current sys defaultencoding:",sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding("utf-8")
print "reload sys;then sys defaultencoding is :",sys.getdefaultencoding()

import chardet
import codecs
def check_text(buf=''):
    print '>>',chardet.detect(buf),'->',buf[:1024]

def check_file(filename=''):
    if not os.path.exists(filename):
        print "not exists:",filename
        return
    with open(filename,'r') as f:
        buf=f.read(1024)
        check_text(buf)
        s=buf.decode('GB2312')
        print '-'*50
        print s

    # with codecs.open(filename) as f:
    #     buf=f.read(1024)
    #     check_text(buf)




def test1():
    s1='helloworld'
    check_text(s1)
    s2='中国人'
    check_text(s2)
    check_file(r'D:\dev\Github\projectMgr\PyMLIB\userGroup\input\user_param_feature.csv')

def main():
    test1()

if __name__ == '__main__':
    main()

