//
// Created by Admin on 2018/3/27.
//


#include <com_example_admin_jni_demo_JniTest.h>

//自定义log
#include <Android/log.h>

#define TAG "[jnitest]"
#define LOGI(...) __android_log_print(ANDROID_LOG_INFO, TAG, __VA_ARGS__)
#define LOGD(...) __android_log_print(ANDROID_LOG_DEBUG, TAG, __VA_ARGS__)
#define LOGE(...) __android_log_print(ANDROID_LOG_ERROR, TAG, __VA_ARGS__)


JNIEXPORT jstring JNICALL Java_com_example_admin_jni_1demo_JniTest_getStrFromC
  (JNIEnv * env, jclass class1)
{
    char* str_name="hello word from C";
    LOGE("the name from java is %s", str_name);
    char * p= NULL;

    //*p=1;

    jstring str= (*env)->NewStringUTF(env, str_name);
    return str;
}