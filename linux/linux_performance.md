# 参考 #

	https://blog.csdn.net/hn2002/article/details/7426907

	https://blog.csdn.net/chinalinuxzend/article/details/1759236

	https://blog.csdn.net/TianTangYouZui/article/details/72231590

	https://blog.csdn.net/shanzhizi/article/details/24816677 Linux常用性能调优工具索引

	https://blog.csdn.net/zhangskd/article/details/37902159/ 系统级性能分析工具 — Perf

# Perf #

	Perf是一个包含22种子工具的工具集，以下是最常用的5种：
	http://www.brendangregg.com/perf.html

	perf-list Perf-list用来查看perf所支持的性能事件，有软件的也有硬件的。
	perf-stat  用于分析指定程序的性能概况。
	cache 优化实例: https://blog.csdn.net/trochiluses/article/details/17346803
	使用perf 来检测程序执行期间由此造成的cache miss的命令：
	perf stat -e cache-misses ./exefilename
	查看触发cach-miss的函数最多的函数
	perf record -e cache-misses ./exefilename  
	

	perf-top 对于一个指定的性能事件(默认是CPU周期)，显示消耗最多的函数或指令。
	perf-record
	perf-report
	perf-lock
	perf-kmem
	probe-sched
	perf-probe


# 1. CPU性能瓶颈 #

	1）通过调整进程优先级调整： nice 命令来调整进程优先级别；可调范围（-20到 19）
	
	如： renice 5 pid
	
	2）通过调整cpu的亲和度来集中处理某一个中断类型: 将系统发出的中断都绑定在一个cpu上，
	这样其他cpu继续执行自己正在执行的线程，不被中断打扰，从而较少了线程上下文切换时间，增强性能；
	
	echo 03 > /proc/irq/19/smp-affinity (将中断类型为19的中断绑定到第三个cpu上处理）

	CPU性能分析工具：
	vmstat
	ps
	sar
	time
	strace
	pstree
	top

# 2. 内存性能瓶颈 #

	高性能的办法就是减少写到磁盘的次数，提高每次写磁盘时的效率质量
	
	1）通过调节page cache的脏数据同步到硬盘的策略
	
	（脏数据表示在page cache中已经修改、但还没有更新到内存或backed-file的数据）
	例如：
	echo 10 > /proc/sys/vm/dirty_background_rato (当脏数据占据物理内存10%时，触发pdflush同步到硬盘）：小心调节，会大幅度的影响性能；
	echo 2000 > /proc/sys/vm/dirty_expire_centisecs (当脏数据在物理内存的逗留时间超过2000ms时被同步到硬盘）；

	2）通过调节swappiness参数，来优化linux虚拟内存管理
	
	基于程序的局部性原理，linux通过虚拟内存机制来实现并发运行进程，linux发现物理内存不够用时，会根据LRU算法将一部分内存swap out到硬盘；
	当运行被换出的那个线程时，在swap in 到内存里；
	例如： echo 10 > /proc/sys/vm/swappiness
	值为0表示尽量都用物理内存(只有当内存不足时才使用swap空间）
	值为100表示积极的使用swap分区，这个参数很重要；小心调节，一般为60

	3） vmstat

	https://blog.csdn.net/lishenglong666/article/details/47747517

	vmstat是一个很全面的性能分析工具，可以观察到系统的进程状态、内存使用、虚拟内存使用、磁盘的IO、中断、上下文切换、CPU使用等。
	vmstat 1 5
	procs		 —————memory—————	  ——swap—— ——io——  ——system——   ——cpu——
	r   b	swpd	 free	   buff	  cache   si	so	bi	 bo	  in	cs	us sy  id wa st
	1   0	84780	909744   267428	1912076   0	 0	 20	 94	   0	 0	 2  1  95  1  0
	1   2	84780	894968   267428	1912216   0	 0	  0   1396	2301 11337	 8  3  89  0  0
	1   0	84780	900680   267428	1912340   0	 0	 76   1428	1854  8082	 7  2  90  0  0
	1   0	84780	902544   267432	1912548   0	 0	116	928	1655  7502	 7  2  92  0  0
	2   0	84780	900076   267432	1912948   0	 0	180	904	1963  8703	10  3  87  0  0
	对输出解释如下：
	1）procs
	a.r列表示运行和等待CPU时间片的进程数，这个值如果长期大于系统CPU个数，就说明CPU资源不足，可以考虑增加CPU；
	b.b列表示在等待资源的进程数，比如正在等待I/O或者内存交换等。
	2）memory
	a.swpd列表示切换到内存交换区的内存数量（以KB为单位）。如果swpd的值不为0或者比较大，而且si、so的值长期为0，那么这种情况一般不用担心，不会影响系统性能；
	b.free列表示当前空闲的物理内存数量（以KB为单位）；
	c.buff列表示buffers cache的内存数量，一般对块设备的读写才需要缓冲；
	d.cache列表示page cached的内存数量，一般作文件系统的cached，频繁访问的文件都会被cached。如果cached值较大，就说明cached文件数较多。
	如果此时IO中的bi比较小，就说明文件系统效率比较好。
	3）swap
	a.si列表示由磁盘调入内存，也就是内存进入内存交换区的数量；
	b.so列表示由内存调入磁盘，也就是内存交换区进入内存的数量
	c.一般情况下，si、so的值都为0，如果si、so的值长期不为0，则表示系统内存不足，需要考虑是否增加系统内存。
	4）IO
	a.bi列表示从块设备读入的数据总量（即读磁盘，单位KB/秒）
	b.bo列表示写入到块设备的数据总量（即写磁盘，单位KB/秒）
	这里设置的bi+bo参考值为1000，如果超过1000，而且wa值比较大，则表示系统磁盘IO性能瓶颈。
	5）system
	a.in列表示在某一时间间隔中观察到的每秒设备中断数；
	b.cs列表示每秒产生的上下文切换次数。
	上面这两个值越大，会看到内核消耗的CPU时间就越多。
	6）CPU
	a.us列显示了用户进程消耗CPU的时间百分比。us的值比较高时，说明用户进程消耗的CPU时间多，如果长期大于50%，需要考虑优化程序啥的。
	b.sy列显示了内核进程消耗CPU的时间百分比。sy的值比较高时，就说明内核消耗的CPU时间多；如果us+sy超过80%，就说明CPU的资源存在不足。
	c.id列显示了CPU处在空闲状态的时间百分比；
	d.wa列表示IO等待所占的CPU时间百分比。wa值越高，说明IO等待越严重。如果wa值超过20%，说明IO等待严重。
	e.st列一般不关注，虚拟机占用的时间百分比。 （Linux 2.6.11）

	4）free

	Memory性能分析工具：
	vmstat
	strace
	top
	ipcs
	ipcrm
	cat /proc/meminfo
	cat /proc/slabinfo
	cat /proc/<pid #>/maps

# 3.  磁盘I/O可调性能参数 #

	1）选择适合应用的文件系统;
	2）调整进程I/O请求的优先级，分三种级别：1代表 real time ; 2代表best-effort; 3代表idle ;
	如：ionice -c1 -p1113(给进程1113的I/O优先级设置为最高优先级）
	3）根据应用类型，适当调整page size 和block size;
	4）升级驱动程序
	5）iostat

# 4. 使用寄存器变量 #

	当对一个变量频繁被读写时，需要反复访问内存，从而花费大量的存取时间。为此，C语言提供了一种变量，即寄存器变量。
	这种变量存放在CPU的寄存器中，使用时不需要访问内存，而直接从寄存器中读写，从而提高效率。
	
	寄存器变量的说明符是register。
	对于循环次数较多的循环控制变量及循环体内反复使用的变量均可定义为寄存器变量，而循环计数是应用寄存器变量的最好候选者。
	
	注意：
	(1) 只有局部自动变量和形参才可以定义为寄存器变量。
	因为寄存器变量属于动态存储方式，凡需要采用静态存储方式的量都不能定义为寄存器变量，包括：模块间全局变量、模块内全局变量、局部static变量
	
	(2) register是一个"建议"型关键字，意指程序建议该变量放在寄存器中，但最终该变量可能因为条件不满足并未成为寄存器变量，而是被放在了存储器中

# page cache #
	
	参考： https://blog.csdn.net/juS3Ve/article/details/80115540
	
	Linux下读写文件，主要有两种方式：

	（1）read/write

		调用read读文件，Linux内核会申请一个page cache，然后把文件读到page cache中，再将内核空间的page cache拷贝到用户空间的buf。
		调用write写文件，则将用户空间buf拷贝到内核空间page cache。

	（2）mmap

		mmap可以避免buf从用户空间到内核空间的拷贝过程。
		直接把文件映射成一个虚拟地址指针，这个指针指向内核申请的page cache。内核知道page cache与硬盘中文件的对应关系。
		page cache可以看作内存针对磁盘的一个缓存，应用程序在写文件时，其实只是将内容写入了page cache，使用sync才能真的写入文件。

	cache可以通过/proc/sys/vm/drop_caches强行释放，写1释放page cache，2释放dentries和inode，3释放两者。
	

# swap #

	匿名页（比如用户进程通过malloc申请的内存页是没有关联任何文件的）和文件背景的页面(基于磁盘文件的内存页)都需要swap。
	有文件背景的页面向自己的文件背景中交换, 匿名页向swap分区和swapfile中交换。
	
	即使编译内核时将CONFIG_SWAP关闭（只是关闭了匿名页的交换），kswapd线程还是会swap有文件背景的页面。

	Linux有三个水位：min，low，high。一旦内存达到低水位时，后台自动回收直到回收到高水位。当内存到达min水位时，直接堵住进程，进行回收。
	
	匿名页和有文件背景的页面都有可能被回收，
	/proc/sys/vm/swappiness 值比较大时，倾向回收匿名页；swappiness值比较小时倾向回收有文件背景的页面。回收算法皆为LRU。
	
	swappiness反应是否积极使用swap空间，默认是60，
	swappiness=0表示仅在内存不足时使用swap空间（free and file-backed pages< high watermark in zone)

	内存换出到swap的过程:
	kswapd（）-->balance_pgdat()-->shrink_zone（）-->shrink_inactive_list（）-->shrink_page_list()（核心函数）-_swap()-->get_swap_page()

# free 命令 #

	参考： https://blog.csdn.net/huangjin0507/article/details/51178768
	
	free默认单位是KB
	
	
	$ free  
				 total	   used	   free	 shared	buffers	 cached（有的时候没有cached这一项）  
	Mem:	   3894036	3473544	 420492		  0	  72972	1332348  
	-/+ buffers/cache:	2068224	1825812  
	Swap:	  4095992	 906036	3189956
	
	--------第一行数据：代表内核角度的统计--------
	total1：表示物理内存总量（排除了kernel代码/数据段占用、保留的内存区）
	used1：表示已使用（已分配出去）的物理内存总量，包括真正已使用和分配给缓存（包含buffers 与cached）的数量。
	free1：未被分配的物理内存。
	如果你认为这个系统空闲内存太小，那就错了，实际上，内核会在需要内存的时候，将buffers和cached状态的内存变为free状态的内存。
	shared1：共享内存（一般可以不理）。
	
	buffers1：表示块设备(block device)所占用的缓存页，包括直接读写块设备、以及文件系统元数据(metadata)如SuperBlock所使用的缓存页.
			如：直接访问/dev/sda1时，如用户程序直接打开open(“dev/sda1…)或执行dd命令，以及文件系统本身去访问裸分区，
	
	cached1：表示普通文件所占用的缓存页. 一般当以文件系统（ext4,xfs等）的形式去访问文件系统中的文件，如mount /dev/sda1 /mnt后，/mnt目录下会有很多文件
	
	buffers与cached都是文件系统的缓存，没有本质区别，唯一区别是背景不同
	
	--------第二行数据：代表应用角度的统计--------
	used2：实际使用内存总量。
	free2：系统当前实际可用内存，包括未被分配的内存以及分配给buffers 与cached 的内存之和。
		对于应用程序来说，buffers/cached占有的内存是可用的，因为buffers/cached是为了提高文件读取的性能，
		当应用程序需要用到内存的时候，buffers/cached会很快地被回收，以供应用程序使用。
	
	可以整理出如下等式：
	total1 = used1 + free1
	total1 = used2 + free2
	used1 = buffers1 + cached1 + used2
	free2 = buffers1 + cached1 + free1
	
	
	
- 释放Cache Memory
	
		To free page cache(页缓存):
		echo 1 > /proc/sys/vm/drop_caches
		
		To free dentries and inodes(inode和目录树缓存):
		echo 2 > /proc/sys/vm/drop_caches
		
		To free pagecache, dentries and inodes:
		echo 3 > /proc/sys/vm/drop_caches
	
		实例：用free命令查看释放cache后的free memory的变化
		
		$ sync  //在清空缓存之前使用sync命令同步数据到磁盘
		$ free -m
					  total	   used	   free		shared	buffers		 cached
		Mem:		   499		323		175		  0		 52				188
		-/+ buffers/cache:		 82		416
		Swap:		 2047		  0		2047
		
		$ echo 3 > /proc/sys/vm/drop_caches
		$ free -m	 //发现缓存明显减少了
					  total	   used		free		shared	buffers		 cached
		Mem:		   499		 83		 415		  0		  1				17
		-/+ buffers/cache:		 64		 434
		Swap:		 2047		  0		 2047
	
	

# /proc/meminfo #

	参考
	https://blog.csdn.net/u014089131/article/details/52814516
	https://blog.csdn.net/cnctloveyu/article/details/4074892
	http://blog.chinaunix.net/uid-16974460-id-1729258.html
	
	代码见meminfo.c, 接口：proc_create(“meminfo”,****，)
	
	MemTotal：可用的总内存= 总物理内存 - kernel代码/数据段占用-保留的内存区。mem_init_print_info里面有具体计算方式
	
	
	MemFree：完全未用到的物理内存, LowFree+HighFree
	
	
	MemAvailable:MemFree+Active(file)+Inactive(file)-(watermark+min(watermark,Active(file)+Inactive(file)/2))
	file占用的内存是可以释放的，但是释放的过多，会导致swap发生，减去部分内存的目的是避免swap
	
	
	Buffers：用于块设备(block device)的page缓冲
	long nr_blockdev_pages(void)
	{
		struct block_device *bdev;
		long ret = 0;
		spin_lock(&bdev_lock);
		list_for_each_entry(bdev, &all_bdevs, bd_list) {
			ret += bdev->bd_inode->i_mapping->nrpages;
		}
		spin_unlock(&bdev_lock);
		return ret;
	}
	
	
	Cached：普通文件占用的缓冲
	global_page_state(NR_FILE_PAGES) – total_swapcache_pages – i.bufferram
	
	NR_FILE_PAGES：所有缓冲页(page cache)的总和，包括 cached+buffer+swap cache
	swap cache包含的是被确定要swapping换页、但是尚未写入物理交换区的匿名内存页(匿名指的是未关联任何具体文件)
	
	
	
	SwapCached：内存足够的情况下，这个值一般为0.
	那些匿名内存页，如果发生swapping换页，这类内存页会被写入交换区。
	一个匿名内存页从被确定要被换页开始，它就被计入了swap cache，但是不一定会被立刻写入物理交换区，因为Linux的原则是除非绝对必要，尽量避免I/O,
	所以swap cache中包含的是被确定要swapping换页、但是尚未写入物理交换区的匿名内存页。
	
	
	Active：  pages[LRU_ACTIVE_ANON]  + pages[LRU_ACTIVE_FILE]
	Inactive：pages[LRU_INACTIVE_ANON] + pages[LRU_INACTIVE_FILE]
	
	ACTIVE_ANON和ACTIVE_FILE，分别表示anonymous pages和mapped pages
	用户进程的内存页分为两种：与文件关联的内存（比如程序文件、数据文件所对应的内存页）和与文件无关的内存（比如进程的堆栈，用malloc申请的内存），
	前者称为file pages或mapped pages，后者称为anonymous pages.
	
	HighMem/LowMem是32bitX86 上面的一种划分，860MB以上内存成为HighMem，ARM架构上面没有这样的划分方式；
	
	
	swap分区参数：Swap分区在系统的物理内存不够用的时候，把硬盘空间中的一部分空间释放出来，以供当前运行的程序使用
	SwapTotal：可用的swap空间的总的大小
	SwapFree：剩余swap空间的大小
	
	
	
	
	Dirty：需要写入磁盘的内存区大小
	
	Writeback：正在被写回磁盘的大小
	
	AnonPages：未映射页的内存大小
	
	Mapped: 设备和文件等映射的大小。
	
	Slab: 内核数据结构slab的大小，可以减少申请和释放内存带来的消耗。
	
	SReclaimable:可收回Slab的大小
	
	SUnreclaim：不可收回Slab的大小（SUnreclaim+SReclaimable＝Slab）
	
	PageTables：管理内存分页页面的索引表的大小。
	
	NFS_Unstable:不稳定页表的大小
	
	VmallocTotal: vmalloc内存区大小
	VmallocUsed: 已用的vmalloc区大小
	VmallocChunk: vmalloc区可用的连续最大块的大小
	

# 查看所有cpus上的时间消耗 #

	参考
	http://www.cnblogs.com/no7dw/archive/2011/07/04/2097300.html
	
	
	在Linux/Unix下，CPU利用率分为用户态，系统态和空闲态，
	分别表示CPU处于用户态执行的时间，系统内核执行的时间，和空闲系统进程执行的时间。
	平时所说的CPU利用率是指：CPU执行非系统空闲进程的时间 / CPU总的执行时间
		
	1）cat /proc/stat
	
	[sailorhzr@builder ~]$ cat /proc/stat
	cpu 432661 13295 86656 422145968 171474 233 5346
	cpu0 123075 2462 23494 105543694 16586 0 4615
	cpu1 111917 4124 23858 105503820 69697 123 371
	cpu2 103164 3554 21530 105521167 64032 106 334
	cpu3 94504 3153 17772 105577285 21158 4 24
	intr 1065711094 1057275779 92 0 6 6 0 4 0 3527 0 0 0 70 0 20 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7376958 0 0 0 0 0 0 0 1054602 0 0 0 0 0 0 0 30 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
	ctxt 19067887
	btime 1139187531
	processes 270014
	procs_running 1
	procs_blocked 0

	输出解释

	CPU 以及CPU0、CPU1、CPU2、CPU3每行的每个参数意思（以第一行为例）：
	参数		   解释
	user (432661)	 从系统启动开始累计到当前时刻，用户态的CPU时间（单位：jiffies） ，不包含 nice值为负进程。1jiffies=0.01秒
	nice (13295)	  从系统启动开始累计到当前时刻，nice值为负的进程所占用的CPU时间（单位：jiffies）
	system (86656)	 从系统启动开始累计到当前时刻，内核时间（单位：jiffies）
	
	idle (422145968) 从系统启动开始累计到当前时刻，除硬盘IO等待时间以外其它等待时间（单位：jiffies）
	iowait (171474) 从系统启动开始累计到当前时刻，硬盘IO等待时间（单位：jiffies）
	irq (233)		 从系统启动开始累计到当前时刻，硬中断时间（单位：jiffies）
	softirq (5346)	 从系统启动开始累计到当前时刻，软中断时间（单位：jiffies）
	
	CPU时间=user+system+nice+idle+iowait+irq+softirq
	
	“intr”这行给出中断的信息，第一个为自系统启动以来，发生的所有的中断的次数；
	然后每个数对应一个特定的中断自系统启动以来所发生的次数。

	“ctxt”给出了自系统启动以来CPU发生的上下文交换的次数。
	“btime”给出了从系统启动到现在为止的时间，单位为秒。
	“processes (total_forks) 自系统启动以来所创建的任务的个数目。
	“procs_running”：当前运行队列的任务的数目。
	“procs_blocked”：当前被阻塞的任务的数目。
	
	那么CPU利用率可以使用以下两个方法。先取两个采样点，然后计算其差值：
	cpu usage=(idle2-idle1)/(cpu2-cpu1)*100
	cpu usage=[(user_2 +sys_2+nice_2) - (user_1 + sys_1+nice_1)]/(total_2 - total_1)*100

	2）cat /proc/stat的源代码
	
	fs/proc/stat.c
	proc_create(“stat”,0, null, &proc_stat_operations)
	static int show_stat(struct seq_file *p, void *v)
		
# **进程的cpu和内存消耗情况** #

	top -m 10 -s cpu（-m显示最大数量，-s 按指定行排序）

	
# **看进程占用的内存等信息**  #

	Cat  /proc/<pid>/status
	
	FDSize是当前分配的文件描述符,这个值不是当前进程使用文件描述符的上限.
	VmPeak: 当前进程运行过程中占用内存的峰值.
			除了我们申请的内存外,还加上为加载动态链接库而占用的内存
	VmSize代表进程现在正在占用的内存
	VmLck代表进程已经锁住的物理内存的大小.锁住的物理内存不能交换到硬盘.
	VmRSS是程序现在使用的物理内存
	VmHWM是程序得到分配到物理内存的峰值.
	VmData:表示进程数据段的大小
	VmStk:表示进程堆栈段的大小.
	VmExe:表示进程代码的大小.
	VmLib:表示进程所使用LIB库的大小.
	代码段可以为机器中运行同一程序的数个进程共享
	堆栈段存放的是子程序（函数）的返回地址、子程序的参数及程序的局部变量
	数据段则存放程序的全局变量、常数以及动态数据分配的数据空间（比如用malloc函数申请的内存）
	与代码段不同，如果系统中同时运行多个相同的程序，它们不能使用同一堆栈段和数据段.
	VmPTE: 占用的页表的大小
	VmSwap: 进程占用Swap的大小
	Threads:表示当前进程组有几个线程
	SigQ: 表示当前待处理信号的个数
	voluntary_ctxt_switches表示进程主动切换的次数.
	nonvoluntary_ctxt_switches表示进程被动切换的次数.
	详细见：http://blog.chinaunix.net/uid-22028680-id-3195672.html


# 进程的memory map #

- 1) cat /proc/<pid>/maps
	
		00fcc000-00fcd000 r-xp 00000000 03:01 1238761 /root/test/gdbservertest/libtest.so
		00fcd000-00fce000 rwxp 00000000 03:01 1238761 /root/test/gdbservertest/libtest.so
		08048000-08049000 r-xp 00000000 03:01 1238765 /root/test/gdbservertest/test.exe
		08049000-0804a000 rw-p 00000000 03:01 1238765 /root/test/gdbservertest/test.exe
		
- 2) cat /proc/<pid>/smaps

		12c00000-12c01000 rw-p 00000000 00:01 6096							   /dev/ashmem/dalvik-main space_649_649 (deleted)
		Size:				  4 kB
		Rss:				   4 kB
		Pss:				   4 kB
		Shared_Clean:		  0 kB
		Shared_Dirty:		  0 kB
		Private_Clean:		 0 kB
		Private_Dirty:		 4 kB
		Referenced:			4 kB
		Anonymous:			 4 kB
		AnonHugePages:		 0 kB
		Swap:				  0 kB
		SwapPss:			   0 kB
		KernelPageSize:		4 kB
		MMUPageSize:		   4 kB
		Locked:				0 kB
		VmFlags: rd wr mr mw me ac
		
		解析 smaps的脚本： linux_smap_analyzer.py， 其中对各种内存进行了统计（包括stack,so,dex）
		见：https://gist.github.com/LanderlYoung/aedd0e1fe09214545a7f20c40c01776c
		结果如下：
		map Pss total = 189260 Kb
		map Vss total = 2690944 Kb
		stacks Pss = 3056 kB
		stacks Vss = 194656 kB
		all so map Pss = 8478 kB
		all so map Vss = 130780 kB
		all dex map Pss = 62834 kB
		all dex map Vss = 115160 kB
		app so map Rss
		app so map Rss = 0 kB
		app so map Vss = 0 kB
		app dex map Rss
		app dex map Rss = 17440 kB

		
# 其他 #

	Ls  /proc/<pid>/task   #可以查看该进程组内所有的pid
	Cat  /proc/<pid>/task/<pid2>/status #看进程组内的其他进程的信息
	procrank  #查看进程占用的内存

	相关全局变量:tgid_base_stuff[] 