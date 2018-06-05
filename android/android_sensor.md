# android sensor #

	参考 
	http://www.cnblogs.com/lcw/p/3402770.html

- 框架


	app:    APK（用来接收Sensor返回的数据，并处理实现对应的UI效果，如屏幕旋转，打电话时灭屏，自动调接背光）
	
	-----------------------------------------------------------
	
	framework: sensorManager.java (是sensorService的client)
	JNI: android_hardware_sensorManager.cpp(定义JNI接口）
	
	-----------------------------------------------------------
	HAL: sensorManager.cpp(客户端，负责与服务端SensorService.cpp的通信)
		 sensorDevice.cpp(与具体的sensor对象通信）   
		 具体的sensor对象(sensor.h的实现）
		 
	Native: sensorService.cpp(服务端, 它打开HAL层的所有sensor设备，并通过HAL来poll底层的event事件。 由systemServer启动） 
	
# proximity sensor 近距离传感器 #

    一般会有以下几个关键部件：
    1）一个红外LED
    2) 一个给主机的中断PIN
    3) 通过SDA/SCL挂接到主机的I2C总线上
    
    
# 陀螺仪 #

	1.手机陀螺仪是有活动部件的
	2.硅陀螺会让一个细微的机械结构使用静电力驱动起来。
	3.振动起来后，如果发生旋转，会因为柯氏力在正交方向上产生位移，产生电容变化。这个位移与转动角速度成正比。
	4.检测这个电容变化，转换成数字信号，经过dsp，就可以给ap处理了。

#  sensor HAL #

	关键字： HAL_MODULE_INFO_SYM
	
	/android/hardware/libhardware/include/hardware/sensors.h
	/android/..,hardware/libsensors/libsensors/SensorHAL.cpp  //HAL层的总入口: 会初始化具体的sensor
	
	1）具体的sensor: AccelerometerSensor
	
	/android/..,hardware/libsensors/libsensors/AccelerometerSensor.cpp  //具体的sensor: 会用到SensorBase.cpp，
	以及 /android/..,hardware/libsensors/libsensors/AccGyroMagSensor.cpp ，这才是具体实现的文件
	
	AccelerometerSensor::AccelerometerSensor()
	SensorBase(NULL, "accelerometer_sensor"),  //先调用基类的构造函数，然后才会调用AccelerometerSensor自己的构造函数
	mInputReader(36)
	
	构造函数
	class AccelerometerSensor : public SensorBase {
	protected:
	    InputEventReader mInputReader;
	    AccGyroMagSensor* agsensor = AccGyroMagSensor::getInstance();  //实际是AccGyroMagSensor对象
	...
	}
	
	该sensor对应的节点
	
	/sys/class/input/input0 # ls -l
	drwxr-xr-x 2 root root    0  10:02 capabilities
	-rw-r--r-- 1 root root 4096  10:02 enabled
	drwxr-xr-x 3 root root    0  10:02 event0
	drwxr-xr-x 2 root root    0  10:02 id
	-r--r--r-- 1 root root 4096  10:02 modalias
	-r--r--r-- 1 root root 4096  10:02 name
	-r--r--r-- 1 root root 4096  10:02 phys
	drwxr-xr-x 2 root root    0  10:02 power
	-r--r--r-- 1 root root 4096  10:02 properties
	lrwxrwxrwx 1 root root    0  10:02 subsystem -> ../../../../class/input
	-rw-r--r-- 1 root root 4096  10:02 uevent
	-r--r--r-- 1 root root 4096  10:02 uniq
	
	（1）readevent过程
	这个函数是上层轮询设备的桥梁。上层通过策略，在某段时间里主动读取input缓冲区，查看驱动报上来的值。 
	参考：https://www.cnblogs.com/yiru/archive/2013/02/01/2889503.html
	
	ssize_t n = mInputReader.fill(data_fd);  //fill会用系统调用read来读取data_fd这个文件的内容，将其放入input_event
	
	在while循环中，使用mInputReader.readEvent从input_event队列读值：
	while (count && mInputReader.readEvent(&event)) {
	    
	    先判断事件类型，若是坐标绝对值（type==EV_ABS），则通过刚刚提到的indexToValue将值保存在mPendingEvent.distance中；
	    若是报值结束标志（EV_SYN），则认为这次读值完成，给mPendingEvent盖时间戳，将上层传来取值的指针赋上数据，计数器count自减，numEventReceived自加。
	
	    mInputReader.next();  //在while循环的结尾，input_reader指向下一条事件。
	    return numEventReceived; //函数最后返回已读取的事件数目。
	}
	
	（2）poll_active
	用来控制上层是否接收来自底层的事件，本质上写sysfs的enable节点

	char buf_val[];
	int2a(buf_val,val,sizeof(buf_val))
	fd= open("/sys/class/input/input2/enable", O_WRONLY)
	write(fd,buf_val,sizeof(buf_val))  //调用driver的enable_store函数
	close(fd);
	

	3）sensorbase是具体sensor的基类，它的工作是 ：
	（1）打开/dev/input/eventX 设备，并保存FD
	（2）获取/sys/class/sensors/XX_sensor/name里的sensor chip 名称（不一定要保存）
	
	/android/..,hardware/libsensors/libsensors/SensorBase.cpp
	#define SENSOR_SYMBOLIC_LINK_PATH   "/sys/class/sensor_event/symlink/"
	#define SENSOR_CLASS_PATH   "/sys/class/sensors/"
	
	
	Input子系统会在/dev/input/路径下创建我们硬件输入设备的事件节点，
	一般情况下手机中这些节点是以eventXX来命名的，如event0，event1等.
	我们可以利用EVIOCGNAME来获取事件结点对应的设备名称(device name)，它是android中对于input事件处理数据的来源点。
	
	/dev/input/ # ls -l
	crw-rw---- 1 root input 13,  64  10:02 event0
	crw-rw---- 1 root input 13,  65  10:02 event1
	crw-rw---- 1 root input 13,  66  10:02 event2
	crw-rw---- 1 root input 13,  67  10:02 event3  //会对应到具体的device name
	crw-rw---- 1 root input 13,  68  10:02 event4
	crw-rw---- 1 root input 13,  69  10:02 event5
	
	参考：https://blog.csdn.net/wh_19910525/article/details/11803917
	上面链接中的openInput(const char* inputName)函数会返回/dev/input/eventX(对应inputNmae)的fd
	
	char name[80];
	if (ioctl(fd, EVIOCGNAME(sizeof(name) - 1), &name) < 1)  //返回fd对应的设备名
	    name[0] = '\0';
	
	
	/sys/class/sensors/accelerometer_sensor # ls -l
	-rw-rw-r-- 1 system radio 4096  10:02 calibration
	--w--w---- 1 system radio 4096  10:02 lowpassfilter
	-r--r--r-- 1 system radio 4096  10:02 name  //保存该sensor chip的名称
	drwxr-xr-x 2 root   root     0  10:02 power
	-r--r--r-- 1 system radio 4096  10:02 raw_data
	-rw-rw-r-- 1 system radio 4096  10:02 reactive_alert
	-r--r--r-- 1 system radio 4096  10:02 selftest
	lrwxrwxrwx 1 root   root     0  10:02 subsystem -> ../../../../class/sensors
	-rw-r--r-- 1 root   root  4096  10:02 uevent
	-r--r--r-- 1 system radio 4096  10:02 vendor