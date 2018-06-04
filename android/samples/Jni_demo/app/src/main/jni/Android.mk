# 设置当前的编译目录（Android.mk所在的目录）
LOCAL_PATH := $(call my-dir)

#-----lib 1--------------
# 清除LOCAL_XX变量（LOCAL_PATH除外）
include $(CLEAR_VARS)

# 添加调试信息for gdb
LOCAL_CFLAGS += -g

# 链接log库
LOCAL_LDLIBS :=-llog

# 指定当前编译模块的名称
LOCAL_MODULE := jnitest_Lib

# 编译模块需要的源文件
LOCAL_SRC_FILES := jnitest.c

# 指定编译出的库类型，BUILD_SHARED_LIBRARY：动态库；BUILD_STATIC_LIBRARY：静态库， BUILD_EXECUTEABLE指：可执行文件
include $(BUILD_SHARED_LIBRARY)

#-----lib 2--------------