hexdump
http://www.cnblogs.com/lifexy/p/7553550.html  Linux-hexdump命令调试event驱动—详解(13)

使用TSLIB应用程序测试
(TSLIB安装以及使用详解地址: http://www.cnblogs.com/lifexy/p/7628780.html)
TSLIB: 为触摸屏驱动获得的采样提供诸如滤波、去抖、校准等功能，通常作为触摸屏驱动的适配层，为上层的应用提供了一个统一的接口。

linux底层驱动
http://www.cnblogs.com/lifexy/category/1076894.html



波特率与传输速度的关系是：波特率/8=字符数，如115200BPS，即每秒传输115200个字节，115200/8=14400个8位字符，也就是每秒传输14400个字符。


---memory---

Svelte是简化版的Jemalloc,SVELTE用于2GB或更低内存
Svelte禁用了线程缓存,对于需要频繁分配/释放用户空间的多线程应用程序

BoardConfig.mk文件中,
MALLOC_SVELTE := true


从N-OS起，Surfaceflinger应用程序缓冲中的程序在转入后台时仍驻留内存。这增加了系统中的总体ION内存消耗.

ro.config.destory_surface=true

hlos可以用的内存可用从/proc/meminfo中的"system"字样的地址段大小的总和。


-----------
perflock （高通）
1) 提供了JAVA和native的接口给app，用于设置与cpu governor/freq有关的系统参数
2）perflock底层实现是一个mpctl的 client(仅仅xx.so)和mpctl server(perfd), client接收app的请求，然后通过socket的方式发送到server的监听队列中，
server根据请求来写sysfs节点

-----
Valgrind使用说明
https://www.cnblogs.com/wangkangluo1/archive/2011/07/20/2111248.html

---------------------------------

AOSS: Always on subsystem

system power monitor (SPM)

voltage regulator manager (VRM)
core power reduction (CPR)
aggregated resource controller (ARC)
virtual clock domains (VCDs)
power domain controller (PDC)
Trigger command set (TCS)
current resource state(CRS) register
pulse frequency modulation (PFM) and pulse width modulation (PWM)



参考：https://blog.csdn.net/juS3Ve/article/details/80035753

Linux内核为应用程序分配内存的lazy行为

如，在用户空间成功申请100M内存时并没有真的申请成功，只有100M内存中的任意一页被写的时候才真的成功。
用户空间malloc成功申请100M内存时，Linux内核将这100M内存中的每一个4K都以只读的形式映射到一个全部清零的页面（这其实不太符合堆的定义，堆一般是可读可写的），当任意一个4K被写的时候即会发生page fault，Linux内核收到缺页中断后就可以从硬件寄存器中读取到缺页中断的地址和发生原因。之后Linux内核根据缺页中断报告的虚拟地址和原因分析出是用户程序在写malloc的合法区域，此时Linux内核会从内存中新申请一页内存，执行copy on write，把全部清零的页面重新拷贝给新申请的页面，然后把进程的页表项的虚拟地址指向一个新的物理地址。同时，页表中这一页地址的权限也修改为R+W的。注意以页单位发生page fault。



https://www.jianshu.com/p/259a31f628a4 Android Studio+LLDB调试内核Binder


KDUMP
使用内核转储工具kdump把发生Oops时的内存和CPU寄存器的内容dump到一个文件里，之后我们再用gdb来分析问题
但KDUMP一般不用于嵌入式设备上。
参考：https://www.ibm.com/developerworks/cn/linux/l-cn-kdump1/



内核的OOPs信息是有意义的，参考：https://www.cnblogs.com/wwang/archive/2010/11/14/1876735.html


kernel 参数集中在： /proc/sys/kernel

1）nmi_watchdog
NMI watchdog(non maskable interrupt)又称硬件watchdog，用于检测OS是否hang，系统硬件定期产生一个NMI，
而每个NMI调用内核查看其中断数量，如果一段时间(10秒)后其数量没有显著增长，则判定系统已经hung，接下来启用panic机制即重启OS，如果开启了Kdump还会产生crash dump文件

APIC(advanced programmable interrupt controller)：高级可编程中断控制器，默认内置于各个x86CPU中，在SMP中用于CPU间的中断；比较高档的主板配备有IO-APIC，负责收集硬件设备的中断请求并转发给APIC

要使用NMI Watchdog必须先激活APIC，SMP内核默认启动
该参数有2个选项：0不激活；1/2激活，有的硬件支持1有的支持2

2）kptr_restrict
用来限制root和普通用户是否有权限读取 /proc/kallsyms 所显示的内核符号信息
参考： https://blog.csdn.net/gatieme/article/details/78311841

perf

perf工具源码位于linux内核目录的tools下
perf工具的编译需要依赖于内核
perf工具必须使用编译linux内核源码的同一个编译器编译
    
perf在ubuntu可以使用如下命令安装：
sudo apt-get install linux-tools-common

但arm的perf就需要自己动手编译了
参考：
https://blog.csdn.net/chensong_2000/article/details/53436777
https://blog.csdn.net/mtofum/article/details/44108601

https://blog.csdn.net/dreamcoding/article/details/7782415




UART 裸板实现printf函数
https://blog.csdn.net/ForFuture_/article/details/79394046


tee

格式：tee -a file
输出到标准输出的同时，追加到文件file中。如果文件不存在，则创建；如果已经存在，就在末尾追加内容，而不是覆盖。
如：
@echo "+++++build u-boot+++++" | tee  $(OPI_OUTPUT_DIR)/build_uboot.log
@$(PWD)/script/make_uboot.sh 2>&1 | tee -a $(OPI_OUTPUT_DIR)/build_uboot.log


linux增加用户：

1.创建增加用户（名为xxx）所需的文件：
    touch /etc/passwd    //创建用户文件       
    touch /etc/group     //创建用户组文件
    mkdir /home/xxx       //创建用户家目录

2.增加用户：
    adduser  xxx       //增加用户

3.增加用户后，把用户xxx提升为管理员权限：
    vi  /etc/passwd
        原内容：
            xxx:x:1000:1000:Linux User,,,:/home/xxx:/bin/sh
        把用户的uid和gid改为0:
            xxx:x:0:0:Linux User,,,:/home/xxx:/bin/sh

4.增加用户后，还需设置用户的密码：
    passwd  xxx   //执行命令后，输入密码