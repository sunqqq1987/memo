# KMEMLEAK #

	参考
	http://blog.chinaunix.net/uid-26859697-id-5758037.html
	http://linuxperf.com/?p=188

- kmemleak原理

		kmemleak把kmalloc()、vmalloc()、kmem_cache_alloc()等函数分配的内存的指针和大小、时间、stack trace等信息记录在一个rbtree中，
		当调用free释放内存时就把相应的记录从rbtree中删除，这样rbtree中的记录就是已经分配出去但尚未释放的内存。
		这些内存中，尚未释放的情况分为2种：1是因为还在使用，这属于正常情况；2是内存尚未释放但又不会再被使用，这就是“泄漏”的内存。
	
		那如何找出泄漏的内存呢？
		kmemleak默认每10分钟对内存做一次扫描，
		最后把这些泄漏的内存地址以及rbtree中记录的时间、大小、strack trace等相关信息通过 /sys/kernel/debug/kmemleak 这个接口展现给我们。
		
		扫描算法见kmemleak_scan():
	
		1) 标记红黑树中所有的object（对应一个指针）为白色(即object没有被任何东西引用，是孤立的）
	
		2) 从data和stack区开始起，扫描内存，如果内存该处的值正好是红黑树中的某个object，
		那么这个object的引用计数+1， 当计数达到min_count时（即至少有min_count个地方引用了该object)，
		则把它加入到gray_list中，表示该object是被人引用了（即不是孤立的）
	
		3）依次扫描gray_list中的object1, 对这个object1指针可能包括的其他内存范围进行扫描，
		如果某内存处的指针对应的object正好也在红黑树中，然后采用2）中类似的处理，尽可能将object加入到gray_list中.
	
		4）最后，红黑树中剩余的白色object就被认为是孤立的（很可能是泄漏的）。它们可以通过 /sys/kernel/debug/kmemleak 来输出
	
		注意， kmemleak的扫描算法存在误报的可能，比如：
		1）内存中碰巧有一个数据与rbtree中的某个地址相同，但它只是数据而非指针，kmemleak是无法分辨的，会认为它是正常使用中的内存块
	
		所以，kmemleak工具的目的是为了给进一步分析提供线索，并不绝对精确。

- 使能 kmemleak

		1) 打开以下config

		CONFIG_DEBUG_KMEMLEAK=y
	
		CONFIG_DEBUG_KMEMLEAK_EARLY_LOG_SIZE=400  //如果要记录kmemleak模块初始化前的内存分配和释放情况，那么这size决定了可以记录多少信息
	
		# CONFIG_DEBUG_KMEMLEAK_TEST is not set  //用于自测
	
		CONFIG_DEBUG_KMEMLEAK_DEFAULT_OFF=n  //是否使能kmemleak, y表示不使能。 
		使能，有2种方式：
		(1）CONFIG_DEBUG_KMEMLEAK_DEFAULT_OFF=n
		(2）如果CONFIG_DEBUG_KMEMLEAK_DEFAULT_OFF=y时，仅需在kernel cmdline中设置：kmemleak=on。 原因见kmemleak.c
	
		如果要关闭kmemleak，可以在kernel cmdline中设置：kmemleak=off, 即使相关config已经enable了。

		2) mount -t debugfs nodev /sys/kernel/debug/
		
		3) 立即触发内存扫描： echo scan > /sys/kernel/debug/kmemleak
		
		4) 查看leak结果： cat /sys/kernel/debug/kmemleak
		
		其他：
		1) 清除之前扫描到的可能的leak信息，以便开始新的扫描：
			echo clear > /sys/kernel/debug/kmemleak
		
		具体见使用手册：https://www.kernel.org/doc/html/latest/dev-tools/kmemleak.html
		documention/kmemleak.txt
	
		实例：
		# cat /sys/kernel/debug/kmemleak
		unreferenced object 0xffff88003cff1260 (size 32):
		  comm "softirq", pid 0, jiffies 4297625839
		  hex dump (first 32 bytes):
			f0 a1 9b 35 00 00 00 00 0c 00 00 00 01 00 01 00  ...5............
			da c0 70 3a 00 00 00 00 2a 00 00 00 00 00 00 00  ..p:....*.......
		  backtrace:
			[<ffffffff8156585e>] kmemleak_alloc+0x5e/0xe0
			[<ffffffff8119c622>] __kmalloc+0x1f2/0x330
			[<ffffffffa0056800>] virtqueue_add_buf+0x2c0/0x5e0 [virtio_ring]
			[<ffffffffa0140ee7>] start_xmit+0x1a7/0x460 [virtio_net]
			[<ffffffff814ac0dc>] dev_hard_start_xmit+0x22c/0x4a0
			[<ffffffff814cbce6>] sch_direct_xmit+0x166/0x1d0
			[<ffffffff814ac8a8>] dev_queue_xmit+0x268/0x380
			[<ffffffff815123b8>] arp_xmit+0x58/0x60
			[<ffffffff81512903>] arp_send+0x43/0x50
			[<ffffffff81513316>] arp_solicit+0x236/0x2b0
			[<ffffffff814b7aa1>] neigh_timer_handler+0xf1/0x370
			[<ffffffff81094a5e>] run_timer_softirq+0x20e/0x3e0
			[<ffffffff81089b6f>] __do_softirq+0xff/0x260
			[<ffffffff8100c48c>] call_softirq+0x1c/0x30
			[<ffffffff8100fe6d>] do_softirq+0xad/0xe0
			[<ffffffff81089885>] irq_exit+0x95/0xa0