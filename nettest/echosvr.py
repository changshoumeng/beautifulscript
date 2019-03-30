# -*- coding: utf-8 -*-
"""
In conjunction with nc.py for network testing,
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


def process_acceptor(accetpor, addr):
    client_info = "{0}_{1}".format(accetpor.fileno(), addr)
    print('accept {0}'.format(client_info))

    while True:
        try:
            data = accetpor.recv(1024 * 16)
            if not data:
                print('recv 0.client:{0} '.format(client_info))
                accetpor.close()
                return
            print("on_msg>{0}".format(data))
            if data.startswith("end"):
                print('end {0}'.format(client_info))
                accetpor.close()
                return
            rsp = on_msg(data, client_info)
            print("on_rsp>{0}".format(rsp))
            accetpor.send(rsp)
        except socket.timeout:
            continue
        except Exception as e:
            print('recv a exception.client:{0} {1}'.format(client_info, e))
            accetpor.close()
            return


def server(port):
    addr = ("", port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(addr)
    sock.listen(1024)
    print("======================================")
    print("=============")
    print("create socket:{0} listen in {1}".format(sock.fileno(), addr))

    while True:
        print("waiting for a connection....")
        try:
            accetpor, addr = sock.accept()
            process_acceptor(accetpor, addr)
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
