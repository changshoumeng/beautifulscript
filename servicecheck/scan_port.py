#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket
import sys
import app_util
import app_env

import threading
import time
import struct
import Queue

queue = Queue.Queue()

'''
address is (ip,port)
'''


def tcp_connect_test(address):
    ret = 0
    socket.setdefaulttimeout(5)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    log = "fileno:{0} remote:{1}".format(s.fileno(), address)
    t1 = app_util.gettickcount()

    try:
        s.connect(address)
        t2 = app_util.gettickcount()
        t = t2 - t1
        log += " connect ok. use ms:{0}".format(t)
        ret = 0
    except socket.error as arg:
        t2 = app_util.gettickcount()
        t = t2 - t1
        log += " connect failed. use ms:{0},error:{1}".format(t, str(arg))
        ret = 1
    s.close()
    return ret, log


def udp_sender(address):
    ret = 0
    sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    log = "udp_sender udpfileno:{0} remote:{1} ".format(sock_udp.fileno(), address)
    try:
        sock_udp.sendto("abcd...", address)
        ret = 0
        log += "sendto ok;"
    except Exception as e:
        log += "sendto failed; error:{1}".format(str(2))
        ret = 1
    sock_udp.close()
    #print(ret, log)


def icmp_receiver(address):
    ret = 0
    log = "icmp_receiver remote:{0}".format(address)
    icmp = socket.getprotobyname("icmp")
    try:
        sock_icmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    except socket.error, (errno, msg):
        if errno == 1:
            log += " Operation not permitted;Note that ICMP messages can only be sent from processes;"
            log += "\nmsg:" + msg
            print(ret, log)
            raise socket.error(msg)

        log += " unexpected error,msg:" + msg
        print(ret, log)
        raise  # raise the original error
    sock_icmp.settimeout(3)
    try:
        recPacket, addr = sock_icmp.recvfrom(64)
    except Exception as e:
        log += " recvfrom exception:{0}".format(str(e))
        #print(ret, log)
        queue.put(True)
        return
    icmpHeader = recPacket[20:28]
    icmpPort = int(recPacket.encode('hex')[100:104], 16)
    head_type, code, checksum, packetID, sequence = struct.unpack(
        "bbHHh", icmpHeader
    )
    sock_icmp.close()
    if code == 3 and icmpPort == address[1] and addr[0] == address[0]:
        log += " recv->icmpPort:{0} addr:{1}".format(icmpPort, addr)
        queue.put(False)

    print(ret, log)
    return


def udp_connect_test(address):
    ret = 0
    log = "udp_connect_test remote:{0}".format(address)
    if app_env.is_win32():
        ret = 1
        log += ",not support in win32,so give up the test "
        return ret, log
    try:
        thread_udp = threading.Thread(target=udp_sender, args=(address,))
        thread_icmp = threading.Thread(target=icmp_receiver, args=(address,))
        thread_udp.daemon = True
        thread_icmp.daemon = True
        thread_icmp.start()
        time.sleep(1)
        thread_udp.start()
        thread_icmp.join()
        thread_udp.join()
        if queue.get(False):
            ret = 0
            log += " connect ok;"
        else:
            ret = 1
            log += " connect failed;"
    except:
        ret = 1
        log += " connect error;"
    return ret, log


