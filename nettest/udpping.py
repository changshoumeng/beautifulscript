import socket
import threading
import time
import struct
import Queue
queue = Queue.Queue()
def udp_sender(ip,port):
    try:
        ADDR = (ip,port)
        sock_udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock_udp.sendto("abcd...",ADDR)
        sock_udp.close()
    except Exception as e:
        print "udp_sender caught :",e,ip,port
        pass
def icmp_receiver(ip,port):
    # print "----icmp_receiver----"
    icmp = socket.getprotobyname("icmp")
    try:
        sock_icmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        # print "----icmp_receiver---2-"
    except socket.error, (errno, msg):
        print errno,msg
        if errno == 1:
            # Operation not permitted
            msg = msg + (
                " - Note that ICMP messages can only be sent from processes"
                " running as root."
            )
            print msg
            raise socket.error(msg)
        raise # raise the original error
    sock_icmp.settimeout(3)
    try:
        recPacket,addr = sock_icmp.recvfrom(64)
    except:
        queue.put(True)
        return
    icmpHeader = recPacket[20:28]
    icmpPort = int(recPacket.encode('hex')[100:104],16)
    head_type, code, checksum, packetID, sequence = struct.unpack(
            "bbHHh", icmpHeader
    )
    sock_icmp.close()
    if code == 3 and icmpPort == port and addr[0] == ip:
        queue.put(False)
    return
def checker_udp(ip,port):
    try:
        thread_udp = threading.Thread(target=udp_sender,args=(ip,port))
        thread_icmp = threading.Thread(target=icmp_receiver,args=(ip,port))
        thread_udp.daemon= True
        thread_icmp.daemon = True
        thread_icmp.start()
        time.sleep(1)
        thread_udp.start()
        thread_icmp.join()
        thread_udp.join()
        return queue.get(False)
    except:
        print "exception:",ip,port
        return False


def main():
    portlist=[
        10321,
        5463,
        7143,
        3567,
        9600,
        4879,
        2197,
        8366,
        6578
    ]
    iplist=['139.196.4.12','106.14.242.172','112.73.93.126','112.73.93.127']
    for ip in iplist:
        for port in portlist:
            ret=checker_udp(ip, port)
            print "checker_udp:",ret,ip,port



if __name__ == '__main__':
    # import sys
    main()
    # print checker_udp(sys.argv[1],int(sys.argv[2]))
