###################################################
#Teach Wisedom to My Machine
#       Please Call me Devil
#
CC         := g++
ROOT_DIR   := $(shell pwd)
SRC_DIR    := $(ROOT_DIR)/src
LIB_DIR    := $(ROOT_DIR)/lib
INC_DIR    := $(ROOT_DIR)/include

INC_DIR    += $(ROOT_DIR)/common/include
INC_DIR    += $(ROOT_DIR)/common/common/include
INC_DIR    += $(ROOT_DIR)/common/corebase/include
INC_DIR    += $(ROOT_DIR)/common/thirdparty_include
INC_DIR    += $(ROOT_DIR)/protocol

INSTALL_PATH := $(ROOT_DIR)/bin/

SRC_FILES  := $(wildcard $(SRC_DIR)/*.cpp)
OBJ_FILES  := $(SRC_FILES:.cpp=.o)
LD_LIBS    :=  corebase net rt common2 dbpool mysqlclient_r pthread  hiredis curl json

######################################################################
#		 LIB				                       #
######################################################################
#LIB_NAME   := openapi
#LIB_SUFFIX := .a
#LIB_TARGET := lib$(LIB_NAME)$(LIB_SUFFIX)

APP_NAME	:= grpchatdbg_dev
APP_SUFFIX	:=
APP_TARGET	:= $(APP_NAME)$(APP_SUFFIX)

.PHONY: all clean

#LDFLAGS    := -m32 -L$(LIB_DIR) $(addprefix -l,$(LD_LIBS))
LDFLAGS    :=  -L$(LIB_DIR) $(addprefix -l,$(LD_LIBS))
CFLAGS     :=  -O2  -Werror -DTRACE_LOG -Wno-deprecated  -Wformat=0   -I$(SRC_DIR) $(addprefix -I,$(INC_DIR))
#CFLAGS     := -m32 -O2  -Werror -DTRACE_LOG -DNS_CONNECT_APSVR -I$(SRC_DIR) $(addprefix -I,$(INC_DIR))

#ifeq ($(DEBUG),yes)
CFLAGS     += -ggdb2 -D__DEBUG
#endif

all: $(APP_TARGET);

$(APP_TARGET): $(OBJ_FILES)
	$(CC) -o $(APP_TARGET) $(CFLAGS) $(OBJ_FILES) $(LDFLAGS)
	@echo *********Build $@ $(APP_TARGET:.a=.so) Successful*********
	@echo

%.o: %.cpp
	$(CC) $(CFLAGS) -c $< -o $@


install:
	@echo install...
	cp $(APP_TARGET) ../update -r
	cp $(APP_TARGET) $(INSTALL_PATH)$(APP_TARGET) -r

clean:
	@echo clean...
	@rm -rf $(APP_TARGET) $(LIB_TARGET) $(LIB_TARGET:.a=.so) $(OBJ_FILES) $(LIB_TARGET:.a=.bin) *.log


