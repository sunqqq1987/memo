

# 1) kernel log level #

	文件：kern_level.h
	
	#define KERN_SOH	"\001"		/* ASCII Start Of Header */
	#define KERN_SOH_ASCII	'\001'
	
	#define KERN_EMERG	KERN_SOH "0"	/* system is unusable */
	#define KERN_ALERT	KERN_SOH "1"	/* action must be taken immediately */
	#define KERN_CRIT	KERN_SOH "2"	/* critical conditions */
	#define KERN_ERR	KERN_SOH "3"	/* error conditions */
	#define KERN_WARNING	KERN_SOH "4"	/* warning conditions */
	#define KERN_NOTICE	KERN_SOH "5"	/* normal but significant condition */
	#define KERN_INFO	KERN_SOH "6"	/* informational */
	#define KERN_DEBUG	KERN_SOH "7"	/* debug-level messages */
	
	#define KERN_DEFAULT	KERN_SOH "d"	/* the default kernel loglevel */

# 2) console log level #
	
	文件：printk.h
	
	/* printk's without a loglevel use this.. */
	#define MESSAGE_LOGLEVEL_DEFAULT CONFIG_MESSAGE_LOGLEVEL_DEFAULT
	
	/* We show everything that is MORE important than this.. */
	#define CONSOLE_LOGLEVEL_SILENT  0 /* Mum's the word */
	#define CONSOLE_LOGLEVEL_MIN	 1 /* Minimum loglevel we let people use */
	#define CONSOLE_LOGLEVEL_QUIET	 4 /* Shhh ..., when booted with "quiet" */
	#define CONSOLE_LOGLEVEL_DEFAULT 7 /* anything MORE serious than KERN_DEBUG */
	#define CONSOLE_LOGLEVEL_DEBUG	10 /* issue debug messages */
	#define CONSOLE_LOGLEVEL_MOTORMOUTH 15	/* You can't shut this one up */
	
	extern int console_printk[];
	
	#define console_loglevel (console_printk[0])
	#define default_message_loglevel (console_printk[1])
	#define minimum_console_loglevel (console_printk[2])
	#define default_console_loglevel (console_printk[3])
	
	int console_printk[4] = {
		CONSOLE_LOGLEVEL_DEFAULT,	/* console_loglevel */
		MESSAGE_LOGLEVEL_DEFAULT,	/* default_message_loglevel */
		CONSOLE_LOGLEVEL_MIN,		/* minimum_console_loglevel */
		CONSOLE_LOGLEVEL_DEFAULT,	/* default_console_loglevel */
	};


# 3) /proc/sys/kernel/printk #
	
	log level越小，级别越高，表明问题越严重
	
	只有当printk打印信息时的log level < 当前的console log level的值，这些信息才会被打印到console上。
	
	但所有log都会保留在系统的缓冲区中(ring buffer，可被dmesg读取) 
	参考：https://www.cnblogs.com/aaronLinux/p/6843131.html
	
	cat /proc/sys/kernel/printk
	6 4 1 7
	
	依次分别为：
	6, 当前的控制台日志级别：优先级高于该值（值小于它的）的消息将被打印至控制台
	4, 缺省的消息日志级别：  使用该优先级来打印没有优先级的消息，如：printk(“hell world”); 
		优先级为4,由于满足4<6，故会打印到控制台
	1, 最低的控制台日志级别：控制台日志级别可被设置的最小值（最高优先级）
	7, 缺省的控制台日志级别：控制台日志级别的缺省值，也就是第一项的默认值。
	
	控制台可以是：文本模式终端, 串口, 或者是一台并口打印机
	
	由前面可知：
	第1项是console的当前log level, 默认是console_printk[0] = 7
	第2项是没有指明信息级别时，会采用默认的信息级别， 默认是console_printk[1]=4


# 4) 改写log level #

- 在.rc文件中设置log level

		# Set the console loglevel to KERN_INFO 
		# Set the default message loglevel to KERN_INFO 
		write /proc/sys/kernel/printk "6 6 1 7" 
	
- 设置全部prink输出到console

		echo 15 10 > /proc/sys/kernel/printk
	
- 屏蔽掉所有的内核printk打印到控制台

		echo 1  4  1  7 > /proc/sys/kernel/printk
	
- 其他

		改变console loglevel的方法有如下几种：
		1.启动时Kernel boot option：loglevel=x //loglevel是设置initial console log level
		2.运行时Runtime: dmesg -n level （注意：demsg -n level 改变的是console上的loglevel，dmesg命令仍然会打印出所有级别的系统信息）
		3.运行时Runtime: echo $level > /proc/sys/kernel/printk
		4.运行时Runtime:写程序使用syslog系统调用（可以man syslog）





