# Input子系统架构 #

		输入子系统由: 输入驱动层(input_driver),输入核心层(Input Core )，和事件处理层(Event Handler)三部分组成。
		输入事件(如鼠标移动、键盘按键按下、joystick的移动等)通过input driver -> Input core -> Event handler -> userspace 到达用户空间传给应用程序。
		架构图如下：TBD
		
		注意：keyboard.c不会在/dev/input下产生节点，而是作为ttyX终端（不包括串口终端）的输入。
		上图中cvdev.c现在不用了，改而使用evdev.c
		
		另外，根据目前的代码，Event handler应该叫做 input handler 更合适

- 变量

		input_dev_list  //保存所有的input_dev
		input_handler_list //保存所有的input_handler
	
- 接口

		1）input_register_handler()
		注册一个input handler 到input core.
		该过程会调用input_attach_handler()将input_dev_list 中的input_dev与当前的handler相关联（先match后connect）。

		int input_register_handler(struct input_handler *handler)
		{
			struct input_dev *dev;
			int error;

			error = mutex_lock_interruptible(&input_mutex);
			if (error)
				return error;

			INIT_LIST_HEAD(&handler->h_list);

			list_add_tail(&handler->node, &input_handler_list); //

			list_for_each_entry(dev, &input_dev_list, node)  //
				input_attach_handler(dev, handler); //

			input_wakeup_procfs_readers();

			mutex_unlock(&input_mutex);
			return 0;
		}
		EXPORT_SYMBOL(input_register_handler);
		
		static int input_attach_handler(struct input_dev *dev, struct input_handler *handler)
		{
			const struct input_device_id *id;
			int error;

			id = input_match_device(handler, dev); //
			if (!id)
				return -ENODEV;

			error = handler->connect(handler, dev, id); //
			if (error && error != -ENODEV)
				pr_err("failed to attach handler %s to device %s, error: %d\n",
					   handler->name, kobject_name(&dev->dev.kobj), error);

			return error;
		}

		2）input_register_device()
		注册一个input_dev到input core，并且添加该设备到内核。
		该过程会调用input_attach_handler()将input_handler_list 中的input_handler与当前的input_dev相关联。

		int input_register_device(struct input_dev *dev)
		{
			...
			error = device_add(&dev->dev); //
			if (error)
				goto err_free_vals;

			...
			
			list_add_tail(&dev->node, &input_dev_list); //

			list_for_each_entry(handler, &input_handler_list, node) //
				input_attach_handler(dev, handler); //

			...
		}


		3）input_event()
		Input device(driver)通过 input_event()上报EV_KEY、EV_REL、EV_ABS等事件给应用程序。
		input_event()调用Input_handle_event()，进而最终调用到与 input_dev关联的input_handler的event()函数去上报事件（见input handler部分）。
		
		void input_event(struct input_dev *dev,
		 unsigned int type, unsigned int code, int value)
		{
			unsigned long flags;

			if (is_event_supported(type, dev->evbit, EV_MAX)) {

				spin_lock_irqsave(&dev->event_lock, flags);
				input_handle_event(dev, type, code, value);  //
				spin_unlock_irqrestore(&dev->event_lock, flags);
			}
		}
		
		input_handle_event()
			->input_pass_values()
				-> input_to_handler()
		
		static unsigned int input_to_handler(struct input_handle *handle,
			struct input_value *vals, unsigned int count)
		{
			struct input_handler *handler = handle->handler;
			struct input_value *end = vals;
			struct input_value *v;

			...

			if (handler->events)
				handler->events(handle, vals, count);
			else if (handler->event)
				for (v = vals; v != vals + count; v++)
					handler->event(handle, v->type, v->code, v->value); //

			return count;
		}


# input handler #

	以evdev为例。 文件：evdev.c
	
	会生成 /dev/input/event0 ~ n 的设备节点 ？
	
	在evdev模块初始化时会调用input_register_handler()将 evdev_handler 注册到input core层。
	如之前所述，此过程会调用evdev_connect()。
	
	evdev_ids.driver_info = 1 表示所有的input_dev都会使用evdev_handler来处理事件。
	
	static const struct input_device_id evdev_ids[] = {
		{ .driver_info = 1 },	/* Matches all devices */
		{ },			/* Terminating zero entry */
	};

	MODULE_DEVICE_TABLE(input, evdev_ids);

	static struct input_handler evdev_handler = {
		.event		= evdev_event,  //
		.events		= evdev_events, //
		.connect	= evdev_connect, //
		.disconnect	= evdev_disconnect,
		.legacy_minors	= true,
		.minor		= EVDEV_MINOR_BASE,
		.name		= "evdev",  //
		.id_table	= evdev_ids,
	};

	1） evdev_connect()会往内核添加个字符设备，且其file_operation是evdev_fops:
	
	static int evdev_connect(struct input_handler *handler, struct input_dev *dev,
		 const struct input_device_id *id)
	{
		struct evdev *evdev;
		int minor;
		int dev_no;
		int error;

		...
		
		INIT_LIST_HEAD(&evdev->client_list); //
		spin_lock_init(&evdev->client_lock);
		mutex_init(&evdev->mutex);
		init_waitqueue_head(&evdev->wait);
		evdev->exist = true;

		dev_no = minor;
		/* Normalize device number if it falls into legacy range */
		if (dev_no < EVDEV_MINOR_BASE + EVDEV_MINORS)
			dev_no -= EVDEV_MINOR_BASE;
		dev_set_name(&evdev->dev, "event%d", dev_no);  //

		evdev->handle.dev = input_get_device(dev);
		evdev->handle.name = dev_name(&evdev->dev);
		evdev->handle.handler = handler;  //
		evdev->handle.private = evdev;

		evdev->dev.devt = MKDEV(INPUT_MAJOR, minor);
		evdev->dev.class = &input_class;  //
		evdev->dev.parent = &dev->dev;
		evdev->dev.release = evdev_free;
		device_initialize(&evdev->dev);

		error = input_register_handle(&evdev->handle);  //
		if (error)
			goto err_free_evdev;

		cdev_init(&evdev->cdev, &evdev_fops);  // ==>
		evdev->cdev.kobj.parent = &evdev->dev.kobj;
		error = cdev_add(&evdev->cdev, evdev->dev.devt, 1);  //
		if (error)
			goto err_unregister_handle;

		error = device_add(&evdev->dev);  //
		if (error)
			goto err_cleanup_evdev;

		return 0;
	}

	这类文件的操作方法定义在evdev_fops变量中:
	
	static const struct file_operations evdev_fops = {
		.owner		= THIS_MODULE,
		.read		= evdev_read,  //
		.write		= evdev_write, //
		.poll		= evdev_poll,  //
		.open		= evdev_open,  //
		.release	= evdev_release,
		.unlocked_ioctl	= evdev_ioctl,
	#ifdef CONFIG_COMPAT
		.compat_ioctl	= evdev_ioctl_compat,
	#endif
		.fasync		= evdev_fasync,  //
		.flush		= evdev_flush,
		.llseek		= no_llseek,
	};

	(1)当应用程序打开evdev的文件节点时会调用evdev_open函数，它会为当前应用程序建立一个client,
	将client添加到evdev->client_list中，然后调用具体input_dev的open函数（见input driver部分）：
	evdev_open()
	-> evdev_attach_client() //为当前应用程序建立一个client, 将client添加到evdev->client_list中
		-> dev->open()

	(2)应用程序通过读取文件节点的方式去调用evdev_fops的evdev_read函数来读取event。
	具体过程是：evdev_read调用input_event_to_user()将event copy to user buffer.
	
	static ssize_t evdev_read(struct file *file, char __user *buffer,
		  size_t count, loff_t *ppos)
	{
		struct evdev_client *client = file->private_data;
		struct evdev *evdev = client->evdev;
		struct input_event event;
		size_t read = 0;
		int error;

		...

		for (;;) {
			
			...

			while (read + input_event_size() <= count &&
				   evdev_fetch_next_event(client, &event)) { //

				if (input_event_to_user(buffer + read, &event)) //
					return -EFAULT;

				read += input_event_size();
			}

			if (read)
				break;
			...
		}

		return read;
	}


	2） evdev_event() // 通过异步通知的方式(kill_fasync)，将所有的event传递给所有的client.
			->evdev_events(handle, vals, 1);
				->evdev_pass_values(client, vals, count, time_mono, time_real)
					->__pass_event(client, &event);
						->client->buffer[client->head++] = *event; //将事件保存到client的buffer中
						->kill_fasync(&client->fasync, SIGIO, POLL_IN); //必要时，告知应用程序client去读取该事件
		   
# input driver #

	具体的input driver会:
	1) input_allocate_device() //驱动获得一个input_dev
	2）设置input_dev的相关参数，如open方法
	3) 调用input_register_device() //将驱动具体的input dev注册到input core

	以gpio_keys 驱动为例：(gpio_keys.c)
	gpio_keys_probe()->gpio_keys_setup_key()中会初始化处理key的isr。
	当有按键中断到来时，ISR调度 worker 线程执行对应的work函数gpio_keys_gpio_work_func(),
	该函数最终调用 input_event() 和 input_sync()去执行evdev的event handler的相应event方法。
	
	static void gpio_keys_gpio_report_event(struct gpio_button_data *bdata)
	{
		const struct gpio_keys_button *button = bdata->button;
		struct input_dev *input = bdata->input;
		unsigned int type = button->type ?: EV_KEY;
		int state = gpio_get_value_cansleep(button->gpio);

		if (state < 0) {
			dev_err(input->dev.parent, "failed to get gpio state\n");
			return;
		}

		state = (state ? 1 : 0) ^ button->active_low;  //
		if (type == EV_ABS) {
			if (state)
				input_event(input, type, button->code, button->value); //
		} else {
			input_event(input, type, button->code, !!state); //
		}
		input_sync(input); //
	}


# android层事件处理 #

	架构图如下：TBD
	
	
- InputManager

		InputManager是系统事件处理的核心。
		InputManager使用两个线程：
		1）InputReaderThread叫做"InputReader"线程，它从EventHub中读取kernel的input事件，
		并预处理RawEvent，applies policy并且把消息送入InputDispatcherThead管理的队列中。
		2）InputDispatcherThread叫做"InputDispatcher"线程，它在队列上等待新的输入事件，并且异步地把这些事件分发给应用程序。
		
		InputManager创建时，就会创建EventHub实例。
	
- InputReader读取事件的流程

		Thread::_threadLoop->
			InputReaderThread::threadLoop->
				InputReader::loopOnce
					->EventHub::getEvents()
			->processEventsLocked()
		   
		如果是input_event的类型为EV_KEY，则需要调用device->keyMap.keyLayoutMap->mapKey函数把iput_event.code映射为RawEvent.keyCode.
		
		key mapping: TBD
	
- EventHub

		EventHub 是系统中所有事件的中央处理站，通过getEvents函数，给系统提供一个输入事件流。
		具体是：
		1）初始化EventHub实例时，就从/dev/input目录下查找所有设备，并进行打开（调用kernel态中evdev_open函数），获取其相关属性，最后加入mDevices列表中
		2）调用epoll_wait(mEpollFd, mPendingEventItems, EPOLL_MAX_EVENTS, timeoutMillis)，等待有事件发生
		3）从device->fd中读取input_event事件：
		read(device->fd, readBuffer, sizeof(struct input_event) * capacity)
	

- LOG

		< 6>[25923.602439] [0: InputReader: 3774] logger: !@interceptKeyBeforeQueueing(172), action=0 // Home key down
		< 6>[25923.633731] [0: InputReader: 3774] logger: !@handleInterceptActions(172), action=0, wmActions=0
		< 6>[25923.634064] [0: InputReader: 3774] logger: !@interceptKeyBeforeQueueing(172), action=1 // Home key up

		//正常inputdispatcher派发touch event的log：
		[53742.976516][2: InputDispatcher] 06-04 19:36:21.251  2802  3578 I  InputDispatcher Delivering touch to (5075): x: 59.000, y: 470.000, flags=0x0, action: 0x4, channel '4f1334c StatusBar (server)', toolType: 0
		
		//以下log是检测到inputdispatcher被阻塞，在此时间点前的log会打出Signal Catcher的log
		[71367.177967][1: InputDispatcher] 06-05 00:30:05.451  2802  3578 D  InputDispatcher Waiting for application to become ready for input: Window{2455357e u0 d0 com.android.contacts/com.android.dialer.DialtactsActivity}.  
		Reason: Waiting to send non-key event because the touched window has not finished processing certain input events that were delivered to it over 500.0ms ago.  
		Wait queue length: 10.  Wait queue head age: 17624436.0ms.