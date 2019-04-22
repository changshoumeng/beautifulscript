# -*- coding: utf-8 -*-
"""
In conjunction with nc.py for network testing,
this service provides a echo instruction
and remote system instruction operation

tazzhang  2019-4-1
"""


import socket
import sys
import time

socket.setdefaulttimeout(60)


def gettickcount():
    current_time = time.time()
    return int(round(current_time * 1000))


def process_msg(s):
    while True:
        inp = raw_input(">>>")
        if inp == "end":
            s.sendall(inp)
            return

        t1 = gettickcount()
        s.sendall(inp)
        t2 = gettickcount()
        t = t2 - t1
        print("send>{}>use:{}".format(inp, t))

        t1 = gettickcount()
        try:
            data = s.recv(1024 * 16)
            t2 = gettickcount()
            t = t2 - t1
            print("---------------------")
            print("recv ok. datasize:{} use:{}".format( len(data),t))
            print(data)
        except Exception as e:
            print(e)
            return


def client(address):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_info = "{0}_{1}".format(s.fileno(), address)
    t1 = gettickcount()
    try:
        s.connect(address)
        t2 = gettickcount()
        t = t2 - t1
        print("connect ok.{0} ".format(client_info, t))
    except socket.error as arg:
        t2 = gettickcount()
        t = t2 - t1
        print("connect failed.{0} ".format(client_info, t))
        print(arg)
        sys.exit(1)
    process_msg(s)


def main():
    if len(sys.argv) < 3:
        print("help:python nc.py [ip] [port]")
        return
    address = (sys.argv[1], int(sys.argv[2]) )
    client(address)

if __name__ == '__main__':
    main()
