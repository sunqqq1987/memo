# 并发和竞态 #

	参考： https://blog.csdn.net/geng823/article/details/37657273

	1）atomic_xx 函数
	底层实现依赖于ldres,strex指令。
	由于这个函数只是对整数操作，所以不会收中断的影响。

	文件：<asm/atomic.h>

	2）自旋锁 spin_lock
	底层实现依赖于ldres,strex指令，内存屏障dmb,dsb,wfe,sev指令。
	spinlock只能保证临界区不受其他CPU和本CPU的抢占进程打扰，但是无法避免受到中断和中断下半部分的影响。
	因此在进程上下文中使用spin_lock_irq 或 spin_lock_irqsave, 在中断上下中使用spin_lock.

	spinlock 会关抢断
	需要注意：
	spinlock后的临界区内不能有引起进程调度的函数，如：
	copy_from_user, copy_to_user, kmalloc, malloc, msleep，down()等

	使用原则： 自旋锁必须是尽可能短时间持有

	文件： <linux/spinlock.h>

	3）`读写(自旋)锁 rwlock_t
	改进了spinlock, 允许多个同时读，但读写、写写都是互斥的，且只能有一个写者。
	也有带关中断的版本 read_lock_irqsave, write_lock_irq_save
	
	这有点儿类似RCU机制，适合频繁读取数据，而写入操作相对比较少的场景，下面我们看看读写锁的实现原理：
	读写锁包括读取锁和写入锁.
	(1)锁变量的初值是__ARCH_RW_LOCK_UNLOCKED，0表示未锁状态；
	(2)写入锁检查锁变量，如果是未锁状态，则锁变量的第31位置位（0x80000000），否则等待锁变量被释放；释放写入锁，也就是清除锁变量的第31位；
	(3)读取锁检查锁变量的第31位是否置位，是则等待释放写入锁，然后给锁变量加1；释放读取锁时，锁变量减1；
	参考：arch_read_lock(arch_rwlock_t *rw)
	
	
	4) 顺序锁 seqlock: 对读写自旋锁的优化
	读者间、读和写者间都不互斥，但多个写者间是互斥的。
	如果读期间有发生写，那么只有重新读才可能读到有效的数据，因此有可能出现反复读的情况。

	用于：要保护的资源小, 简单, 并且常常被存取, 并且很少写但是必须要快。

	write_seqlock, write_seqlock_irqsave
	read_seqbegin, read_seqbegin_irqsave, read_seqretry

	文件： <linux/seqlock.h>

	5) RCU（读-复制-更新): 不是锁机制
	优点： 允许多个读和多个写单元间能同时访问共享资源。

	在写者在访问共享资源前，首先复制一个副本，然后写者对副本进行修改;
	并用副本代替原来共享资源，但此时并不销毁原来共享资源, 而是通过callback机制在适当的时机把它销毁。
	这个时机是所有引用共享资源的进程都退出了对共享资源的读操作的时候，我们把这段等待时间叫做宽限期（grace period)。

	用于: 需要频繁的读取数据、而相应修改数据并不多的场景。

	缺点： 如果有写比较多的时候，对读者性能的提高不能弥补写者同步带来的损失，此时不能代替读写锁。
	
	synchronize_rcu(): 由写者调用，他会阻塞写单元，直到当前CPU上所有的已存在的读者完成共享资源的访问。

	文件： <linux/rcupdate.h>

	6) 信号量semaphore
	用于同步和互斥的典型手段，同步对应于操作系统中的PV操作。
	但用于互斥时，linux倾向于用mutex。
	文件： <asm/semaphore.h>

	DECLARE_MUTEX(name);  //2 个宏定义, 用来声明和初始化一个在互斥模式下使用的信号量.
	DECLARE_MUTEX_LOCKED(name);
	
	void init_MUTEX(struct semaphore *sem); //这 2 函数用来在运行时初始化一个信号量.  
	void init_MUTEX_LOCKED(struct semaphore *sem);
	
	down()与down_interruptible()的区别：前者引起的睡眠不能被信号打断，而后者可以.

	rwsem: 读写信号量
	读写信号量比mutex有更高的适用性： 多个线程同时占用读模式，但是只能一个线程占用写模式。
	(1) 当读写锁是写加锁状态时，在这个锁被解锁之前，所有试图对这个锁加锁的线程都会被阻塞；
	(2) 当读写锁在读加锁状态时，所有试图以读模式对它进行加锁的线程都可以得到访问权，但是以写模式对它进行加锁的线程将阻塞；
	(3) 当读写锁在读模式锁状态时，如果有另外线程试图以写模式加锁，读写锁通常会阻塞随后的读模式锁请求，
		这样可以避免读模式锁长期占用，而等待的写模式锁请求长期阻塞；

	适用于： 进行读的次数比写的次数多的情况

	struct rw_semaphore;
	init_rwsem(struct rw_semaphore *sem)
	void down_read(struct rw_semaphore *sem)
	void up_read(struct rw_semaphore *sem)
	void down_write(struct rw_semaphore *sem)
	void up_write(struct rw_semaphore *sem)

	7) 互斥体 mutex
	mutex与自旋锁的选择：

	(1) 自旋锁是更底层的操作，是cpu忙等，适用于临界区较小的情况；
		mutex是进程级别的互斥，用于开销大的场景，它的实现依赖于自旋锁。
	(2) mutex保护的临界区有可能引起阻塞，而自旋锁要避免保护带来阻塞的代码，因为阻塞带来的进程切换，
		使得新进程有可能会获取同一个自旋锁，从而导致死锁。
	(3) mutex只能用于进程上下文，不能用于中断或软中断下；
		如果共享资源要在中断或软中断的环境下被使用，那么用自旋锁。
		如果非要用互斥体，那么用mutex_trylock()来做（不能获取就立即返回）。

	8) 完成量 completion
	允许一个线程告诉另一个线程工作已经完成, 用于一个进程等待另一个进程执行完某个动作。
	文件： <linux/completion.h>
	
	init_completion(struct completion *c);
	INIT_COMPLETION(struct completion c);
	void wait_for_completion(struct completion *c) //等待一个 completion 事件发出.
	void complete(struct completion *c);

	9) 等待队列 __wait_queue_head
	实现进程的阻塞和唤醒
	文件： <linux/wait.h>
	
	wake_up()可以唤醒INTERRUPTIBLE和UNINTERRUPTIBLE进程
	wake_up_interruptible()只能唤醒处于INTERRUPTIBLE的进程

	成对使用：
	sleep_on()   / wake_up() //主动睡眠
	wait_event() / wake_up() //等待事件发生
	wait_event_interruptible(queue, condition) / void wake_up_interruptible(wait_queue_head_t *queue)
	wait_event_timeout(wait_queue_head_t q, condition, long timeout)
	=> 如果你的驱动使用一个等待队列来等待某些其他事件, 但是你也想确保它在一个确定的时间后返回

	独占等待:
	当一个等待队列入口有 WQ_FLAG_EXCLUSEVE 标志置位, 它被添加到等待队列的尾部

	10）同时获取多个锁（建议尽力避免需要多于一个锁的情况）
	解决方法常常是: 当必须多个锁获得时, 它们应当一直以同样顺序获得。
	但是往往要参考其他的代码来实现，经验有：
	（1）如果必须获得一个对你的代码来说的本地锁, 以及一个属于内核更中心部分的锁, 先获取你的
	（2）如果是一个信号量和自旋锁的组合, 你必须先获得信号量 