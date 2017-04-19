#!/bin/bash
##########################################################
#   Teach Wisedom To Machine.
#   Please Call Me Programming devil.
#   ModuleName:server.sh
#   Note: /etc/rc.local
#########################################################

# you must change it
PROCESS_NAME = "test"
SERVER_LOG_DIR = "/data/cpplog"

# you cannot change it
LOG_FILE = "run.log"
PID_FILE = "run.pid"
BASE_DIR = ""
RUN_DIR = ""
LIB_DIR = ""

function
timeStamp()
{
    date + '%Y/%m/%d %H:%M:%S'
}

function
timeStamp2()
{
    date + '%Y%m%d%H%M%S'
}

function
logMessage()
{
    echo $(timeStamp) $@
echo

$(timeStamp) $@

>> $RUN_DIR /$LOG_FILE
}

function
setEnv()
{
if [-z "$BASE_DIR"];
then
PRG = "$0"
while [-h "$PRG"] ; do
ls = `ls - ld
"$PRG"
`
link = `expr
"$ls": '.*-> \(.*\)$'
`
if expr "$link": '/.*' > / dev / null;
then
PRG = "$link"
else
PRG = "`dirname "$PRG
"`/$link"
fi
done
BASE_DIR = `dirname
"$PRG"
` /..
BASE_DIR = `cd
"$BASE_DIR" & & pwd
`
fi
RUN_DIR =$BASE_DIR / bin / run
BIN_DIR =$BASE_DIR / bin
LIB_DIR =$BASE_DIR / lib
mkdir - p  $RUN_DIR
}

function
setProcessName()
{
IS_CHECK_NAME =$1
if [-z "$IS_CHECK_NAME"] ;then
IS_CHECK_NAME = 1
fi

if [ $IS_CHECK_NAME -eq 0];then
PROCESS_NAME =${BASE_DIR  ##*/}
return
fi

if [-f "$BIN_DIR/$PROCESS_NAME"] ;then
NEWFILENAME =${BASE_DIR  ##*/}
if ["$NEWFILENAME" != "$PROCESS_NAME"];
then
[-f
"$BIN_DIR/$NEWFILENAME"] & & mv
"$BIN_DIR/$NEWFILENAME"  "${BIN_DIR}/${NEWFILENAME}_$(timeStamp2)"
mv
"$BIN_DIR/$PROCESS_NAME"  "$BIN_DIR/$NEWFILENAME"
PROCESS_NAME =$NEWFILENAME
fi
else
PROCESS_NAME =${BASE_DIR  ##*/}
fi
}


function
setWatchDog()
{
    DOGNAME = "${PROCESS_NAME}_dog.sh"
echo
"set watchdog to $DOGNAME"
if [-f "$DOGNAME"];
then
return 0
fi
(
    cat << EOF
# !/bin/bash
# Teach wisedom to my machine
# zhangtao
# watch dog
# watchdog.sh

APPNAME = server.sh

while (true)
    do
    ./ server.sh
    monit
    sleep
    10
done
EOF
) > $DOGNAME
chmod
777
"$DOGNAME"
}

function
setServerDumpLog()
{
if [-z "$SERVER_LOG_DIR"];
then
if [ ! -d
"log"];then
mkdir
log
fi
return 1
fi

MYSERVER_LOG_DIR = "${SERVER_LOG_DIR}/${PROCESS_NAME}"
if [-d "$MYSERVER_LOG_DIR"] ;then
echo
"server_log_dir is $MYSERVER_LOG_DIR"
else
mkdir - p
"$MYSERVER_LOG_DIR"
echo
"create server_log_dir as: $MYSERVER_LOG_DIR"
fi

if [ ! -d "log"];then
ln - s
"$MYSERVER_LOG_DIR"
log
fi
}




function
excuteCmdAndreportLog()
{
`eval $@


`
logMessage $@

}


function
running()
{
if [-f "$RUN_DIR/$PID_FILE"]; then
pid =$(cat
"$RUN_DIR/$PID_FILE")
if [-z "$pid"] ;then
return 1
fi

pidlist = `pidof
"$PROCESS_NAME"
`
if [-z "$pidlist"] ;then
return 1
fi

if [["$pidlist" =~  "$pid"]];then
return 0
else
return 1
fi
else
return 1
fi
}



function
start_server()
{
setProcessName
setServerDumpLog
if running ;then
logMessage
"$PROCESS_NAME is running ..."
exit
1
fi
setWatchDog
logMessage
"----------------------------------> start_server    $PROCESS_NAME "
logMessage
"nohup $BIN_DIR/$PROCESS_NAME  2>&1 1>&/dev/null  &"
export
LD_LIBRARY_PATH =$LIB_DIR:$LD_LIBRARY_PATH
echo $LIB_DIR
chmod
a + x $BIN_DIR /$PROCESS_NAME
nohup $BIN_DIR /$PROCESS_NAME
2 > & 1
1 > & / dev / null &
echo $! > $RUN_DIR /$PID_FILE
excuteCmdAndreportLog
"chmod 777 $RUN_DIR/$PID_FILE"
sleep
2
if running ;then
logMessage
"$PROCESS_NAME is running ...   "
exit
1
fi
logMessage
"$PROCESS_NAME start failed !"
}


function
start_server_only()
{
if running ;then
logMessage
"$PROCESS_NAME is running ..."
exit
1
fi
logMessage
"----------------------------------> start_server    $PROCESS_NAME "
logMessage
"nohup $BIN_DIR/$PROCESS_NAME  2>&1 1>&/dev/null  &"
export
LD_LIBRARY_PATH =$LIB_DIR:$LD_LIBRARY_PATH
echo $LIB_DIR
chmod
a + x $BIN_DIR /$PROCESS_NAME
nohup $BIN_DIR /$PROCESS_NAME
2 > & 1
1 > & / dev / null &
echo $! > $RUN_DIR /$PID_FILE
excuteCmdAndreportLog
"chmod 777 $RUN_DIR/$PID_FILE"
sleep
2
if running ;then
logMessage
"$PROCESS_NAME is running ...   "
exit
1
fi
logMessage
"$PROCESS_NAME start failed !"
}


function
stop_server()
{
if ! running;then
logMessage
"$PROCESS_NAME was not running"
exit
1
fi

DOGNAME = "${PROCESS_NAME}_dog.sh"
DOGPID = `ps - ef | egrep - i
"bash" | egrep - i
"$DOGNAME" | egrep - v
"egrep" | awk
'{print $2}'
`
if [-n "$DOGPID"] ;then
logMessage
"$DOGNAME Work at $DOGPID"
excuteCmdAndreportLog
"kill -9 $DOGPID"
fi

count = 0
pid =$(cat $RUN_DIR /$PID_FILE)
while running; do
let
count =$count + 1
logMessage
"stopping $PROCESS_NAME $count times !!!"
if [ $count -gt 5];then
excuteCmdAndreportLog
"kill -9 $pid"
else
sleep
1
excuteCmdAndreportLog
"kill  $pid"
fi
sleep
2
done
logMessage
"-----------> stop $PROCESS_NAME successfully <------------"
excuteCmdAndreportLog
"rm $RUN_DIR/$PID_FILE"
}

function
monit_server()
{
if running ;then
exit
1
fi
start_server_only $@

}

function
status()
{
if running; then
logMessage
"$PROCESS_NAME is running.";
exit
0;
else
logMessage
"$PROCESS_NAME was stopped.";
exit
1;
fi
}



function
help()
{
echo
"------------------------------------------------------------------------------"
echo
"Usage: server.sh {start|status|stop|restart|logback}" > & 2
echo
"       start:             start the $PROCESS_NAME server"
echo
"       stop:              stop the $PROCESS_NAME server"
echo
"       monit:             monit the $PROCESS_NAME server"
echo
"       restart:           restart the $PROCESS_NAME server"
echo
"       logback:           reload logback config file"
echo
"       status:            get $PROCESS_NAME current status,running or stopped."
echo
"-----------------------------------------------------------------------------"
}

function
getOpts()
{
command =$1
shift
1
case $command in
start)
start_server $@

;
;;
stop)
stop_server $@

;
;;
logback)
reload_logback_config $@

;
;;
status)
status $@

;
;;
monit)
monit_server $@

;
;;
restart)
$0
stop $@

$0
start $@

;;
help)
help;
;;
* )
help;
exit
1;
;;
esac
}

function
main()
{
    setEnv $@
setProcessName


0
getOpts $@

}



main $@
