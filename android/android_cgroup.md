# Android中的cpuctl/cpuset/schedtune的应用 #

	参考
	https://blog.csdn.net/omnispace/article/details/73320945

	Process类: 提供给其他服务接口，用来设置进程优先级、调度策略等
	
	文件： frameworks/base/core/java/android/os/Process.java
	
	1）process类提供的进程优先级 等级：
	
	public static final int THREAD_PRIORITY_DEFAULT = 0;  应用的默认优先级
	
	* ** Keep in sync with utils/threads.h **
	public static final int THREAD_PRIORITY_LOWEST = 19;  线程的最低优先级
	public static final int THREAD_PRIORITY_BACKGROUND = 10;  后台线程的默认优先级
	
	public static final int THREAD_PRIORITY_FOREGROUND = -2;  前台进程的标准优先级
	public static final int THREAD_PRIORITY_DISPLAY = -4;  系统用于显示功能的优先级
	public static final int THREAD_PRIORITY_URGENT_DISPLAY = -8;  系统用于重要显示功能的优先级
	public static final int THREAD_PRIORITY_AUDIO = -16;  音频线程默认优先级
	public static final int THREAD_PRIORITY_URGENT_AUDIO = -19;  重要音频线程默认优先级
	
	2）process类提供的调度策略：
	
	public static final int SCHED_OTHER = 0; 普通进程的默认调度策略，对应CFS调度类（就是CFS的SCHED_NORMAL吗？）
	
	public static final int SCHED_FIFO = 1;  FIFO调度策略，对应RT调度类
	public static final int SCHED_RR = 2;  RR调度策略，对应RT调度类
	
	public static final int SCHED_BATCH = 3;  普通进程的批调度策略，对应CFS调度类
	public static final int SCHED_IDLE = 5;  idle调度策略
	
	注意：SCHED_BATCH是 SCHED_NORMAL普通进程策略的分化版本，适用于非交互型的处理器消耗型进程。
	它采用分时策略，根据动态优先级(可用nice()API设置），分配CPU运算资源。
	
	3）process提供的线程组
	
	 public static final int THREAD_GROUP_DEFAULT = -1;
	 public static final int THREAD_GROUP_BG_NONINTERACTIVE = 0;
	 
	 
	4）Process提供的API
	
	//设置线程的优先级，-20<=priority<=19, 等价于linux的nice值
	public static final native void setThreadPriority(int tid, int priority)
	public static final native int getThreadPriority(int tid)  
	
	//设置线程的调度策略和优先级，policy的取值是SCHED_OTHER等， 注意：priority要在policy所允许的范围内
	因为对于CFS/RT/IDLE等调度器，都有优先级的范围(<0时)
	public static final native void setThreadScheduler(int tid, int policy, int priority)
	public static final native int getThreadScheduler(int tid)
	
	//设置线程的调度组。 Sets the scheduling group for a thread.
	@param group The target group for this thread from THREAD_GROUP_*.
	public static final native void setThreadGroup(int tid, int group)
	
	public static final native void setProcessGroup(int pid, int group)
	        throws IllegalArgumentException, SecurityException;
	
	        
	5) Process的JNI层对应的函数
	文件：android/frameworks/base/core/jni/android_util_Process.cpp
	
	以setThreadPriority为例：
	 {"setThreadPriority",   "(II)V", (void*)android_os_Process_setThreadPriority},
	 
	 android_os_Process_setThreadPriority()
	 -> androidSetThreadPriority()
	    ->set_sched_policy(tid, SP_BACKGROUND) //1 先设置线程的调出策略, 我们重点看这个调出策略的实现
	    ->setpriority(PRIO_PROCESS, tid, pri) //2 再设置线程的优先级
	 
	 
	6) set_sched_policy()函数 根据SchedPolicy类型将tid写入到cpu/schedtune两个子系统的tasks节点中。
	子系统节点和SchedPolicy类型对应如下：
	
	/dev/cpuctl/tasks  SP_FOREGROUND SP_AUDIO_APP SP_AUDIO_SYS
	/dev/cpuctl/bg_non_interactive/tasks  SP_BACKGROUND
	
	/dev/stune/top-app/tasks  SP_TOP_APP
	/dev/stune/foreground/tasks  SP_FOREGROUND SP_AUDIO_APP SP_AUDIO_SYS
	/dev/stune/background/tasks  SP_BACKGROUND
	
	SP_xxx 是 SchedPolicy类型的枚举。
	如果不采用组调度的情况下，SP_BACKGROUND对应SCHED_BACH调度策略，其他对应SCHED_NORMAL；
	但实际情况是都支持组调度，所以android层的SP_XXX策略与内核的cfs调度器的策略间的映射，看上去没有直接关系，更多的是通过
	
	int set_sched_policy(int tid, SchedPolicy policy)  
	{  
	    pthread_once(&the_once, __initialize); //1.1先运行__initialize函数
	    
	#if POLICY_DEBUG   
	   ……  
	#endif   
	   
	    if (__sys_supports_schedgroups) {    //1.2如果支持组调度
	        switch (policy) {
	#ifdef USE_CPUSETS
	        case SP_CACHED:
	            fd = cached_cgroup_fd;
	            break;
	        case SP_ABNOR_BACK:
	            fd = bg_abnormal_cgroup_fd;
	            break;
	#endif
	        default:
	            fd = fg_cgroup_fd;  //1.2.1默认是前台进程组的fd
	            break;
	        }
	
	        if (add_tid_to_cgroup(tid, fd)) {   //1.2.2将当前线程ID写入到fd的文件节点中。比如 /dev/cpuctl/tasks
	            ……  
	        }  
	    } else {    //1.3 如果系统不支持的话，直接通过linux的系统调用来设置线程的调度策略
	        struct sched_param param;
	        param.sched_priority = 0;  
	        sched_setscheduler(tid,
	                           (policy == SP_BACKGROUND) ?  
	                            SCHED_BATCH : SCHED_NORMAL,  
	                           &param);  
	    }  
	}
	
	initialize这个函数很关键，这里的__sys_supports_schedgroups用来检查android系统是否支持组调度。
	
	static void __initialize(void) {
	    char* filename;
	
	//如果android手机上有/dev/cpuctl/tasks文件，则设置__sys_supports_schedgroups为1 （一般都支持）
	    if (!access("/dev/cpuctl/tasks", F_OK)) {
	        __sys_supports_schedgroups = 1;
	
	        filename = "/dev/cpuctl/tasks"; //cat这个文件，可以看到里面都是pid
	        fg_cgroup_fd = open(filename, O_WRONLY | O_CLOEXEC); //获取前台进程组的fd
	
	#ifdef USE_CPUSETS
	        filename = "/dev/cpuctl/bg_cached/tasks";
	        cached_cgroup_fd = open(filename, O_WRONLY | O_CLOEXEC);
	
	        filename = "/dev/cpuctl/bg_abnormal/tasks";
	        bg_abnormal_cgroup_fd = open(filename, O_WRONLY | O_CLOEXEC);
	#endif
	    } else {
	        __sys_supports_schedgroups = 0;
	    }
	...
	}
	
	
	7) 另一种设置线程的调度策略的方式是：set_cpuset_policy(), 它是在使能USE_CPUSETS后才用到.
	set_cpuset_policy()函数会根据SchedPolicy类型将tid写入到cpuset和schedtune子系统的tasks节点中（不会写入到cpuctl子系统）。
	由这个函数可以得出cpuset、schedtune和不同类型SchedPolicy之间的对应关系（需要补充）：
	
	/dev/cpuset/foreground/tasks  SP_FOREGROUND SP_AUDIO_APP SP_AUDIO_SYS
	/dev/cpuset/background/tasks  SP_BACKGROUND
	/dev/cpuset/system-background/tasks  SP_SYSTEM
	/dev/cpuset/top-app/tasks      SP_TOP_APP
	
	/dev/stune/top-app/tasks      SP_TOP_APP
	/dev/stune/foreground/tasks  SP_FOREGROUND SP_AUDIO_APP SP_AUDIO_SYS
	/dev/stune/background/tasks  SP_BACKGROUND
	
	
	
	int set_cpuset_policy(int tid, SchedPolicy policy)
	{
	    // in the absence of cpusets, use the old sched policy
	#ifndef USE_CPUSETS
	    return set_sched_policy(tid, policy);  //1. 没有使能USE_CPUSETS时，调用set_sched_policy()
	
	#else //2 使能CPUSETS后
	   ...
	    return 0;
	#endif
	
	
	8) android中cpuctl/cpuset/schedtune子系统
	参考rootfs中的init.rc
	
	(1) cpuctl
	
	mkdir /dev/cpuctl
	mount cgroup none /dev/cpuctl cpu  //mount cgroup子系统，具体指 /dev/cpuctl 是特殊的文件系统类型？
	
	chmod 0666 /dev/cpuctl/tasks  //默认分组
	chmod 0666 /dev/cpuctl/bg_non_interactive/tasks  //bg_non_interactive分组
	
	
	(2) cpuset
	
	mkdir /dev/cpuset
	mount cpuset none /dev/cpuset   //注意/dev/cpuset不是cgroup...
	
	
	(3) schedtune
	
	# Create energy-aware scheduler tuning nodes
	mkdir /dev/stune
	mount cgroup none /dev/stune schedtune
	
	mkdir /dev/stune/foreground
	
# cgroup #

	1） cgroup 机制
	
	CGroup是control group的简称，它为Linux kernel提供一种任务聚集和划分的机制，可以限制、记录、隔离进程组（process groups）所使用的资源（cpu、memory、I/O等）。
	CGroup也是LXC为实现虚拟化所使用的资源管理手段。
	
	CGroup本身是提供将进程进行分组化管理的功能和接口的基础结构，I/O或内存的分配控制等具体的资源管理功能是通过这个功能来实现的。
	这些具体的资源管理功能称为CGroup子系统。
	
	CGroup子系统包含如下：
	
	blkio
	设置限制每个块设备的输入输出控制。
	
	cpu
	使用调度程序为CGroup任务提供CPU的访问。
	
	cpuacct
	产生CGroup任务的CPU资源报告，CPU Accounting Controller。
	
	cpuset
	如果是多核CPU，这个子系统就会为CGroup任务分配单独的CPU和内存。
	
	devices
	允许或拒绝CGroup任务对设备的访问。
	
	freezer
	暂停或恢复CGroup任务。
	
	hugetlb
	允许限制CGroup 的HubeTLB使用
	
	memory
	设置每个CGroup的内存限制以及产生内存资源报告。
	
	net_cls
	标记每个网络包以供CGroup方便使用。
	
	net_prio
	提供接口以供动态调节程序的网络传输优先级。
	
	perf_event
	增加了对没group的检测跟踪的能力，即可以检测属于某个特定的group的所有线程以及运行在特定CPU上的线程。
	
	
	2）CGROUP参数的意义
	
	(1) cpu.shares： 用来设置cgroup分组任务获得CPU时间的相对值
	举例来说，cgroup A和cgroup B的cpu.share值都是1024，那么cgroup A 与cgroup B中的任务分配到的CPU时间相同
	从下面的cpuctl数据可以看出，默认分组与bg_non_interactive分组cpu.share值相比接近于20:1
	由于Android中只有这两个cgroup，也就是说默认分组中的应用可以利用95%的CPU，而处于bg_non_interactive分组中的应用则只能获得5%的CPU利用率。
	52/(1024+52)=4.8%
	
	(2)cpu.rt_runtime_us： 用来设置cgroup获得CPU资源的周期，单位为微妙。
	
	(3) cpu.rt_period_us： 用来设置cgroup中的任务可以获得的最长CPU资源的时间，单位为微秒。
	设定这个值可以防止某个cgroup独占CPU资源。最长的获取CPU资源时间取决于逻辑CPU的数量。
	比如cpu.rt_runtime_us设置为200000（0.2秒），cpu.rt_period_us设置为1000000（1秒），
	则：在单个CPU上的获得时间为每秒为0.2秒。 2个CPU上获得的时间则是0.4秒。
	
	3) cpuset子系统
	
	cpuset是一个用来分配限制CPU和Memory资源的CGroup子系统。
	cpuset使用sched_setaffinity系统调用来设置tasks的CPU亲和性，使用mbind和set_mempolicy包含Memory策略中的Memory Nodes。
	调度器不会在cpuset之外的CPU上面调度tasks，页分配器也不会在mems_allowed之外的内存中分配。
	
	cpuset提供了一种灵活配置CPU和Memory资源的机制。Linux中已经有配置CPU资源的cpu子系统和Memory资源的memory子系统。
	
	kernel/cpuset.c中定义了子系统cpuset结构体: cpuset_cgrp_subsys
	
	相关节点：
	根目录：/dev/cpuset/
	
	cpu_exclusive cpu资源是否专用？
	cpus  //=> 当前cpuset的CPU列表
	effective_cpus 有效的CPU列表
	effective_mems 有效的memory
	mem_exclusive memory资源是否专用？
	mem_hardwall
	memory_migrate 如果置位，则将页面移到cpusets节点
	memory_pressure 测量当前cpuset的paging压力
	
	memory_spread_page  //if set, spread page cache evenly on allowed nodes
	memory_spread_slab   //if set, spread slab cache evenly on allowed nodes
	
	mems  //=> 当前cpuset的Memory Nodes列表
	sched_load_balance 当前cpuset是否进行负载均衡
	sched_relax_domain_level //the searching range when migrating tasks