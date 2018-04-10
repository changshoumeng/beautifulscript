#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################
#   Teach Wisedom To Machine.
#   Please Call Me Programming devil.
#   Module Name: pyZooKeeperHelp
######################################################## #
import os
import sys
import commands


app_dir="/data/appdatas/zookeeper"
conf_dir="/data/cppgroup/javaapp/java_base/zookeeper-3.4.5/conf"

cmdList=[
	"mkdir -p  %s"%app_dir,
	"call make_node node1",
	"call make_node node2",
	#"call make_node node5",
]


clientPorts=[
	'1023',#only zhanyongfu
	"2181",
	"2182",
	"2183",
	"2184",
	"2185",
]




def make_node(args):        
	print "make node:",args
        node=args
	
	os.system("mkdir %s/%s"%(app_dir,node)	 )
	os.system("mkdir %s/%s/data"%(app_dir,node) )
	os.system("mkdir %s/%s/log"%(app_dir,node) )
	num = node[4:]
	with open("%s/%s/data/myid"%(app_dir,node),'w') as f:
		f.write(num)

	clientPort=clientPorts[ int(num) ]
	with open("%s/zoo_%s.cfg"%(conf_dir,num ),'w') as f:
		f.write("tickTime=2000\n")
		f.write("initLimit=10\n")
		f.write("syncLimit=5\n")
		f.write("clientPort=%s\n"%clientPort )
		f.write("dataDir=/data/appdatas/zookeeper/%s/data\n"%(node)  )
		f.write("dataLogDir=/data/appdatas/zookeeper/%s/log\n"%(node)  )		
		f.write("server.1=192.168.1.132:2281:2291\n")
		f.write("server.2=192.168.1.132:2282:2292\n")
		f.write("server.3=192.168.1.150:2283:2293\n")
		f.write("server.4=192.168.1.150:2284:2294\n")
		f.write("server.5=192.168.1.150:2285:2295\n")
		
	
	return True





calls={
    "make_node":make_node,

}


def main():
	for cmd in cmdList:
	    print cmd
	    if cmd[:4] !="call":
		status,result=commands.getstatusoutput(cmd)	
		print ">>",cmd,"->", status,result
		if status != 0:
		    print "shell error:",cmd
		    return
	    else:	
		p=cmd.find(' ',5)
		c=cmd[5:p]
                a=cmd[p+1:]	
		if not calls[c](a):
		   print "call error:",cmd
		   return
		else:
		   print "call OK"
		pass
	pass


main()




