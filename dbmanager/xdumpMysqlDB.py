# -*- coding: utf-8 -*-
# http://blog.csdn.net/zcyhappy1314/article/details/8283717
#
# Tazzhang
#
# import MySQLdb
import sys
import os
import time

mysql = r"/usr/bin/mysql"
mysqldump = r"/usr/bin/mysqldump"
mysql_host = "192.168.101.205"
mysql_port = 3307
mysql_user = "sdkcfg"
mysql_pwd = "ymscfga123"
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
def dumpDatabaseOnlyStruct(dbName="", dbCount=0):
    print ("dumpDatabaseOnlyStruct: {0} {1}".format(dbName, dbCount))
    databases = ""
    if dbCount == 0:
        databases = dbName
    else:
        for i in xrange(dbCount):
            databases += "{0}_{1} ".format(dbName, i)
    dbFile = r"{0}/{1}.sql".format(save_dir, dbName)
    if os.path.exists(dbFile):
        print "remove file:", dbFile
        os.remove(dbFile)
    ########################
    cmdStr = "{0} -h{1} -P{2} -u{3} -p{4} -d -B {5} > {6}".format(mysqldump, mysql_host, mysql_port, mysql_user,
                                                                  mysql_pwd, databases, dbFile)
    print ("------------------dumpDatabaseOnlyStruct---------------")
    print (cmdStr)
    pause()
    t1 = time.time()
    result = os.system(cmdStr)
    t2 = time.time()
    t3 = t2 - t1
    print ("dumpDatabaseOnlyStruct cmd:{0} \n>>result:{1} useTime:{2} file:{3}".format(cmdStr, result, t3, dbFile))


# dump database , db-struct,+ db-data
# db_im_msg_record
def dumpDatabaseStructAndData(dbName="", dbCount=0):
    databases = ""
    if dbCount == 0:
        databases = dbName
    else:
        for i in xrange(dbCount):
            databases += "{0}_{1} ".format(dbName, i)

    dbFile = r"{0}/{1}.sql".format(save_dir, dbName)
    if os.path.exists(dbFile):
        print("remove file:".format(dbFile))
        os.remove(dbFile)
    ########################
    cmdStr = "{0} -h{1} -P{2} -u{3} -p{4} -B {5} > {6}".format(mysqldump, mysql_host, mysql_port, mysql_user, mysql_pwd,
                                                               databases, dbFile)
    print ("------------------dumpDatabaseStructAndData---------------")
    print (cmdStr)
    pause()
    t1 = time.time()
    result = os.system(cmdStr)
    t2 = time.time()
    t3 = t2 - t1
    print ("dumpDatabaseOnlyStruct cmd:{0} \n>>result:{1} useTime:{2} file:{3}".format(cmdStr, result, t3, dbFile))


# recover from mysql_dump_sql_file
def recoverMysqlFromDumpfile(dbName):
    dbFile = r"{0}/{1}.sql".format(save_dir, dbName)
    if not os.path.exists(dbFile):
        print "recoverMysqlFromDumpfile,but not find file:{0}".format(dbFile)
        sys.exit(-1)
    cmdStr = '{0} -h{1} -P{2} -u{3} -p{4} -e "source {5}"'.format(mysql, mysql_host, mysql_port, mysql_user, mysql_pwd,
                                                                  dbFile)
    print ("------------------recoverMysqlFromDumpfile---------------")
    print (cmdStr)
    pause()
    t1 = time.time()
    result = os.system(cmdStr)
    t2 = time.time()
    t3 = t2 - t1
    print ("recoverMysqlFromDumpfile cmd:{0} result:{1} useTime:{2}".format(cmdStr, result, t3))


def loadConfig():
    fileName = "db_list.txt"
    if not os.path.exists(fileName):
        print ("cannot find file:{0}".format(fileName))
        return

    dbList = []
    with open(fileName) as rf:
        for line in rf:
            line = line.strip()
            if not line:
                continue
            elems = []
            for sep in line.split(" "):
                sep = sep.strip()
                if not sep:
                    continue
                elems.append(sep)
            if not elems:
                continue

            if len(elems) >= 3:
                print("invalid elems:{0}".format(elems))
                sys.exit(1)

            dbList.append(elems)
    return dbList


def dumpMysqlDB():
    dbList = loadConfig()
    if not dbList:
        print("dbList is empty")
        return

    for elems in dbList:
        if len(elems) == 1:
            dumpDatabaseStructAndData(elems[0], 0)
            continue

        if len(elems) == 2:
            dumpDatabaseStructAndData(elems[0], int(elems[0]))
            continue


def recoverMysqlDB():
    dbList = loadConfig()
    if not dbList:
        print("dbList is empty")
        return

    for elems in dbList:
        recoverMysqlFromDumpfile(elems[0])


if __name__ == "__main__":
    mkdir(save_dir)
    dumpMysqlDB()
    # recoverMysqlDB()

