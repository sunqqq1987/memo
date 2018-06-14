# kernel boot #

	参考
	
	https://blog.csdn.net/ongoingcre/article/details/50118809
	https://blog.csdn.net/cagent_z/article/details/61441951

# start_kernel() #

- rest_init()

		start_kernel函数调用 rest_init,于是进入rest_init函数执行：
		kernel_thread(kernel_init,NULL,CLOSE_FS)
		在此处创建一个进程去执行kernel_init，然后在文件系统中寻找并执行init程序，这个就是系统的1号进程。

		接下来执行：
		pid = kernel_thread(kthreadd,NULL,CLONE_FS| CLONE_FILES)
		这个函数是创建一个内核线程去管理系统资源，也是就系统的2号进程.
		
		cpu_startup_entry(CPUHP_ONLINE)执行这个函数后系统启动完毕, 进入cpu_idle_loop()
		(位于linux-3.18.6/kernel/sched/idle.c), 当系统没有进程需要执行时就调度到idle进程, 这个就是0号进程。
		
		1号进程是所有用户态进程的祖先，2号进程是所有内核线程的祖先。