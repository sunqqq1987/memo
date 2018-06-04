# 资源

- kernel源码交叉索引

		http://lxr.free-electrons.com

- 每个内核版本的具体变更

		http://kernelnewbies.org

- 如何提交patch

		参考
		https://blog.csdn.net/mirage1993/article/details/53957205  如何向 Linux 内核上游提交 Patch 
		https://blog.csdn.net/mirage1993/article/details/69056230  如何向 Linux Kernel 提交 Patch
		https://legacy.gitbook.com/book/0xax/linux-insides/details  linux-insides

# 系统睡眠 #

- 以下是进入sleep的关键入口
 
		lpm_cpuidle_enter(,fromidle)或 lpm_suspend_enter(,fromidle)  
		 ->lpm_enter_low_power()  
			->lpm_cpu_prepare(system_state, cpu_index, from_idle);  
			->lpm_system_prepare(system_state, idx, from_idle);  
				->msm_rpm_enter_sleep()   
					->smd_mask_receive_interrupt() //屏蔽RPM发给AP的中断	  
				->msm_mpm_enter_sleep() //进入sleep前配置MPM  
			->msm_cpu_pm_enter_sleep(cpu_level->mode, from_idle);  
				->execute[mode](from_idle); //调用 msm_pm_power_collapse()等  
			->lpm_system_unprepare(system_state, cpu_index, from_idle);  
				->msm_rpm_exit_sleep();  //不屏蔽RPM发给AP的中断  
				->msm_mpm_exit_sleep(from_idle); //退出SLEEP时  
			->lpm_cpu_unprepare(system_state, cpu_index, from_idle);   
	  
- 1) lpm_suspend_enter()被调用的过程

	文件:main.c, suspend.c
	  
	被定义在 lpm_suspend_ops 里:
 
		static const struct platform_suspend_ops lpm_suspend_ops =   
		{  
			enter = lpm_suspend_enter,  //<=
			valid = suspend_valid_only_mem,  
			prepare_late = lpm_suspend_prepare,  
			wake = lpm_suspend_wake  
		}  
		  
		suspend_set_ops(&lpm_suspend_ops) //Set the global suspend method table:suspend_ops  
   
	貌似以下2种情况是由app主动写文件节点而设置睡眠的  

		 autosleep_store()->...->try_to_suspend()  //配置了CONFIG_PM_AUTOSLEEP
		
		 或 state_store	
		
			 ->pm_suspend()   //suspend.c
			   ->enter_state() //Do common work needed to enter system sleep state  
				   ->suspend_prepare()
					  ->pm_notifier_call_chain(PM_SUSPEND_PREPARE)
						 ->msm_cpufreq_suspend() //设置Qcom-freq suspend_data=1, 这会阻止msm_cpufeq_target()去set_cpu_freq().
				   ->suspend_devices_and_enter()
					 ->dpm_suspend_start(PMSG_SUSPEND) //Prepare devices for PM transition and suspend them
					  ->dpm_prepare(PMSG_SUSPEND) //遍历 dpm_list 中的device, 执行完device_prepare()后将device 放到 dpm_prepared_list 中。
													device_add()->device_pm_add()会将所有的device加到dpm_list中.
					   ->dpm_suspend(PMSG_SUSPEND) //遍历 dpm_prepared_list 中的device, 执行完device的suspend函数后，将其放到 dpm_suspended_list 中
						 ->cpufreq_supend() //suspend cpufreq governors(linux 3.10)
						 ->device_suspend() //<= 执行各device的suspend callback
					
					  //方式一：将async_suspend放到system_unbound_wq worker线程里，等待被该worker调用，即异步方式执行suspend的callback.
					  //方式二：立即执行__device_suspend(dev, pm_transition, false)->执行struct dev_pm_ops.suspend函数
					  ->suspend_enter() //系统核心级的suspend
						   ->suspend_ops->prepare_late()
						   ->dpm_suspend_end(PMSG_SUSPEND)
							   ->dpm_suspend_late()//执行device 的 (struct dev_pm_ops->suspend_late函数)
							   ->dpm_suspend_noirq()  //执行dpm_late_early_list上的device 的callback(struct dev_pm_ops->suspend_noirq函数), 期间不会收到IRQ.
								  ->suspend_device_irqs() //<= disable all currently enabled irq line, and make sure all the irq thread are finished.
									  ->synchronize_irq() //<= 等待irq thread完成
								  ->device_suspend_noirq() //执行device的suspend_noirq()函数
								  ->pm_wakeup_pending() //如果有wakeup事件，那么会退出,并调用print_active_wakeup_source()打印出wakeup source
						   ->disable_nonboot_cpus()   //打印disalbing cpu的log
						   ->arch_suspend_disable_irqs()  
						   ->syscore_suspend() //<= Execute all the registered system core suspend   
												callbacks in syscore_ops_list,like GPIO,timer, sched_clock, GIC, VIC, cupfreq   
						   ->if(!error) //如果syscore suspend成功，那么进入low power mode  
							 {  
								if not pm_wakeup_pending()   //<= 如果没有唤醒中断
									->suspend_ops->enter(state) //<= 执行lpm_suspend_enter(,fromidle=false) 开始进入low power  
								syscore_resume() //<= 唤醒后执行系统核心的resume函数
							 }
							->arch_suspend_enable_irqs()
							->enable_nonboot_cpus()  //bootup每个cpu并打印enable cpu log
							->suspend_ops->wake()  
						->dpm_resume_start(PMSG_RESUME) //执行pre resume
		
				  ->dpm_resume_end(PMSG_RESUME) //
					   ->dpm_resume(state) //将dpm_suspended_list中的device放到 dpm_prepared_list
						 ->starttime= ktime_get()
						 ->device_resume() //<= 执行各device的resume函数
						 ->dpm_show_time(starttime,state,null) //打印device resume的消耗的总时间
						 ->cpufreq_resume() //resume cpufreq governors
					   ->dpm_complete(state) //将dpm_prepared_list的device放到dpm_list
		   
				->suspend_finish()
				  ->suspend_thaw_process()
					->thaw_process() //<= 唤醒所有的task并打印restarting task log,调用schedule()后打印’done’
				  ->pm_notifier_call_chain(PM_POST_SUSPEND)
					->msm_cpufreq_resume() //设置Qcom-freq suspend_data=0
			  
- 2) lpm_cpuidle_enter()被调用的过程  
   
	从以下可以看出，这是因CPU没有任务运行，所以主动进入sleep.
 
		 start_kernel()  
		 ->rest_init()  
			->cpu_idle()  
			{  
			   while (1)   
			   {  
					while (!need_resched())   
					{  
					  
						if (!need_resched())   
						{  
							cpuidle_idle_call() //通过cpuidle_get_driver获取cpuidle_curr_driver变量  
							->cpuidle_enter_state()  
								->cpuidle_enter_ops()  //被赋予：cpuidle_enter()  
								  ->target_state->enter()  //被赋予：lpm_cpuidle_enter(,fromidle=true).	
								  //在lpm_cpuidle_init()里，msm_cpuidle_driver 通过cpuidle_register()函数被注册到cpuidle_curr_driver变量  
									
						}  
					}  
			   }  
			}

- 如何让Linux进入休眠

		echo  mem > /sys/power/state  //使系统进行睡眠
		echo  on > /sys/power/state	 //使系统从睡眠中唤醒过来
		
		
# cmpxchg #

	cmpxchg(void* ptr, int old, int new)
	将old和ptr指向的内容比较，如果相等，则将new写入到ptr中，返回old;
	如果不相等，则返回ptr指向的内容。 整个操作是原子的。

	http://blog.csdn.net/penngrove/article/details/44175387

# DMA #

- 文件

		dma-contiguous.c
		Dma-mapping.h (\kernel\arch\arm\include\asm)

- 接口

		cma_create_area()
		bitmap_set()
		
		dma_alloc_from_contiguous()
		#define dma_alloc_coherent(d, s, h, f) dma_alloc_attrs(d, s, h, f, NULL)
		static inline void *dma_alloc_attrs()
		
		static struct cma_area {
			phys_addr_t base;  //物理基地址
			unsigned long size; //该区域的大小(bytes)
			struct cma *cma;  //-->该区域具体的信息
			const char *name;  //区域的名称
			bool to_system;
		} cma_areas[MAX_CMA_AREAS];  //cma区域的全局变量
		
		struct cma {
			unsigned long	base_pfn; //物理叶匡号
			unsigned long	count;   //所占的page 数
			unsigned long	*bitmap; //标记这些page是否使用，1为已经使用。用1个bit来标示1个page是否使用，所以bitmap的size=count/8 个字节
			bool in_system;
			struct mutex lock;
		};

		宏：CONFIG_DEBUG_CMA_TRACE

		cma_areas[0]是default 的 cma area

- LOG

		查cma的分配情况，搜索：”cma monitering:“
		
		cma monitering: arm_dma_alloc:78b9000.i2c 512/from 1[swapper/0]
		===>指模块78b9000.i2c去申请cma内存，当前线程pid=1, 线程名：swapper/0
		
		<6>[   47.706612]  [0:	  swapper/0:	1] cma: dma_alloc_from_contiguous(cma e6eb3180, count 1, align 0)
		==>e6eb3180来自cma_areas[0].cma= 0xE6EB3180, count 1指一个page