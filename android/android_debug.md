# adb #

    ubuntu上adb不能识别到手机：
    lsusb后
    加入到：/etc/udev/rules.d$ sudo vi 70-android.rules

# bugreport #

    adb bugreport > br1.txt
    ==> 在当前目录下生成br1.txt以及对应的bugreport***.zip
    从br1.txt里可以看到bugreport文件在device中的路径

    adb bugreport br1
    ==> 在当前目录下生成br1.zip


    将 wear os产生的bugreport导出：
    adb pull /data/user_de/0/com.google.android.apps.wearable.bugreportsender/cache ~/xxl/tmp/
    bugreport会打包以下目录：
    /data/misc/logd
    往上面的目录push文件：
    adb root
    adb push /home/mobvoi/xxl/issues/crash_after_do_bugreport/test/* /data/misc/logd
    

- 系统属性

        bugreport中：
        SYSTEM PROPERTIES (getprop)

- 系统分区的情况

        ------ FILESYSTEMS & FREE SPACE (df) ------
        Filesystem                                             1K-blocks   Used Available Use% Mounted on
        rootfs                                                    443408   3088    440320   1% /
        tmpfs                                                     458816    668    458148   1% /dev
        /dev/block/platform/soc/7824900.sdhci/by-name/system     1257344 639240    588616  53% /system
        /dev/block/platform/soc/7824900.sdhci/by-name/vendor      261856 135116    118880  54% /vendor
        tmpfs                                                     458816      0    458816   0% /mnt
        /dev/block/mmcblk0p24                                      60400     56     59036   1% /cache
        /dev/block/platform/soc/7824900.sdhci/by-name/modem       131008  52256     78752  40% /firmware
        /dev/block/platform/soc/7824900.sdhci/by-name/oem          11760     44     11232   1% /oem
        /dev/block/platform/soc/7824900.sdhci/by-name/userdata   1776480 464972   1295124  27% /data
        /data/media                                              1776480 464972   1295124  27% /storage/emulated

        ------ VOLD DUMP (vdc dump) ------
        0 23661 Dumping loop status
        0 23661 Dumping DM status
        0 23661 Dumping mounted filesystems
        0 23661 rootfs / rootfs ro,seclabel,size=443408k,nr_inodes=110852 0 0
        0 23661 tmpfs /dev tmpfs rw,seclabel,nosuid,relatime,size=458816k,nr_inodes=114704,mode=755 0 0
        0 23661 devpts /dev/pts devpts rw,seclabel,relatime,mode=600 0 0
        0 23661 proc /proc proc rw,relatime,gid=3009,hidepid=2 0 0
        0 23661 sysfs /sys sysfs rw,seclabel,relatime 0 0
        0 23661 selinuxfs /sys/fs/selinux selinuxfs rw,relatime 0 0
        0 23661 /dev/block/platform/soc/7824900.sdhci/by-name/system /system ext4 ro,seclabel,relatime,data=ordered 0 0
        0 23661 /dev/block/platform/soc/7824900.sdhci/by-name/vendor /vendor ext4 ro,seclabel,relatime 0 0
        0 23661 debugfs /sys/kernel/debug debugfs rw,seclabel,relatime 0 0
        0 23661 none /acct cgroup rw,relatime,cpuacct 0 0
        0 23661 tmpfs /mnt tmpfs rw,seclabel,relatime,size=458816k,nr_inodes=114704,mode=755,gid=1000 0 0
        0 23661 none /config configfs rw,relatime 0 0
        0 23661 none /dev/memcg cgroup rw,relatime,memory 0 0
        0 23661 none /dev/cpuctl cgroup rw,relatime,cpu 0 0
        0 23661 pstore /sys/fs/pstore pstore rw,seclabel,relatime 0 0
        0 23661 /dev/block/platform/soc/7824900.sdhci/by-name/cache /cache ext4 rw,seclabel,nosuid,nodev,noatime,data=ordered 0 0
        0 23661 /dev/block/platform/soc/7824900.sdhci/by-name/persist /persist ext4 rw,seclabel,nosuid,nodev,noatime,data=ordered 0 0
        0 23661 /dev/block/platform/soc/7824900.sdhci/by-name/modem /firmware vfat ro,context=u:object_r:firmware_file:s0,relatime,uid=1000,gid=1000,fmask=0337,dmask=0227,codepage=437,iocharset=iso8859-1,shortname=lower,errors=remount-ro 0 0
        0 23661 /dev/block/platform/soc/7824900.sdhci/by-name/oem /oem ext4 ro,context=u:object_r:oemfs:s0,nosuid,nodev,relatime,data=ordered 0 0
        0 23661 tmpfs /storage tmpfs rw,seclabel,relatime,size=458816k,nr_inodes=114704,mode=755,gid=1000 0 0
        0 23661 adb /dev/usb-ffs/adb functionfs rw,relatime 0 0
        0 23661 /dev/block/platform/soc/7824900.sdhci/by-name/userdata /data ext4 rw,seclabel,nosuid,nodev,noatime,discard,noauto_da_alloc,data=ordered 0 0
        0 23661 /data/media /mnt/runtime/default/emulated sdcardfs rw,nosuid,nodev,noexec,noatime,fsuid=1023,fsgid=1023,gid=1015,multiuser,mask=6,derive_gid 0 0
        0 23661 /data/media /storage/emulated sdcardfs rw,nosuid,nodev,noexec,noatime,fsuid=1023,fsgid=1023,gid=1015,multiuser,mask=6,derive_gid 0 0
        0 23661 /data/media /mnt/runtime/read/emulated sdcardfs rw,nosuid,nodev,noexec,noatime,fsuid=1023,fsgid=1023,gid=9997,multiuser,mask=23,derive_gid 0 0
        0 23661 /data/media /mnt/runtime/write/emulated sdcardfs rw,nosuid,nodev,noexec,noatime,fsuid=1023,fsgid=1023,gid=9997,multiuser,mask=7,derive_gid 0 0


# dumpstate #

    // Start the dumpstate service.
    property_set("ctl.start", "dumpstate");

# logcat #

    adb logcat -v time -s xxx yyy
    ==>按tag过滤出xxx或yyy的log

    adb logcat | grep -i xxx
    => 只显示xxx相关的log
    https://www.cnblogs.com/bydzhangxiaowei/p/8168598.html

# ANR #

	ANR: Application not responding
	当检查到ANR时，触发signal 6(SIGABORT)终止未响应的应用
	
	原因：
	
	1）应用主线程卡住，对其他请求响应超时。
		(1）应用程序在5s内不能响应touch等输入事件
		(2）广播接收器在10s内部不能执行完（如果是后台广播，时间是60s)
		(3) service或contentprovider在10s内不能执行完
	2）死锁。
	3）系统反应迟钝。
	4）CPU负载过重。
	
	如果不能弹出ANR框，那有可能是framework层发生了问题，比如在activityManager或windowManager上发生了deadlock,这最终会导致watchdog timeout.

	anr时产生的trace log保存在： /data/anr/traces.txt

# Force Close(FC) #

	发生场景：应用进程崩溃。
	崩溃症状：系统弹出窗口提示用户某进程崩溃。
	发生原因：空指向异常或者未捕捉的异常。
	
# 系统服务崩溃 #

	发生场景：系统服务是Android核心进程，此服务进程发生崩溃。
	崩溃症状：手机重启到Android启动界面

	发生原因：
	1）系统服务看门狗发现异常 Watchdog timeout
	
		参考： https://blog.csdn.net/fu_kevin0606/article/details/64479489
		
		android watchdog每30s检查重要的service在1分钟内是否有响应：
		Activity Manager Service, Window Manager Service, and Power Manager Service
		
		Watchdog原理：
		(1）尝试获取系统service的lock，看1分钟内是能否成功
		(2）检查主线程的looper里的pending message在1分钟内是否还没处理完
		
		原因： 通常是重要service的某些线程间存在deadlock
	
	2）系统服务发生未捕获异常。
	3）OOM。
	4）系统服务Native发生Tombstone。

# Java层异常 #

	java 层打印callstack 可以通过 catch exception 然后使用：
	Log.w(LOGTAG, Log.getStackTraceString(throwable)) 打印调用堆栈
		
		如：
			Throwable throwable = new Throwable();	
			Log.w(LOGTAG, Log.getStackTraceString(throwable));

		或者：
			try {  
				wait();  
			} catch (InterruptedException e) {  
				Log.e(LOGTAG, "Caught exception while waiting for overrideUrl");  
				Log.e(LOGTAG, Log.getStackTraceString(e));  
			}  

# Android crash 原因 #

	参考
	https://blog.csdn.net/u011686167/article/details/52733414
	https://blog.csdn.net/u011686167/article/details/52738255
	
# 分析Tombstone #

只有native的代码发异常才会产生tombstone。

		backtrace信息如：

		I/DEBUG   (  241): backtrace:
		I/DEBUG   (  241):	 #00 pc 00028fa8  /system/lib/libc.so (dlfree+1239)
		I/DEBUG   (  241):	 #01 pc 0000f2cb  /system/lib/libc.so (free+10)
		I/DEBUG   (  241):	 #02 pc 0000a1cb  /system/lib/libstagefright_foundation.so (_ZN7android7ABufferD2Ev+42)
		I/DEBUG   (  241):	 #03 pc 0000a211  /system/lib/libstagefright_foundation.so (_ZN7android7ABufferD0Ev+4)
		I/DEBUG   (  241):	 #04 pc 0000d68d  /system/lib/libutils.so (_ZNK7android7RefBase9decStrongEPKv+40)
		I/DEBUG   (  241):	 #05 pc 0005adfd  /system/lib/libstagefright.so (_ZN7android2spINS_13GraphicBufferEED2Ev+10)
		I/DEBUG   (  241):	 #06 pc 0007cd0f  /system/lib/libstagefright.so (_ZN7android14MPEG4Extractor10parseChunkEPxi+634)
		I/DEBUG   (  241):	 #07 pc 0007d43d  /system/lib/libstagefright.so (_ZN7android14MPEG4Extractor10parseChunkEPxi+2472)


- 参考

		Android Tombstone 分析：
		https://www.cnblogs.com/CoderTian/p/5980426.html
		
		跟踪Android callback 调用堆栈
		https://blog.csdn.net/hellowxwworld/article/details/10720765

分析方法有：

- 1） addr2line： 对单个地址获取源码行号

		addr2line 是用来获得指定动态链接库文件或者可执行文件中指定地址对应的源代码信息的工具.

		使用说明：
		  Usage: aarch64-linux-android-addr2line.exe [option(s)] [addr(s)]
			 Convert addresses into line number/file name pairs.
			 If no addresses are specified on the command line, they will be read from stdin
			 The options are:
			  @<file>				Read options from <file>
			  -a --addresses		 Show addresses
			  -b --target=<bfdname>  Set the binary file format
			  -e --exe=<executable>  Set the input file name (default is a.out)
			  -i --inlines		   Unwind inlined functions
			  -j --section=<name>	Read section-relative offsets instead of addresses
			  -p --pretty-print	  Make the output easier to read for humans
			  -s --basenames		 Strip directory names
			  -f --functions		 Show function names
			  -C --demangle[=style]  Demangle function names
			  -h --help			  Display this information
			  -v --version		   Display the program's version

	
		用法：
	
			cd ./prebuilts/gcc/linux-x86/arm/arm-linux-androideabi-4.8/bin/
			arm-linux-androideabi-addr2line -f -e out/debug/target/product/XXXX/symbols/system/lib/libstagefright.so  0007cd0f<出错时的pc>
			
			或者用NDK里的windows版aarch64-linux-android-addr2line.exe

			输出：
			_ZN7android14MPEG4Extractor10parseChunkEPxi
			/home/XXX/source/XXX/LINUX/android/frameworks/av/media/libstagefright/MPEG4Extractor.cpp:2180 (discriminator 1)
		
		注意：
		（1) libstagefright.so 是要包含调试符号信息的，即是debug版本（有的release版本中会剥离debug信息）。
		具体的说是要保证以下2点：

			(a) 修改 android.mk，增加，为 LOCAL_CFLAGS 增加 -g 选项
			(b) 修改 application.mk，增加 APP_OPTIM := debug

		(2）可以在windows和linux运行对应版本的ddr2line.exe，但是工具链必须与编译SO库时的架构一样（arm是芯片架构，linux是操作系统）


- 2）**ndk-stack**：对所有的backtrace行输出对应的源码行号 (推荐）

		官方参考：https://developer.android.com/ndk/guides/ndk-stack.html

		Android NDK 自从版本 r6开始, 提供了一个工具 ndk-stack
		这个工具能自动分析 tombstone 文件, 将崩溃时的调用内存地址和 c++ 代码一行一行对应起来.

		代码位于：/ndk/sources/host-tools/ndk-stack/ndk-stack.c
		在NDK中的路径：\Sdk\ndk-bundle\prebuilt\windows-x86_64\bin\ndk-stack.exe
		
		使用说明：
			Usage:
			   ndk-stack -sym <path> [-dump <path>]
			
				  -sym  Contains full path to the root directory for symbols.
				  -dump Contains full path to the file containing the crash dump.
						This is an optional parameter. If ommited, ndk-stack will
						read input data from stdin
			
			   See docs/NDK-STACK.html in your NDK installation tree for more details.

			（1）dump 参数: dump下来的log文件或tombstone文件.
			（2）sym 参数: android项目下编译成功之后，system debug so库的所在的目录，注意要带有符号信息编译.

		例如，分析tombstone_01.txt：
			ndk-stack -sym debug-so_path/ -dump tombstone_01.txt

		此外，在调试android系统源码的时候也可以直接分析log中的crash信息：
			adb shell logcat | ndk-stack -sym out/debug/target/product/XXXX/symbols/system/lib/xxx.so


- 3）stack.py： 对所有的backtrace行输出对应的源码行号

		stack.py工具就是要把backtrace通过addr2line工具一次性把addr对应到代码。
		但没有找到这个脚本的出处。

		使用方法：
			python stack.py --symbols-dir=out/target/profuct/XXX/sysbols/  tombstone-00(tombstone文件)

# Native的memory leak #

	(1) gcc 带-g编译 test.c
	(2) ENG版本，并adb shell setprop libc.debug.malloc 10  (1不起作用)
	(3) adb shell 后run test。之后用adb shell logcat >test_leak_log.txt得到log.

	如果有leak会打出以下log, 然后用addrline工具来定位到具体的代码行。
	I/libc	( 3500): ./data/O5_xxl_test_leak: using libc.debug.malloc 10 (chk)
	E/libc	( 3500): +++ /data/O5_xxl_test_leak leaked block of size 40 at 0xb6c2c200 (leak 1 of 1)
	E/libc	( 3500): *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
	E/libc	( 3500):		   #00  pc 00006f68  /system/lib/libc_malloc_debug_leak.so (chk_malloc+71)
	E/libc	( 3500):		   #01  pc 00012842  /system/lib/libc.so (malloc+9)
	E/libc	( 3500):		   #02  pc 00000348  /data/O5_xxl_test_leak

# NDK调试native程序 #

# LLDB调试native程序 #

	参考
	http://lldb.llvm.org/lldb-gdb.html


# Native tracing #

	https://developer.android.com/ndk/guides/tracing.html

	use the native tracing API (trace.h) to write trace events to the system buffer.
	You can then analyze this trace output by using the Systrace tool.
	The native tracing API is supported for Android API levels 23 and higher. 