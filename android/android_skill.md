
# 查看和报告android issue #

    https://source.android.com/source/report-bugs

# adb pull/push #

    (1)adb pull /sdcard/mine.jpg  c:/Temp/mine.jpg  #将sdcard中的一个mine.jpg 拷贝到PC
    
    (2)adb pull  /system  c:\Temp     #将/system文件夹整个拷贝到PC的temp目录,注意PC路径用\

# logcat #

    参考：https://blog.csdn.net/mayingcai1987/article/details/6364657

- 显示某一TAG的某一级别的日志信息
    
        格式：adb logcat TAG名称:级别.....TAG名称：级别 *:S
        如： logcat -s update_engine:v  

# 查看linux系统应用的源码 #
    
    如adb, ls等，一般放在system/bin和/sbin下面，我们可以通过adb shell来执行这些命令。 

    这些命令的源代码保存在/android/system/core/目录下，
    如mount命令对应的源代码是/android/system/core/toolbox/mount.c
    Top命令对应top.c
    
    如果root了，这个目录下会有su

# 查看运行的service及其包名 #

    Adb shell service list
    如：media_session: [android.media.session.ISessionManager]

    检查service是否存在：adb shell service check phone //phone是service名

# 查看、设置、监视属性 #

    getprop  [propertyName]       #查看名为 propertyName 的属性的值，不加参数执行 getprop 将列出所有属性值。
    getprop  |  grep  -i  audio  #查看音频属性配置情况。
    
    或 cat /system/build.prop
    
    监视系统属性
    watchprops  <propertyName>  #监视名为 propertyName 的属性的值，当其数值发生变化时将最新的属性值实时打印出来。
    
    设置系统属性
    setprop  <propertyName>  <value> #将名为 propertyName 的属性的值设置为 value。
    
# 查看应用的包名和安装位置 #

    adb shell pm list packages -f
    
    package:/system/app/com.qualcomm.qti.services.secureui/com.qualcomm.qti.services.secureui.apk=
            com.qualcomm.qti.services.secureui

    dex2oat

    https://blog.csdn.net/sumin_fushengruocha/article/details/51147776
    https://blog.csdn.net/roland_sun/article/details/50234551

# Android studio #

- 重命名文件：Shift+F6

    选中你要重命名的文件（pic.PNG），在“Refactor”选项中有Rename

- 参数提示：CTRL+Q

- 当出现没有引入包名导致的错误时，alt+enter 自动提示和引入需要添加的包名

- 查看引入的第三方开源库的路径
        file-> project structure -> Modules下的app-> dependencies引入的第三方库， 
        这些库在项目路径\.idea\libraries里有定义，一般指向.gradle文件夹：
        C:\Users\Admin\.gradle\caches\modules-2\files-2.1

- 修改最小SDK版本

        build.gradle文件中：
        defaultConfig {
            minSdkVersion 21
        }

# app开发 #


# HAL #

- Android下使用dlopen函数动态调用.so链接库

        p=dlopen("./dl2.so",RTLD_NOW);
        func=dlsym(p,"max");
        printf("%d与%d相比，%d为大数。\n",a,b,(*func)(a,b));
        dlclose(p);
        
        参考：http://blog.csdn.net/hdhd588/article/details/6922202
