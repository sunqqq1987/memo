# aosp 源码下载和编译 #

    参考
    https://www.jianshu.com/p/367f0886e62b

    https://mirrors.tuna.tsinghua.edu.cn/help/AOSP/

    使用清华大学的AOSP镜像：
    将 https://android.googlesource.com/ 替换为 https://aosp.tuna.tsinghua.edu.cn/


- 1.安装Ubuntu16.04中的依赖

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

- 2.下载 repo 工具

        mkdir ~/bin

        PATH=~/bin:$PATH
        或者：将 ~/bin加到PATH环境变量里:
            vi ~/.bashrc
            添加：PATH=~/bin:$PATH
            source ~/.bashrc  //不重启，使得PATH生效

        // curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
        =>使用： curl https://mirrors.tuna.tsinghua.edu.cn/git/git-repo -o ~/bin/repo

        chmod a+x ~/bin/repo
        
- 3.安装OPENJDK8

        sudo apt-get install openjdk-8-jdk

- 4.下载android code

        
        方法1: 使用每月更新的初始化包

        由于首次同步需要下载约 30GB 数据，过程中任何网络故障都可能造成同步失败，我们强烈建议您使用初始化包进行初始化。
        
        1）wget -c https://mirrors.tuna.tsinghua.edu.cn/aosp-monthly/aosp-latest.tar  //下载初始化包

        2) vi ~/bin/repo, 将REPO_URL这一行修改为：
            REPO_URL = 'https://gerrit-google.tuna.tsinghua.edu.cn/git-repo'

        3）tar xf aosp-latest.tar  //可以省略，用4）即可

            注意：如果是在虚拟机上，要先对虚拟机扩容

            解压后得到的 AOSP 工程目录. 
            这时 ls 的话什么也看不到，因为只有一个隐藏的 .repo 目录

            repo sync -j8 //正常同步一遍即可得到完整目录

        方法2： 用repo下载

        1）获取指定branch
        否则下载的代码库会很大，所有的android分支可以从这里查看： https://source.android.com/source/build-numbers.html#source-code-tags-and-builds

        //repo init -u https://aosp.tuna.tsinghua.edu.cn/platform/manifest -b android-8.1.0_r2
        repo init -u https://aosp.tuna.tsinghua.edu.cn/platform/manifest -b android-wear-8.0.0_r1

        2）获取最新代码： repo sync -j8 

- 5.编译

        注意： vmware虚拟机的内存至少12G, 否则会出现内存不足的编译错误

        命令：
        source build/envsetup.sh
        lunch aosp_arm64-eng
        make -j16
        
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

# kernel common #

    git clone https://android.googlesource.com/kernel/common
    => git clone https://aosp.tuna.tsinghua.edu.cn/kernel/common