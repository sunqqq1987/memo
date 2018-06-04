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
	