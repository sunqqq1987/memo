
# android 源码下载和编译 #

	参考
	https://www.jianshu.com/p/367f0886e62b

	https://mirrors.tuna.tsinghua.edu.cn/help/AOSP/

	使用清华大学的AOSP镜像：
	将 https://android.googlesource.com/ 替换为 https://aosp.tuna.tsinghua.edu.cn/

- 1.下载 repo 工具

		mkdir ~/bin
		PATH=~/bin:$PATH

		// curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
		=>使用： curl https://mirrors.tuna.tsinghua.edu.cn/git/git-repo -o ~/bin/repo
		chmod a+x ~/bin/repo

		将 ~/bin加到PATH环境变量里:
			vi ~/.bashrc
			添加：PATH=~/bin:$PATH
			source ~/.bashrc  //不重启，使得PATH生效

		repo的使用，参考： https://blog.csdn.net/ican87/article/details/20726151
		
- 2.安装OPENJDK8

		sudo apt-get install openjdk-8-jdk

- 3.安装Ubuntu16.04中的依赖

		sudo apt-get install libx11-dev:i386 libreadline6-dev:i386 libgl1-mesa-dev g++-multilib 
		sudo apt-get install -y git flex bison gperf build-essential libncurses5-dev:i386 
		sudo apt-get install tofrodos python-markdown libxml2-utils xsltproc zlib1g-dev:i386 
		sudo apt-get install dpkg-dev libsdl1.2-dev libesd0-dev
		sudo apt-get install git-core gnupg flex bison gperf build-essential  
		sudo apt-get install zip curl zlib1g-dev gcc-multilib g++-multilib 
		sudo apt-get install libc6-dev-i386 
		sudo apt-get install lib32ncurses5-dev x11proto-core-dev libx11-dev 
		sudo apt-get install libgl1-mesa-dev libxml2-utils xsltproc unzip m4
		sudo apt-get install lib32z-dev ccache

- 4.使用每月更新的初始化包

		由于首次同步需要下载约 30GB 数据，过程中任何网络故障都可能造成同步失败，我们强烈建议您使用初始化包进行初始化。
		
		1）wget -c https://mirrors.tuna.tsinghua.edu.cn/aosp-monthly/aosp-latest.tar # 下载初始化包

		2) vi ~/bin/repo, 将REPO_URL这一行修改为：
			REPO_URL = 'https://gerrit-google.tuna.tsinghua.edu.cn/git-repo'

		3）tar xf aosp-latest.tar

			注意：如果是在虚拟机上，要先对虚拟机扩容

		4）cd AOSP   # 解压得到的 AOSP 工程目录. 这时 ls 的话什么也看不到，因为只有一个隐藏的 .repo 目录

		获取指定
		repo init -u https://aosp.tuna.tsinghua.edu.cn/platform/manifest -b android-8.1.0_r2 
		repo sync # 正常同步一遍即可得到完整目录

		其他：
		repo info: 获取当前的android branch
			sam@ubuntu:~/aosp$ repo info
			Manifest branch: refs/tags/android-8.1.0_r2
			Manifest merge branch: refs/heads/android-8.1.0_r2
			Manifest groups: all,-notdefault
			----------------------------
			Project: platform/art
			Mount path: /home/sam/aosp/art
			Current revision: refs/tags/android-8.1.0_r2
			Local Branches: 0

		repo branches：查看分支状态
		repo start/checkout/abandon/prune：创建/切换/删除/整理分支
	

- 5.编译

		注意： vmware虚拟机的内存至少12G, 否则会出现内存不足的编译错误

		命令：
		source build/envsetup.sh
		lunch aosp_arm64-eng
		make -j4
		
		数小时后，生成以下image:
			sam@ubuntu:~/aosp$ ls out/target/product/generic_arm64/*.img -l
			-rw-r--r-- 1 sam sam   69206016 May 19 05:06 out/target/product/generic_arm64/cache.img
			-rw-rw-r-- 1 sam sam    1117950 May 19 06:33 out/target/product/generic_arm64/ramdisk.img
			-rw-r--r-- 1 sam sam 2684354560 May 19 06:36 out/target/product/generic_arm64/system.img
			-rw-rw-r-- 1 sam sam 2686451712 May 19 06:37 out/target/product/generic_arm64/system-qemu.img
			-rw-r--r-- 1 sam sam  576716800 May 19 06:25 out/target/product/generic_arm64/userdata.img
			-rw-r--r-- 1 sam sam   99999744 May 19 06:35 out/target/product/generic_arm64/vendor.img
			-rw-rw-r-- 1 sam sam  102760448 May 19 06:36 out/target/product/generic_arm64/vendor-qemu.img

		编译后的target目录：
		sam@ubuntu:~/aosp/out/target/product/generic_arm64$ ls -l
			total 3993932
			-rw-rw-r--  1 sam sam         85 May 17 08:03 advancedFeatures.ini
			-rw-rw-r--  1 sam sam          7 May 17 08:00 android-info.txt
			-rw-rw-r--  1 sam sam         81 May 19 03:55 build_fingerprint.txt
			drwxrwxr-x  2 sam sam       4096 May 19 05:06 cache  //貌似是空的
			-rw-r--r--  1 sam sam   69206016 May 19 05:06 cache.img
			-rw-r--r--  1 sam sam     524288 May 19 07:33 cache.img.qcow2
			-rw-rw-r--  1 sam sam      91766 May 18 07:44 clean_steps.mk
			-rw-rw-r--  1 sam sam        380 May 17 08:03 config.ini
			drwxrwxr-x  7 sam sam       4096 May 19 07:15 data
			drwxrwxr-x  3 sam sam       4096 May 17 10:55 dex_bootjars
			drwxrwxr-x  2 sam sam       4096 May 19 06:35 fake_packages
			drwxrwxr-x  6 sam sam       4096 May 17 09:13 gen
			-rw-rw-r--  1 sam sam       1842 May 19 07:16 hardware-qemu.ini
			-rw-rw-r--  1 sam sam     373790 May 19 06:36 installed-files.json
			-rw-rw-r--  1 sam sam     119093 May 19 06:36 installed-files.txt
			-rw-rw-r--  1 sam sam      52689 May 19 06:35 installed-files-vendor.json
			-rw-rw-r--  1 sam sam      15569 May 19 06:35 installed-files-vendor.txt
			-rw-rw-r--  1 sam sam    7747584 May 17 08:03 kernel-ranchu
			-rw-rw-r--  1 sam sam    3314980 May 17 08:00 module-info.json
			drwxrwxr-x 17 sam sam       4096 May 19 06:35 obj
			drwxrwxr-x  9 sam sam       4096 May 17 08:05 obj_arm
			-rw-rw-r--  1 sam sam         40 May 17 07:30 previous_build_config.mk
			-rw-rw-r--  1 sam sam    1117950 May 19 06:33 ramdisk.img
			drwxrwxr-x  3 sam sam       4096 May 17 07:47 recovery
			drwxrwxr-x 16 sam sam       4096 May 19 06:33 root  //ramdisk的文件
			drwxrwxr-x  8 sam sam       4096 May 19 05:57 symbols
			drwxrwxr-x 16 sam sam       4096 May 19 06:36 system //system的目录
			-rw-r--r--  1 sam sam 2684354560 May 19 06:36 system.img
			-rw-rw-r--  1 sam sam 2686451712 May 19 06:37 system-qemu.img
			-rw-r--r--  1 sam sam     196656 May 19 07:16 system-qemu.img.qcow2
			-rw-r--r--  1 sam sam  576716800 May 19 06:25 userdata.img
			-rw-r--r--  1 sam sam 2147483648 May 19 07:16 userdata-qemu.img
			-rw-r--r--  1 sam sam  106233856 May 19 07:33 userdata-qemu.img.qcow2
			drwxrwxr-x  7 sam sam       4096 May 19 06:01 vendor  //与具体odm有关的HAL
			-rw-r--r--  1 sam sam   99999744 May 19 06:35 vendor.img
			-rw-rw-r--  1 sam sam  102760448 May 19 06:36 vendor-qemu.img
			-rw-r--r--  1 sam sam     196616 May 19 07:16 vendor-qemu.img.qcow2
			-rw-rw-r--  1 sam sam          3 May 19 07:16 version_num.cache
			
			Android系统自带的apk文件都在out/target/product/generic_arm64/system/apk目录下;
			一些可执行文件(比如C编译的执行),放在out/target/product/generic_arm64/system/bin目录下;
			动态链接库放在out/target/product/generic_arm64/system/lib目录下;
			硬件抽象层文件都放在out/targer/product/generic_arm64/system/lib/hw目录下.

	- 模块编译
		
		
- 6.运行模拟器

		在编译完成之后,就可以通过以下命令运行Android虚拟机了,命令如下:
		
		source build/envsetup.sh
		lunch aosp_arm64-eng
		emulator


# 查看和报告android issue #

	https://source.android.com/source/report-bugs

# adb pull/push #

    (1)adb pull /sdcard/mine.jpg  c:/Temp/mine.jpg  #将sdcard中的一个mine.jpg 拷贝到PC
    
    (2)adb pull  /system  c:\Temp 	#将/system文件夹整个拷贝到PC的temp目录,注意PC路径用\

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

	getprop  [propertyName]  	 #查看名为 propertyName 的属性的值，不加参数执行 getprop 将列出所有属性值。
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
