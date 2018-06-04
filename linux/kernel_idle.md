# 0号进程上下文信息–init_task描述符 #

    init_task是内核中所有进程、线程的task_struct雏形，在内核初始化过程中，通过静态定义构造出了一个task_struct接口，
	取名为init_task，然后在内核初始化的后期，通过rest_init（）函数新建了内核init线程，kthreadd内核线程。
    
    1) 内核init线程，最终执行/sbin/init进程，变为所有用户态程序的根进程（pstree命令显示）,即用户空间的init进程
    
    开始的init是由kthread_thread创建的内核线程, 他在完成初始化工作后, 转向用户空间, 并且生成所有用户进程的祖先
    
    2)内核kthreadd内核线程，变为所有内核态其他守护线程的父线程。
    
    它的任务就是管理和调度其他内核线程kernel_thread, 会循环执行一个kthread的函数，
	该函数的作用就是运行kthread_create_list全局链表中维护的kthread, 
	当我们调用kernel_thread创建的内核线程会被加入到此链表中，因此所有的内核线程都是直接或者间接的以kthreadd为父进程
    
    ps-aux
    
    3) 所以init_task决定了系统所有进程、线程的基因, 它完成初始化后, 最终演变为0号进程idle, 并且运行在内核态
    
    内核在初始化过程中，当创建完init和kthreadd内核线程后，内核会发生调度执行，
	此时内核将使用该init_task作为其task_struct结构体描述符，当系统无事可做时，会调度其执行， 
	此时该内核会变为idle进程，让出CPU，自己进入睡眠，不停的循环，查看init_task结构体，其comm字段为swapper，作为idle进程的描述符。
    
    4) idle的运行时机
    
    idle 进程优先级为MAX_PRIO-20。早先版本中，idle是参与调度的，所以将其优先级设低点，当没有其他进程可以运行时，才会调度执行 idle。
    而目前的版本中idle并不在运行队列中参与调度，而是在运行队列结构中含idle指针，指向idle进程，在调度器发现运行队列为空的时候运行，调入运行。
    
    简言之, 内核中init_task变量就是是进程0使用的进程描述符，也是Linux系统中第一个进程描述符，
	init_task并不是系统通过kernel_thread的方式（当然更不可能是fork）创建的, 而是由内核黑客静态创建的.


# idle的workload–cpu_idle_loop #

    从上面的分析我们知道，idle在系统没有其他就绪的进程可执行的时候才会被调度。不管是主处理器，还是从处理器，最后都是执行的cpu_idle_loop()函数。
 
    其中cpu_idle_loop就是idle进程的事件循环，定义在kernel/sched/idle.c，早期的版本中提供的是cpu_idle，
	但是这个函数是完全依赖于体系结构的，不利用架构的分层，因此在新的内核中更新为更加通用的cpu_idle_loop，
	由他来调用体系结构相关的代码, 所以我们来看看cpu_idle_loop做了什么事情。
    
    因为idle进程中并不执行什么有意义的任务，所以通常考虑的是两点:
    节能
    低退出延迟
    
    循环判断need_resched以降低退出延迟，用idle()来节能。
    
    默认的idle实现是hlt指令，hlt指令使CPU处于暂停状态，等待硬件中断发生的时候恢复，从而达到节能的目的。
	即从处理器C0态变到 C1态(见 ACPI标准)。这也是早些年windows平台上各种”处理器降温”工具的主要手段。
	当然idle也可以是在别的ACPI或者APM模块中定义的，甚至是自定义的一个idle(比如说nop)。
    
    　　1.idle是一个进程，其pid为0。
    
    　　2.主处理器上的idle由原始进程(pid=0)演变而来。从处理器上的idle由init进程fork得到，但是它们的pid都为0。
    
    　　3.Idle进程为最低优先级，且不参与调度，只是在运行队列为空的时候才被调度。
    
    　　4.Idle循环等待need_resched置位。默认使用hlt节能。

# idle的调度和运行时机 #

	我们知道, linux进程的调度顺序是按照 rt实时进程(rt调度器), normal普通进程(cfs调度器)，和idel的顺序来调度的
	
	那么可以试想如果rt和cfs都没有可以运行的任务，那么idle才可以被调度，那么他是通过怎样的方式实现的呢？
	
	在normal的调度类,cfs公平调度器sched_fair.c中, 我们可以看到
	
	static const struct sched_class fair_sched_class = {
	.next = &idle_sched_class,

	也就是说，如果系统中没有普通进程，那么会选择下个调度类优先级的进程，即使用idle_sched_class调度类进行调度的进程
	当系统空闲的时候，最后就是调用idle的pick_next_task函数，被定义在/kernel/sched/idle_task.c中
	
	static struct task_struct *pick_next_task_idle(struct rq *rq)
	{
	        schedstat_inc(rq, sched_goidle);
	        calc_load_account_idle(rq);
	        return rq->idle;    //可以看到就是返回rq中idle进程。
	}

	这idle进程在启动start_kernel函数的时候调用init_idle函数的时候，把当前进程（0号进程）置为每个rq运行队列的的idle上。
	
参考：http://blog.csdn.net/gatieme/article/details/51484562