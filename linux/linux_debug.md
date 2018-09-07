# Kernel debug #

## 1. 常见方法 ##

- 官方开发阶段用到的工具

		https://www.kernel.org/doc/html/latest/dev-tools/index.html
	
- 时间点

         PM      : suspend entry 2018-08-19 23:47:32.269249326 UTC
         => 这是utc时间，实际的中国时间应该+8
         

- wake_lock

        adb shell
        echo test > /sys/power/wake_lock

        //remove
        echo test > /sys/power/wake_unlock

- 抓开机log

		adb shell cat /proc/last_kmsg >d:/temp/1.txt   //偶尔出现只有xbl log的情况
		adb shell cat /proc/kmsg >d:/temp/1.txt  //只有kernel log, 在O之前是可以不断输出，但到了O之后不可以
		adb shell dmesg >d:/temp/1.txt  //只有kernel log，但只能输出当前的kernel log, 然后退出
		adb shell logcat -b kernel  //可以不断输出kernel log

        android 8.0后：
        adb shell cat /sys/fs/pstore/console-ramoops > last_kmsg.txt

        adb root
        adb shell dmesg > kmsg.txt

        清空dmesg:
        adb shell dmesg -c


        其他：
        dump_last_kmsg()
        #define LAST_KMSG_PATH          "/proc/last_kmsg"
        #define LAST_KMSG_PSTORE_PATH   "/sys/fs/pstore/console-ramoops"
        
- 检查last kmsg是否有特定信息

        Fs_mgr_verity.cpp (system\core\fs_mgr)：
        was_verity_restart()

       更多参考：https://blog.csdn.net/skykingf/article/details/50600439
        
- 开机后台抓取kernel log

        https://blog.csdn.net/kris_fei/article/details/77186635?locationNum=3&fps=1

- bugreport/dumpstate的实现

        https://blog.csdn.net/u010164190/article/details/72875984
        
- 用printk 输出log

    - 打印指针

        打印裸指针(raw pointer)用 %p
        %pF可打印函数指针的函数名和偏移地址
        %pf只打印函数指针的函数名，不打印偏移地址

    - 打印boot时间
    
        ktime_t　wakeup_ktime = ktime_get_boottime();

    - 打印 文件名 函数名 行号

        printk("%s %s %d \n",__FILE__,__FUNCTION__,__LINE__); 

	- 只有提供一个结尾的新行给printk，才会刷行
	
	- 打印设备号
	
			int print_dev_t(char *buffer, dev_t dev)
			char *format_dev_t(char *buffer, dev_t dev)
			两个宏定义都将设备号编码进给定的缓冲区; 唯一的区别是 print_dev_t 返回打印的字符数, 而 format_dev_t 返回缓存区;
			因此, 它可以直接用作 printk 调用的参数, 但是必须记住 printk 只有提供一个结尾的新行才会刷行.
			缓冲区应当足够大以存放一个设备号; 如果 64 位编号在以后的内核发行中明显可能, 这个缓冲区应当可能至少是 20 字节长.
	
	- dynamic_debug: 只针对文件开启
	
			adb root
			adb shell mount -t debugfs none /sys/kernel/debug
			adb shell "echo 'file phy-msm-usb.c +p' > /sys/kernel/debug/dynamic_debug/control"
			adb shell
			cat /proc/kmsg > /data/kmesg.txt &

	- __ratelimit: 限制printk打印log的频率
			
			printk_ratelimit()和printk_ratelimited(), 都封装了__ratelimit().

			int printk_ratelimit(void)：
			通过跟踪多少消息发向控制台而工作. 当输出级别超过一个限度, printk_ratelimit 开始返回 0 并扔掉消息.
			
			定义如下：
			/*																									  
			 * printk rate limiting, lifted from the networking subsystem.										  
			 *																									  
			 * This enforces a rate limit: not more than 10 kernel messages										
			 * every 5s to make a denial-of-service attack impossible.											  
			 */																									  
			DEFINE_RATELIMIT_STATE(printk_ratelimit_state, 5 * HZ, 10); //允许在5s内最多打印10条消息出来									  
																													
			int printk_ratelimit(void)																			   
			{																										
				return __ratelimit(&printk_ratelimit_state);														
			}																										
			EXPORT_SYMBOL(printk_ratelimit);  
			
			它的行为可以通过修改 /proc/sys/kernel/printk_ratelimit (多长时间) ，
			以及 /proc/sys/kernel/printk_ratelimit_burst（在printk_ratelimit时间段内最多允许的消息数量）来定制。

			如果内核代码里没有调用printk_ratelimit就不受这两个值的限制。

			典型的使用方法：
			(1) 在打印一个可能会常常重复的消息之前调用. 如果这个函数返回非零值, 继续打印你的消息, 否则跳过它.
				if (printk_ratelimit())
					printk(KERN_NOTICE "The printer is still on fire\n");

			(2) printk_ratelimited(KERN_ERR "end_request: %s error, dev %s, "  
			   "sector %llu\n", error_type, req->rq_disk ?  
			   req->rq_disk->disk_name : "?",  
			   (unsigned long long)blk_rq_pos(req));

	
	- 自定义开启和关闭debug信息
	
			参考：https://blog.csdn.net/geng823/article/details/37656149

			Makefile：
			# Comment/uncomment the following line to disable/enable debugging   
			DEBUG = y   
			   
			# Add your debugging flag (or not) to CFLAGS   
			ifeq ($(DEBUG),y)   
			 DEBFLAGS = -O -g -DSCULL_DEBUG  # "-O" is needed to expand inlines   
			else   
			 DEBFLAGS = -O2   
			endif   
			   
			CFLAGS += $(DEBFLAGS)
						
- dmesg

		dmesg命令可用来查看__LOG_BUF_LEN 字节长的环形缓存的内容, 不会冲掉它;
		实际上, 这个命令将缓存区的整个内容返回给 stdout, 不管它是否已经被读过.

		但有不足之处： 读取完当前的缓冲区log后，就退出，不能一直输出kernel log.

- 用warn_on() 打印log和 callstack

- 调用bug_on()：在特殊点让系统panic

- earlycon

		如果遇到不能boot, 且不能进入upload的情况下，可以在kernel cmdline中加入'earlycon=XXX'参数指明在串口输出log.

		参考：
		https://blog.csdn.net/juS3Ve/article/details/79465972 earlycon实现

- ftrace: 跟踪内核进程切换，中断的开与关，以及性能问题

		可以自己添加trace_printk()

- sysrq: 打印系统进程的信息，甚至可以trigger panic

        参考： https://blog.csdn.net/skdkjzz/article/details/50426397

        //开启SysRq功能
        echo 1>/proc/sys/kernel/sysrq 

        //手动触发crash
        echo c>/proc/sysrq-trigger 

        //显示disk sleep的进程
        echo d>/proc/sysrq-trigger

         //显示线程信息
        echo t>/proc/sysrq-trigger

        //显示linux memory状态
        echo m>/proc/sysrq-trigger



        static struct sysrq_key_op *sysrq_key_table[36] = {
        &sysrq_loglevel_op,		/* 0 */
        &sysrq_loglevel_op,		/* 1 */
        &sysrq_loglevel_op,		/* 2 */
        &sysrq_loglevel_op,		/* 3 */
        &sysrq_loglevel_op,		/* 4 */
        &sysrq_loglevel_op,		/* 5 */
        &sysrq_loglevel_op,		/* 6 */
        &sysrq_loglevel_op,		/* 7 */
        &sysrq_loglevel_op,		/* 8 */
        &sysrq_loglevel_op,		/* 9 */

        /*
        * a: Don't use for system provided sysrqs, it is handled specially on
        * sparc and will never arrive.
        */
        NULL,				/* a */
        &sysrq_reboot_op,		/* b */
        &sysrq_crash_op,		/* c & ibm_emac driver debug */
        &sysrq_showlocks_op,		/* d */
        &sysrq_term_op,			/* e */
        &sysrq_moom_op,			/* f */
        /* g: May be registered for the kernel debugger */
        NULL,				/* g */
        NULL,				/* h - reserved for help */
        &sysrq_kill_op,			/* i */
        #ifdef CONFIG_BLOCK
        &sysrq_thaw_op,			/* j */
        #else
        NULL,				/* j */
        #endif
        &sysrq_SAK_op,			/* k */
        #ifdef CONFIG_SMP
        &sysrq_showallcpus_op,		/* l */
        #else
        NULL,				/* l */
        #endif
        &sysrq_showmem_op,		/* m */
        &sysrq_unrt_op,			/* n */
        /* o: This will often be registered as 'Off' at init time */
        NULL,				/* o */
        &sysrq_showregs_op,		/* p */
        &sysrq_show_timers_op,		/* q */
        &sysrq_unraw_op,		/* r */
        &sysrq_sync_op,			/* s */
        &sysrq_showstate_op,		/* t */
        &sysrq_mountro_op,		/* u */
        /* v: May be registered for frame buffer console restore */
        NULL,				/* v */
        &sysrq_showstate_blocked_op,	/* w */
        /* x: May be registered on ppc/powerpc for xmon */
        /* x: May be registered on sparc64 for global PMU dump */
        NULL,				/* x */
        /* y: May be registered on sparc64 for global register dump */
        NULL,				/* y */
        &sysrq_ftrace_dump_op,		/* z */
        };

- trace32在线调试

- trace simulator分析ramdump

		cpu context, 各进程的callstack,
		memory使用情况（system memory map, buddy, slub, ion, vmalloc分配情况，page info, low memory情况)，
		遍历页表，进程的list，进程占用的锁(mutex,spin lock, rwsem)，中断情况(miss irq)，workqueue里work,
		device list信息，clock信息, timer list信息， CPU/RPM/DDR频率
	
- gdb调试内核 ？

		对于一个运行的内核, 核心文件是内核核心映象, /proc/kcore.
		一个典型的 gdb 调用看来如下:  
		gdb /usr/src/linux/vmlinux /proc/kcore
		第一个参数是非压缩的 ELF 内核可执行文件的名子, 不是 zImage 或者 bzImage 或者给启动环境特别编译的任何东东.
		第二个参数是核心文件的名子.

- kdb/kgdb 内核调试器

		kdb 内嵌式内核调试器, 作为来自 oss.sgi.com 的一个非官方补丁.
		要使用 kdb, 你必须获得这个补丁(确认获得一个匹配你的内核版本的版本), 应用它, 重建并重安装内核.
		
		参考: https://www.kernel.org/doc/html/latest/dev-tools/kgdb.html

- ETB trace

- sysctl命令

		在内核开发调试中，有时想动态修改内核参数，可以使用sysctl命令。
		这个选项可以用来设置vm，调度器，net等配置，设置的参数信息在/proc/sys目录下。
		
		读一个指定变量：
		root:sysctl kernel.dmesg_restrict
		kernel.dmesg_restrict = 0
	
		设置一个变量：
		root#： sysctl kernel.dmesg_restrict=1
		kernel.dmesg_restrict = 1

- others

		1) cat /sys/kernel/debug/wakeup_sources  //wakeup sources
		2) ls /sys/kernel/debug/clk   //clock
		3) ls /sys/class/regulator  //regulator

	
## 2. 问题分类 ##

- non-secure watchdog

		1) 中断风暴
		2) 关中断后，memory发生异常。如spinlock_irq_save()后发生memory corruption/bitflip
		3) CPU 0 ping不通其他CPU, 而其他cpu被卡住，如stuck at TZ side
		4）系统过于繁忙，导致watchdog进场无法被调度.(比如打印过多的crash信息)

- lock-up
		
		1）mutex使用不当，导致deadlock. 需要打开mutex debug等开关辅助调试
		2）在中断上下文中调用导致睡眠的函数
		3）中断hanlder里有的特殊情况没有返回HANDLED

- 内存泄漏

		1) 多个进程运行同一段代码去分配内存（调用kmalloc），其中一个进程上分配的内存将会被丢失，从而发生泄漏。
		 如这样的代码： dptr->data[s_pos] = kmalloc(quantum, GFP_KERNEL)
		解决方法： 在这段代码加mutex类的锁，并且if (!dptr->data[s_pos]) 才调用kmalloc

		2） 使能 KMEMLEAK
		
		3）使能SLUB DEBUG后，解析ramdump 中SLUB的分配情况。
		如果发现某个size的slub object占用很大的内存，那么这个slub object的分配过程是个泄漏的怀疑对象。
			
		
- 内存破坏

		在ENG版本上：
	
		1）使能 SLUB/PAGE 的debug feature

		CONFIG_DEBUG_VM=y
		CONFIG_DEBUG_HIGHMEM=y
		CONFIG_SLUB_DEBUG=y
		CONFIG_SLUB_DEBUG_ON=y
		CONFIG_PAGE_POISONING=y
		
		但是SLUB DEBUG仅仅针对从slub分配器分配的内存，如果你需要检测从栈中或者数据区分配内存的问题，就不行了。
		这时可以选择KASAN
	
		2）使能 KASAN

		可用于debug： use-after-free, double free, overflow write
		
		KernelAddressSANitizer (KASAN) is a dynamic memory error detector.
		It provides a fast and comprehensive solution for finding use-after-free and out-of-bounds bugs.

		KASAN uses compile-time instrumentation for checking every memory access, therefore you will need a GCC version 4.9.2 or later.
		GCC 5.0 or later is required for detection of out-of-bounds accesses to stack or global variables.
		
		使用guide: https://www.kernel.org/doc/html/latest/dev-tools/kasan.html
		
	
# App debug #

- 内存泄漏

	- vagrind
	
	- 通过smem查看USS
	
			VSS- Virtual Set Size 虚拟耗用内存
			RSS- Resident Set Size 实际使用物理内存（包含共享库占用的内存）
			PSS- Proportional Set Size 实际使用的物理内存（比例分配共享库占用的内存）
			USS- Unique Set Size 进程独自占用的物理内存（堆内存，独占）
			VSS >= RSS >= PSS >= USS
		
			可以使用smem工具查看进程的VSS,RSS.PSS,USS值，USS值就是堆内存占用，内存泄漏一般只看这个。
			安装：$ sudo apt-get install smem
			内存泄漏的判定，查看USS，多时间点采样，震荡发散的内存消耗就是存在泄漏.

- 在 strace 下运行程序

		strace 命令是一个有力工具, 显示所有的用户空间程序发出的系统调用. 它不仅显示调用, 还以符号形式显示调用的参数和返回值.
		当一个系统调用失败, 错误的符号值(例如, ENOMEM)和对应的字串(Out of memory) 都显示.
		strace 有很多命令行选项; 其中最有用的是 -t 来显示每个调用执行的时间, -T 来显示调用中花费的时间, -e 来限制被跟踪调用的类型,
		以及-o 来重定向输出到一个文件. 缺省地, strace 打印调用信息到 stderr.

- 给SIGSEGV注册信号处理函数

		当段错误发生时，操作系统会发送一个SIGSEGV信号给进程，导致进程产生核心转储文件并且退出。
		如何才能让进程先捕捉SIGSEGV信号，打印出有用的方便定位问题的信息，然后再优雅地退出呢？可以通过给SIGSEGV注册信号处理函数来实现
		参考《linux环境编程——从应用到内核》

- 强制进程产生coredump，检测死锁以及进程快照

		http://blog.chinaunix.net/uid-23629988-id-175809.html
		
		有些些bug是不会导致进程crash的，比如死锁——这时，程序已经不正常了，可是却没有coredump产生。
		如果环境又不允许gdb调试，难道我们就束手无策了吗？针对这种情况，一般情况下，对于这样的进程，
		可以利用watchdog监控它们，当发现这些进程很长时间没有更新其heartbeat时，可以给这些进程发送SIGSEGV等致命信号导致其产生coredump。

- GDB 中 checkpoint 功能保存出问题时现场的快照

		参考： http://blog.chinaunix.net/uid-23629988-id-2943273.html

		(gdb) checkpoint

- 获取目标平台的GDB debugger
	
	- 编译源码方式安装
	
			1）下载GDB源码： http://ftp.gnu.org/gnu/gdb/gdb-8.0.tar.gz
				GDB官网：http://www.gnu.org/software/gdb/
				ArchLinux: https://www.archlinux.org/packages/community/x86_64/aarch64-linux-gnu-gdb/

			2）linux环境下解压并编译安装(注意，window下也有arm的交叉编译工具）
			32位arm版：
				./configure --target=arm-linux --program-prefix=arm-linux- --prefix=/opt/arm-linux-gdb/
			64位arm版：
				./configure –target=aarch64-linux-gnu
			make  //如果提示makeinfo等错误，先apt-get install textinfo
			make install
			之后whereis aarch64-linux-gnu-gdb 可以看到安装到了usr/local下

	- **直接使用NDK中的gdb，gdbserver**
	
			gdbserver: push到手机中使用
				\Sdk\ndk-bundle\prebuilt\android-arm64\gdbserver\gdbserver
				注意：ndk中没有arm版的gdb

			gdb: windows PC端使用
				android-ndk-r9\toolchains\arm-linux-androideabi-4.8\prebuilt\windows-x86_64\bin\arm-linux-androideabi-gdb.exe ？

	- **使用android源码中编译好的gdb, gdbserver（都是ARM版）**
	
			一般android源码中已有编译好的gdbserver和gdb程序
			如在高通M OS(64位)平台上:
			
			gdbserver位于：prebuilts/misc/android-arm64/gdbserver64，若目标手机是userdebug或eng版本，gdbserver已经安装在system/bin/下
			
			gdb位于：prebuilts/gcc/linux-x86/aarch64/aarch64-linux-android-4.9/bin/aarch64-linux-android-gdb
		
- coredump的原理
	
		当native程序发生异常时，在kernel的异常处理函数中被捕获到。
		因此kernel会调用do_coredump()来执行用户态的coredump存储程序，以保存coredump文件。
		
		1）负责存储coredump的程序（或者说脚本）路径:
		被保存在节点/proc/sys/kernel/core_pattern中，如：
			cat  /proc/sys/kernel/core_pattern
			=> /system/bin/crash_reporter --user=%P:%s:%u:%g:%e
		
		而crash_reporter程序对应的代码是.c/c++

		2）指定coredump存储程序的路径
		默认对应可执行程序是core，但它一般是不存在的。
		所以通常在相应的.rc文件中设定cordump存储程序，以便开机的时候设定它。
		如 /system/core/crash_reporter/crash_reporter.rc 中：
		
			on property:crash_reporter.coredump.enabled=1 //当enable coredump时
			write /proc/sys/kernel/core_pattern \
					"|/system/bin/crash_reporter --user=%P:%s:%u:%g:%e"
			
			on property:crash_reporter.coredump.enabled=0 //没有enable coredump时
				write /proc/sys/kernel/core_pattern "core"
		
		3)ulimit -c 限制coredump的大小
			ulimit -c unlimited 或 0
			=> 把core文件的大小设置为无限大,同时也可以使用数字来替代unlimited,对core文件的上限制做更精确的设定

- GDB调试native的coredump
	
	- 参考

			https://blog.csdn.net/sunxiaopengsun/article/details/72974548
			http://linuxtools-rst.readthedocs.io/zh_CN/latest/tool/gdb.html  #gdb 调试利器
			http://blog.jobbole.com/107759/	 #gdb 调试入门，大牛写的高质量指南
			http://blog.csdn.net/yangzhongxuan/article/details/6911689   #gdb调试（四）函数调用栈之Backtraces
			https://blog.csdn.net/forever_2015/article/details/50286421  #gdb+gdbserver 调试NE-coredump
		
	- 注意
			1）编译时请禁止编译优化选项，即添加-O0编译选项，否则会导致代码在调试时出现跳来跳去的可能
			2）首先要保证程序编译时加了-g选项，否则不能用GDB单步调试，只能用l显示代码行。
			3）要用指定架构的gdb版本（不是gdbserver)才能调试，否则会出现“no core file handler recognizes format”错误

			4) 用Android studio编译的程序，不能直接用android源码中的gdb调试，是交叉编译器不一样导致的？

	- 步骤
	
			1）执行 gdb <program> <coredump>
				如：gdb ./xxl_hello coredump_xxl_hello
				注意，上面的gdb是对应架构下的gdb,如果是ARM架构编译hello, 那就是arm版的gdb
			
			2）l  //显示程序行
	
			3) b 10 //在程序的第10行设置断点
	
			4) bt full //显示调用栈中（所有的帧frame: 函数，相应的局部变量，文件行号）
			   bt  //backtrace的意思
			
			5) frame i //显示backtrace中指定的帧
				简写f i
			
			6）up / down 显示上一帧和下一帧
			
			7）打印局部变量
			   p  var
			
			8）info locals //显示当前的局部变量
				info r //显示寄存器
				info proc m （info proc mappings 的简写）//查看进程的memory map
				info b （info breakpoints）//显示当前程序的断点设置情况
			   

			9）disas [func] //显示函数或当期位置的汇编
				disas/s  //同时显示源码和汇编
		
			10）q //退出gdb调试
			
			其他：
			next（简写 n）//单步跟踪程序，当遇到函数调用时，也不进入此函数体
			step（简写s）//单步调试如果有函数调用，则进入函数；与命令n不同，n是不进入调用的函数的

	- issue
	
			1) GDB调试加载执行程序后，提示 “not in executable format”
			=> 查看Makefile文件，CFLAGS选项是否加-g:
			   CFLAGS= -g -O2


- 高通平台Android GDB调试 natvie 程序

		https://blog.csdn.net/l460133921/article/details/52931328  
		=> 有gdb命令说明
	
- **老版本，使用windows的GDB远程调试设备里的android native程序**

		参考：
		http://blog.163.com/tod_zhang/blog/static/102552214201392824228231
		https://www.cnblogs.com/liangwode/p/6242577.html
		https://blog.csdn.net/earbao/article/details/53021957
	
		1) 获取gdb和gdbserver
		注意：这两个需要配套，建议使用同一个ndk下面的gdb和gdbserver（gdbserver是arm版的）

		2) 然后把gdbserver安装到设备的 /system/bin下
		adb push gdbserver /system/bin/
		adb shell chmod u+x /system/bin/gdbserver
		
		3) 以DEBUG方式编译目标程序hello
		具体来说，就是 ndk-build NDK_DEBUG=1
		可以调试的程序在 ..\obj\local\armeabi目录下，相对于jni目录
		
		4）adb设置端口转发
		adb forward tcp:20000 tcp:20001

		5) 运行gdbserver来启动目标程序hello，等待gdb客户端的连接
		
		adb push hello /data/local/tmp/
		adb shell chmod u+x /data/local/tmp/hello
		
		gdbserver有2种方式调试程序(打开指定的端口)：
			(1) 启动方式： gdbserver IP:PORT  <bin程序路径>
				如：gdbserver:20001 /data/local/tmp/hello
	
				适用于重新启动进程的情况
				
			(2) 附加方式： gdbserver IP:PORT --attach <pid>
	
				适用于进程已经处于运行状态的情况

			注意：当在本机调试设备（手机）时，IP可以省略

		6) 启动GDB客户端，开始调试目标程序

		windows PC端， 运行 arm-linux-androideabi-gdb.exe 后（从哪里获得？）
		(gdb) file ../obj/local/armeabi/sum #加载带调试信息的目标程序hello

		(gdb) target remote :20000 #连上gdb server
		
		(gdb) list #显示代码
		(gdb) break main #设置断点
		(gdb) continue #继续运行
	
	- **调试共享库**
	
			参考：https://blog.csdn.net/hansel/article/details/1830543

- **用NDK-gdb调试native程序**
		
		参考：https://developer.android.com/ndk/guides/ndk-gdb.html
		
			https://blog.csdn.net/you_lan_hai/article/details/50993437
			https://www.cnblogs.com/bingghost/p/5731020.html

		通过andorid studio下载NDK后会附带ndk-gdb脚本，它是常用GDB调试的封装。
		路径：\Sdk\ndk-bundle\ndk-gdb.cmd

# 其他 #

- 判断程序是否是debug版本

		readelf -S file: 看是否有"debug"字样的section

- 判断程序是否包含调试信息

		file <program>
		=> (uses shared libs), for GNU/Linux 2.6.9, not stripped   #保证是可执行文件

- 判断程序是否可以执行

		type <program>
		如：type ./const
		=> ./const is ./const	  #保证执行文件路径正常

- 获取库的编译信息

		objdump -s b.a
		=>Contents of section .comment 段里有GCC的交叉编译信息

# QEMU #

- **用QEMU模拟器调试ARM64内核**

		参考
		http://blog.chinaunix.net/xmlrpc.php?r=blog/article&uid=20718037&id=5748871
		http://www.infocool.net/kb/Linux/201702/297866.html
		
		1) 编译ARM Qemu模拟器

		先到Qemu官网下载最新的模拟器
			1 tar -xfqemu-2.9.0.tar.xz
			2 cd qemu-2.9.0/
			3 mkdir build
			4 cd build/
			5 # 需要安装这个软件包，因为我们使能了--enable-virtfs，否则configure的时候会失败
			6 sudo apt-get install libcap-dev  
			7 ../configure --target-list=arm-softmmu,i386-softmmu,x86_64-softmmu,aarch64-linux-user,arm-linux-user,i386-linux-user,x86_64-linux-user,aarch64-softmmu --enable-virtfs
			8 make –j4 //期间会提示缺少库，要相应安装
			9 sudo make install
		结果是qemu-system-aarch64安装在/usr/local/bin/
		
		2) 安装ARM GCC cross-compile工具链

		sudo apt install gcc-aarch64-linux-gnu
		
		3) ARM GCC corss compile kenrel 4.4

		make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- O=./out_aarch64  defconfig
		make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- O=./out_aarch64  menuconfig

		由于下面要用到ramdisk的启动方式，需要在kernel配置中支持：
		General setup  --->
		   ----> [*] Initial RAM filesystem and RAM disk (initramfs/initrd) support
		Device Drivers  --->
			[*] Block devices  --->
		<*>   RAM block device support
					 (65536) Default RAM disk size (kbytes)

		make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- O=./out_aarch64 -j4
		====>/out_aarch64/arch/arm64/boot/Image
		
		4) ARM cross compile busybox

		make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- menuconfig
		make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu-
		make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- install
		
		5) make rootfs

		vi  mk_rootfs/mk_ramdisk.sh

			#! /bin/sh
			BUSYBOX_PATH=$HOME/bakxxl/busybox-1.26.2
			ROOTFS_IMG=$HOME/bakxxl/flashxxl
			ROOTFS_PATH=$HOME/bakxxl/rootfs

			rm -rf $ROOTFS_IMG
			dd if=/dev/zero of=$ROOTFS_IMG bs=1M count=8
			mkfs.ext2 -m0 $ROOTFS_IMG
			mount -o loop $ROOTFS_IMG $BUSYBOX_PATH/mnt
			cp -R $ROOTFS_PATH/* $BUSYBOX_PATH/mnt
			umount $BUSYBOX_PATH/mnt

		cp -r mk_rootfs/etc  busybox-1.26.2/
		cp mk_rootfs/mk_ramdisk.sh busybox-1.26.2/
		cd busybox-1.26.2/
		./ mk_ramdisk.sh
		
		6) 使用qemu直接启动内核

		cd linux-4.4.54/out_aarch64/
		qemu-system-aarch64 -machine virt -cpu cortex-a53 -machine type=virt -nographic -smp 2 -m 2048
			-kernel ./arch/arm64/boot/Image
			--append "root=/dev/ram0 rwrootfstype=ext4 console=ttyAMA0 init=/linuxrcignore_loglevel"  
			-initrd /home/samlin930/tool/busybox-1.26.2/ramdisk.img
		
		qemu退出方法: ctrl + A + 按 X
		
		7) 使用qemu和gdb来调试内核

		当启动vmlinux出问题时，可以用以下方式来调试内核：

		(1) qemu-system-aarch64 -s -S-machine virt -cpu cortex-a53 -machine type=virt -nographic -smp 2 -m 2048 
			-kernel ./arch/arm64/boot/Image 
			--append "root=/dev/ram0 rwrootfstype=ext4 console=ttyAMA0 init=/linuxrcignore_loglevel"  
			-initrd /home/samlin930/tool/busybox-1.26.2/ramdisk.img
		
		此时内核启动，并使用gdbserver打开了1234端口供gdb客户端连接. 其中：
			-s表示运行虚拟机时将1234端口开启成调试端口；
			-S表示“冷冻”虚拟机，等待调试器发出继续运行命令；
			-append root=…. 表示传递给内核的参数。
		
		(2)本地打开另一个terminal，输入以下命令：
			$aarch64-linux-gnu-gdb
			$file vmlinux
			$target remote localost:1234
			$b start_kernel   #设置断点
			$c	#continue,让程序继续执行，之后会停在上个断点上
			$n	#单步执行

# objdump #

	windows_x86版的objdump:
		\ndk-bundle\toolchains\aarch64-linux-android-4.9\prebuilt\windows-x86_64\bin\aarch64-linux-android-objdump.exe
		\ndk-bundle\toolchains\arm-linux-androideabi-4.9\prebuilt\windows-x86_64\bin\arm-linux-androideabi-objdump.exe
	
	objdump命令是Linux下的反汇编目标文件或者可执行文件的命令.
	编译成目标文件（要加-g选项）, 如：gcc -g -o test.c
	
	1) objdump用-D选项，将所有section都反汇编出来
	如：objdump -D <obj>
	
	2) 输出C源代码和反汇编出来的指令对照的格式
	objdump -S test.o
	
	3）objdump -s test
	除了显示test的全部Header信息，还显示他们对应的十六进制文件代码
	
	4)  objdump -x test
	显示test的全部Header信息

	5) objdump -h test
	显示test的Section Header信息

	6) objdump -d test
	反汇编test中的需要执行指令的那些section

	7) objdump -f test
	显示test的文件头信息


# Crash-utility #

	参考
	https://people.redhat.com/anderson/
	https://blog.csdn.net/juS3Ve/article/details/79428049  crash tool 使用实例
	
	Use Crash-utility to Extract Core Dump From Memory Dump 