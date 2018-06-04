
package com.example.admin.jni_demo; // include package name

public class JniTest {
    public static native String getStrFromC();

    static {
        System.loadLibrary("jnitest_Lib"); //to be loaded lib: lib.so
    }
}