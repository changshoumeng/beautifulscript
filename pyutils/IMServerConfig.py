# -*- coding: utf-8 -*-
#!/usr/bin/env python
##########################################################
#   Teach Wisedom To Machine.
#   Please Call Me Programming devil.
#Create a Configfile,Show All Server's TcpConfig
#
#########################################################
import ConfigParser
import os
import time



class TcpConfig(object):
    pass







class MyConfigParser(ConfigParser.ConfigParser):
    def __init__(self,defaults=None):
        ConfigParser.ConfigParser.__init__(self,defaults=None)
    def optionxform(self, optionstr):
        return optionstr


cur_dir = os.path.split(os.path.realpath(__file__))[0]
parent_dir = os.path.abspath(os.path.join(cur_dir, os.path.pardir))
#conf_dir = os.path.join(parent_dir, "conf")
conf_dir = os.path.join(cur_dir, "conf")




def main():
    print "BEGIN"
    config_file = "my.conf"
    server_name = ""

    cf = MyConfigParser()
    config_template="test2.conf"
    if not  os.path.exists(config_template):
        print "not exist file:",config_template
        return
    try:
        cf.read(config_template)
        for i in xrange(2):
            make_config(cf,i)
            config_file_path  = "{0}{1}/{2}".format(server_name,i,config_file)
            print config_file_path
            if os.path.exists(config_file_path):
                os.remove(config_file_path)
            cf.write(open(config_file_path,'w'))
        print "Make Config Done!"
    except Exception as e:
        print e
        return False
    pass

if __name__ == '__main__':
    main()
