# -*- coding: utf-8 -*-
# http://blog.csdn.net/zcyhappy1314/article/details/8283717
import MySQLdb
import sys
import os
import time

mysql = r"/usr/bin/mysql"
mysqldump = r"/usr/bin/mysqldump"
mysql_host = "127.0.0.1"
mysql_port = 3306
mysql_user = "root"
mysql_pwd = ""
save_dir = "temp"


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def pause():
    raw_input("please enter to continue!")
    print "doing.."


# dump database ,only db-struct,
def dumpDatabaseOnlyStruct(dbName="",dbCount=0):
    print "dumpDatabaseOnlyStruct:",dbName,dbCount
    databases=""
    if dbCount==0:
        databases=dbName
    else:
        for i in xrange(dbCount):
            databases += "{0}_{1} ".format(dbName,i)
    dbFile = r"{0}/{1}.sql".format(save_dir, dbName)
    if os.path.exists(dbFile):
        print "remove file:", dbFile
        os.remove(dbFile)
    ########################
    cmdStr = "{0} -h{1} -u{2} -p{3} -d -B {4} > {5}".format(mysqldump, mysql_host, mysql_user, mysql_pwd, databases,dbFile)
    print "------------------dumpDatabaseOnlyStruct---------------"
    print cmdStr
    pause()
    t1 = time.time()
    result = os.system(cmdStr)
    t2 = time.time()
    t3 = t2 - t1
    print "dumpDatabaseOnlyStruct cmd:{0} \n>>result:{1} useTime:{2} file:{3}".format(cmdStr, result, t3, dbFile)


# dump database , db-struct,+ db-data
#db_im_msg_record
def dumpDatabaseStructAndData(dbName="",dbCount=0):
    databases=""
    if dbCount==0:
        databases=dbName
    else:
        for i in xrange(dbCount):
            databases += "{0}_{1} ".format(dbName,i)

    dbFile = r"{0}/{1}.sql".format(save_dir, dbName)
    if os.path.exists(dbFile):
        print "remove file:", dbFile
        os.remove(dbFile)
    ########################
    cmdStr = "{0} -h{1} -u{2} -p{3} -B {4} > {5}".format(mysqldump, mysql_host, mysql_user, mysql_pwd, databases, dbFile)
    print "------------------dumpDatabaseStructAndData---------------"
    print cmdStr
    pause()
    t1 = time.time()
    result = os.system(cmdStr)
    t2 = time.time()
    t3 = t2 - t1
    print "dumpDatabaseOnlyStruct cmd:{0} \n>>result:{1} useTime:{2} file:{3}".format(cmdStr, result, t3, dbFile)


# recover from mysql_dump_sql_file
def recoverMysqlFromDumpfile(dbName):
    dbFile = r"{0}/{1}.sql".format(save_dir, dbName)
    if not os.path.exists(dbFile):
        print "recoverMysqlFromDumpfile,but not find file:{0}".format(dbFile)
        sys.exit(-1)
    cmdStr = '{0} -h{1} -u{2} -p{3} -e "source {4}"'.format(mysql, mysql_host, mysql_user, mysql_pwd, dbFile)
    print "------------------recoverMysqlFromDumpfile---------------"
    print cmdStr
    pause()
    t1 = time.time()
    result = os.system(cmdStr)
    t2 = time.time()
    t3 = t2 - t1
    print "recoverMysqlFromDumpfile cmd:{0} result:{1} useTime:{2}".format(cmdStr, result, t3)


def dumpMysqlDB():
    dumpDatabaseOnlyStruct("db_im_msg_record",8)
    dumpDatabaseOnlyStruct("db_im_user_msg", 4)
    dumpDatabaseOnlyStruct("db_im_group", 8)
    #dumpDatabaseStructAndData("db_im_msg_record",8)


def recoverMysqlDB():
    recoverMysqlFromDumpfile("db_im_msg_record")
    recoverMysqlFromDumpfile("db_im_user_msg")
    recoverMysqlFromDumpfile("db_im_group")

if __name__ == "__main__":
    print "-------begin--------"
    mkdir(save_dir)
    dumpMysqlDB()
   # recoverMysqlDB()
    print "-------done---------"