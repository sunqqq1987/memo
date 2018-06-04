
# 抢占 #

- preempt_count

		struct thread_info {
			unsigned long	flags;	/* low level flags ,如TIF_NEED_RESCHED 表示运行队列上有新的task需要被调度*/
			int		preempt_count;	/* 0 => preemptable, <0 => bug */
		 …
		};
		
		 1) flags值
		 *  TIF_SIGPENDING	- signal pending  //有信号没有处理
		 *  TIF_NEED_RESCHED	- rescheduling necessary  //当一个睡眠的进程被唤醒，当其要加入运行队列时，如果其动态优先级比当前正在运行进程current的优先级高，
								那么会在current线程上设置TIF_NEED_RESCHED,以告诉内核，有新的高优先级的线程在等待内核调度。
								通常，一个睡眠的进程会在中断处理函数中被唤醒。


		2）进程的((struct thread_info *)(task->stack))->preempt_count（线程的抢占计数器）：
		
		==0, 表示线程可以被抢占,即可以发生内核抢占。
		
		> 0, 表示禁止抢占当前线程，即禁止内核抢占.
		因为此时发生内核抢占不安全，比如进程持有内核的锁。
		该值中具体位的意思见文件：Hardirq.h (\kernel\include\linux)
		此时又分为：
			1）preempt_count的低8位表示：当前线程被加锁的次数，比如调用了_raw_spin_trylock()（也会关闭中断），该值会+1
			2）preempt_count的中间8位表示：当前线程禁止soft irq和tasklet下半段（或者说推迟函数被禁止）的次数,见__local_bh_disable(SOFTIRQ_OFFSET)和local_bh_disable()
			3）preempt_count的bit[16-25]表示：当前线程被硬中断打断的次数,见irq_enter() 
			4）preempt_count的bit 26 表示：当前线程被非屏蔽中断抢占的次数
			5）preempt_count的bit 30 表示：当前进程上是否已经发生内核抢占，一般为1，线程被内核其他线程抢占的时候不能再被抢占
		  
		/*
		* We put the hardirq and softirq counter into the preemption
		* counter. The bitmask has the following meaning:
		*
		* - bits 0-7 are the preemption count (max preemption depth: 256)
		* - bits 8-15 are the softirq count (max # of softirqs: 256)
		*
		* The hardirq count can in theory reach the same as NR_IRQS.
		* In reality, the number of nested IRQS is limited to the stack
		* size as well. For archs with over 1000 IRQS it is not practical
		* to expect that they will all nest. We give a max of 10 bits for
		* hardirq nesting. An arch may choose to give less than 10 bits.
		* m68k expects it to be 8.
		*
		* - bits 16-25 are the hardirq count (max # of nested hardirqs: 1024)
		* - bit 26 is the NMI_MASK
		* - bit 28 is the PREEMPT_ACTIVE flag  //貌似被重新定义到第30bit了
		*
		* PREEMPT_MASK: 0x000000FF
		* SOFTIRQ_MASK: 0x0000FF00
		* HARDIRQ_MASK: 0x03FF0000
		*   NMI_MASK: 	0x04000000
		*/
		#define PREEMPT_BITS	8
		#define SOFTIRQ_BITS	8
		#define NMI_BITS	1

		#define MAX_HARDIRQ_BITS 10

		#ifndef HARDIRQ_BITS
		# define HARDIRQ_BITS	MAX_HARDIRQ_BITS
		#endif
		
		3） 通过把抢占计数器设置为正而显式禁止内核抢占，由preempt_disable完成。

		抢占计数的增减本质上都是通过以下宏来实现的，有些函数只是它们的封装：
		# define add_preempt_count(val)	do { preempt_count() += (val); } while (0)
		# define sub_preempt_count(val)	do { preempt_count() -= (val); } while (0)

		注意锁相关的封装宏如下：
		#define preempt_disable()
			->#define inc_preempt_count() add_preempt_count(1)
		#define preempt_enable()
			->... sub_preempt_count(1)
			
		#define preempt_check_resched() \
		do { \
			if (unlikely(test_thread_flag(TIF_NEED_RESCHED))) \
				preempt_schedule(); \
		} while (0)

		4） 宏CONFIG_PREEMPT：表示是否开启抢占当前线程的功能（包括内核态抢占和用户态抢占）

- 用户抢占

		用户抢占指的是：当内核即将返回用户空间时，如果进程的TIF_NEED_RESCHED 标记被设置，
		那么会导致schedule()被调用，此时发生用户抢占。

		一般发生在以下情况：
		
		1）从中断处理程序返回用户空间时
		
		entry-armv.S (\kernel\arch\arm\kernel)
		
			__irq_usr: //usr模式下的IRQ入口
			usr_entry
			kuser_cmpxchg_check
			irq_handler
			get_thread_info tsk
			mov	why, #0
			b	ret_to_user_from_irq  //1
			UNWIND(.fnend		)
			ENDPROC(__irq_usr)
		
		entry-common.S (\kernel\arch\arm\kernel)
		
			ENTRY(ret_to_user)
			ret_slow_syscall:
				disable_irq				@ disable interrupts
			ENTRY(ret_to_user_from_irq)
				ldr	r1, [tsk, #TI_FLAGS]
				tst	r1, #_TIF_WORK_MASK
				bne	work_pending  //2.如果有work则调到出执行work_pending
			no_work_pending:
			#if defined(CONFIG_IRQSOFF_TRACER)
				asm_trace_hardirqs_on
			#endif
				/* perform architecture specific actions before user return */
				arch_ret_to_user r1, lr
			
				restore_user_regs fast = 0, offset = 0 //6 返回用户空间继续执行
			ENDPROC(ret_to_user_from_irq)
			ENDPROC(ret_to_user)
			
			fast_work_pending:
				str	r0, [sp, #S_R0+S_OFF]!		@ returned r0
			work_pending:
				tst	r1, #_TIF_NEED_RESCHED
				bne	work_resched  //3. 如果有进程等待被调度，那么执行schedule(), 从而发生用户抢占
				tst	r1, #_TIF_SIGPENDING|_TIF_NOTIFY_RESUME
				beq	no_work_pending  
				mov	r0, sp				@ 'regs'
				mov	r2, why				@ 'syscall'
				tst	r1, #_TIF_SIGPENDING		@ delivering a signal?
				movne	why, #0				@ prevent further restarts
				bl	do_notify_resume  //4 如果有信号要处理则处理signal
				b	ret_slow_syscall		@ Check work again //5 返回
			
			work_resched:
				bl	schedule  //发生进程切换
		
		2）从系统调用返回用户空间时
		
		见1）中的ret_slow_syscall处的流程。

- 内核抢占

		内核抢占指的是：进程在内核态（SVC模式下）是否允许内核在任何时间点抢占当前正在执行的进程（也就是抢占当前进程的CPU时间而去调度其他进程）。
		
		一般发生在以下情况：
		
		1）从中断处理程序返回内核空间时
		
		此时需要判断当前进程的preempt_count是否为0. 只有preempt_count为0时发生内核抢占才是安全的。
		因为preempt_count不为0，内核进程可能拥有锁。
		
		代码如下：
		entry-armv.S (\kernel\arch\arm\kernel)
			
			__irq_svc:  //svc模式下IRQ的入口
				svc_entry
				irq_handler  //处理irq
			#ifdef CONFIG_PREEMPT
				get_thread_info tsk  //获得当前task的thread_info到tsk
				ldr	r8, [tsk, #TI_PREEMPT]			  @ get preempt count
				ldr	r0, [tsk, #TI_FLAGS]		@ get flags
				teq	r8, #0				@ if preempt count != 0
				movne	r0, #0				@ force flags to 0
				tst	r0, #_TIF_NEED_RESCHED
				blne	svc_preempt //如果preempt_count大于0，那么即使有进程等待被调度，也不发生调度新进程（即不发生内核抢占），
										否则如果preempt_count==0且有进程等待被调度，那么发生内核抢占。
			#endif
			…
			svc_exit r5				@ return from exception
			
			
			#ifdef CONFIG_PREEMPT
			svc_preempt:
				mov	r8, lr
			1:	bl	preempt_schedule_irq		@ irq en/disable is done inside
				ldr	r0, [tsk, #TI_FLAGS]		@ get new tasks TI_FLAGS
				tst	r0, #_TIF_NEED_RESCHED
				moveq	pc, r8				@ go again //从调度后的新task上检测是否有其他task要被调度，如果没有，则返回
				b	1b  //如果有则重复svc_preempt()过程，即发生内核抢占
			#endif
		
			
			asmlinkage void __sched preempt_schedule_irq(void)
			{
				struct thread_info *ti = current_thread_info();
			
				/* Catch callers which need to be fixed */
				BUG_ON(ti->preempt_count || !irqs_disabled());
			
				do {
					add_preempt_count(PREEMPT_ACTIVE); //内核抢占已经开始
					local_irq_enable();
					__schedule(); //调度到新的task 去执行，执行完新task后返回。
					local_irq_disable();
					sub_preempt_count(PREEMPT_ACTIVE); //内核抢占结束
			
					/*
					 * Check again in case we missed a preemption opportunity
					 * between schedule and now.
					 */
					barrier();
				} while (need_resched()); //如果没有进程等待被调度，那么就返回
			}
		
		ARM tst 和bne连用: 先是用tst进行位与运算，然后将位与的结果与0比较，如果不为0，则跳到bne紧跟着的标记（如bne sleep，则跳到sleep处）。
		
		
		2）内核显示调用schedule()
			包括：
			内核中的任务因等待锁而阻塞，此时调用schedule()。
			内核显示地调用schedule()就允许发生内核抢占,无需额外的安全保障，因为内核此时知道自己是安全的。
