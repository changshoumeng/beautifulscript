#!/usr/bin/python
# -*- coding: UTF-8 -*-
import scan_port
import app_util


class CONFIG:
    neiwang = True
    machine = "192.168.102.79"
    slist = []
    services = u'''
    sshd          [OUT]22
    echosvr       [OUT]4444    
    -----------------------------------------------------------------------------------------------               
    mariadb       [IN]3306                                                            
    mongo         [IN]27017
    redis         [IN]6379
    fastdfs       [IN]22122/23000/8090
    emq           [IN]18083/11883/8083/8883/8091/4369      [OUT]1883/8084
    ----------------------------------------------------------------------------------------------- 
    cfgsrv                                                 [OUT]10200                [DEP]mongodb/mariadb
    account       [IN]9003/8004/8006/                      [OUT]8080                 [DEP]fastdfs
    
    glass         [IN]8020/8210/8010/8110                  [OUT]8008                
                                                                                                                               
    -----------------------------------------------------------------------------------------------
    pp_sdk_verify    [OUT]5000/5001/8011/8012/8081/8082  [OUT]udp8012
    pp_redirect      [OUT]6574/5574                      [OUT]udp5574
    pp_config        [IN]9010/9011
    pp_mcu_signal1   [OUT]6006/6106
    pp_mcu_media1    [OUT]6008                           [OUT]udp6008/udp6010/udp6020  
    mysqld           [IN]3307
    '''


def parse_line(line=""):
    service = []
    for sep in line.split():
        sep = sep.strip()
        if not sep:
            continue
        service.append(sep)
    return service


def load_config():
    CONFIG.slist = []
    for line in CONFIG.services.splitlines():
        line = line.strip()
        if not line:
            continue
        ch = line[0]
        if not ch.isalnum():
            continue
        if "[IN]" not in line and "[OUT]" not in line:
            continue
        s = parse_line(line)
        CONFIG.slist.append(s)


def net_test(name, ps=""):
    for p in ps.split("/"):
        p = p.strip()
        if not p:
            continue
        if "udp" in p:
            p = p[3:]
            port = int(p)
            address = (CONFIG.machine, port)
            ret, log = scan_port.udp_connect_test(address)
            print("{0}\t{1}\t{2}".format(name, ret, log))
        else:
            port = int(p)
            address = (CONFIG.machine, port)
            ret, log = scan_port.tcp_connect_test(address)
            print("{0}\t{1}\t{2}".format(name, ret, log))


def main():
    load_config()
    for service in CONFIG.slist:
        name = service[0]
        ss = service[1:]
        for s in ss:
            if "[OUT]" in s:
                ps = s[5:]
                net_test(name, ps)
                continue

            if CONFIG.neiwang:
                if "[IN]" in s:
                    ps = s[4:]
                    net_test(name, ps)
                    continue


if __name__ == '__main__':
    print("check begin:{0}".format(app_util.now()))
    main()
    print("check   end:{0}".format(app_util.now()))
