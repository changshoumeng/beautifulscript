#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################
#   A clever person solves a problem. A wise person avoids it
#   Please call Me programming devil.
#
#
######################################################## #

import os
def tsearch1(rootDir):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        print path
        if os.path.isdir(path):
            tsearch1(path)


import os
def tsearch2(rootDir):
    list_dirs = os.walk(rootDir)
    for root, dirs, files in list_dirs:
        for d in dirs:
            print os.path.join(root, d)
        for f in files:
            print os.path.join(root, f)

def main():
    rootDir=r"D:\work\zhangtao\chain\qtum-master"
    tsearch2(rootDir)
if __name__ == '__main__':
    main()