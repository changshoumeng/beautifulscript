import socket
import sys

import time


def gettickcount():
    current_time = time.time()
    return int(round(current_time * 1000))


def process_msg(s, address):
    while True:
        inp = raw_input(">>>")
        if inp == "end":
            s.sendto(inp, address)
            return

        t1 = gettickcount()
        r = s.sendto(inp, address)
        t2 = gettickcount()
        t = t2 - t1
        print("send>{}>use:{} ret:{}".format(inp, t, r))

        t1 = gettickcount()
        try:
            data, server_addr = s.recvfrom(1024)
            t2 = gettickcount()
            t = t2 - t1
            print("---------------------")
            print("recvfrom ok. datasize:{} use:{} from:{}".format(len(data), t, server_addr))
            print(data)
        except Exception as e:
            print(e)
            return


def client(address):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    process_msg(client, address)
    client.close()


def main():
    if len(sys.argv) < 3:
        print("help:python udpclient.py [ip] [port]")
        return
    address = (sys.argv[1], int(sys.argv[2]))
    client(address)


if __name__ == '__main__':
    main()
