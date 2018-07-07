#!/usr/bin/env python
# coding: utf-8
"""
原理：
    https://yq.aliyun.com/articles/60684
功能：
    实现tail -n
    实现tail -f
其它实现：
    http://www.cnblogs.com/bufferfly/p/4878688.html
    https://github.com/shengxinjing/my_blog/issues/11
BUG：
    重定向相同数据到日志文件里，使用>而不是>>的话，输入无法打印出来
"""

import os
import sys
import time

PAGE = 4096

class Tail:
    def __init__(self, filename, callback=sys.stdout.write):
        self.filename = filename
        self.callback = callback

    def reverse(self, n=10):
        """
        实现 tail -n
        """
        with open(self.filename, 'rb') as f:
            f_len = f.seek(0, 2)
            rem = f_len % PAGE
            page_n = f_len // PAGE
            r_len = rem if rem else PAGE
            while True:
                # 如果读取的页大小>=文件大小，直接读取数据输出
                if r_len >= f_len:
                    f.seek(0)
                    lines = f.readlines()[::-1]
                    break

                f.seek(-r_len, 2)
                # print('f_len: {}, rem: {}, page_n: {}, r_len: {}'.format(f_len, rem, page_n, r_len))
                lines = f.readlines()[::-1]
                count = len(lines) -1   # 末行可能不完整，减一行，加大读取量

                if count >= n:  # 如果读取到的行数>=指定行数，则退出循环读取数据
                    break
                else:   # 如果读取行数不够，载入更多的页大小读取数据
                    r_len += PAGE
                    page_n -= 1

        for line in lines[:n]:
            self.callback(line.decode('utf-8'))

    def follow(self):
        """
        实现 tail －f
        """
        with open(self.filename, 'rb') as fd:
            pos = fd.seek(0, 2)  # 打开文件时大小
            try:
                while True:
                    curr_pos = fd.seek(0,2)
                    # print('pos: {}, curr_pos: {}'.format(pos, curr_pos))
                    if pos > curr_pos:  # 表示文件数据减少或清空
                        pos = fd.seek(0, 2)
                        # time.sleep(0.3)
                        continue

                    line = fd.readline()
                    if line:
                        self.callback(line.decode('utf-8'))
                    # time.sleep(0.1)
            except KeyboardInterrupt as e:
                pass

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {} [ -f | -# ] file'.format(sys.argv[0]), file=sys.stderr)
        raise SystemExit(1)

    if not os.path.isfile(sys.argv[2]):
        print('File does not exist.')
        raise SystemExit(1)
    else:
        tail = Tail(sys.argv[2])

    if '-f' == sys.argv[1]:
        tail.reverse()
        tail.follow()
    elif '-' in sys.argv[1]:
        try:
            n = int(sys.argv[1].strip('-'))
            tail.reverse(n)
        except ValueError:
            print('Unknown command {!r}'.format(sys.argv[1]), file=sys.stderr)
            raise SystemExit(1)
    else:
        print('Unknown command {!r}'.format(sys.argv[1]), file=sys.stderr)
        raise SystemExit(1)
