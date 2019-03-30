# -*- coding: utf-8 -*-
"""
In conjunction with udpclient.py for network testing,
this service provides a echo instruction
and remote system instruction operation

tazzhang  2019-4-1
"""

import os
import sys
import socket

import subprocess

socket.setdefaulttimeout(60)


def on_msg(data="", client_info=""):
    if data == "me":
        info = client_info
        return info

    if data.startswith("sh "):
        cmd = data[3:]
        cmd = cmd.strip()
        print("cmd>{0}".format(cmd))
        print("============================================")
        # out = os.popen(cmd)
        out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return out.stdout.read()
        # return out.read()
    return data


def process_acceptor(sock, data, client_addr):
    client_info = "{0}".format(client_addr)
    print("recvfrom:{} datasize:{} data:{}".format(client_info, len(data), data))
    rsp = on_msg(data, client_info)
    print("rsp<<{}".format(rsp))
    r = sock.sendto(rsp, client_addr)
    print(r)


def server(port):
    addr = ("", port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(addr)
    print("======================================")
    print("=============")
    print("create socket:{0}  in {1}".format(sock.fileno(), addr))

    while True:
        try:
            data, client_addr = sock.recvfrom(1024)
            process_acceptor(sock, data, client_addr)
        except socket.timeout:
            pass
        except Exception as e:
            print("excetipn:{0}".format(e))

    sock.close()


def main():
    port = 1314
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    server(int(port))


if __name__ == '__main__':
    main()
