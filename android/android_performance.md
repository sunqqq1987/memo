# memory相关 #

- 资料

		【腾讯Bugly干货分享】Android内存优化总结&实践
		https://www.cnblogs.com/ldq2016/p/6635774.html

		https://blog.csdn.net/hnulwt/article/details/44900811

- Dalvik Heap

		Android Dalvik Heap与原生Java一样，将堆的内存空间分为三个区域：
		Young Generation，Old Generation， Permanent Generation
	
		最近分配的对象会存放在Young Generation区域，当这个对象在这个区域停留的时间达到一定程度，
		它会被移动到Old Generation，最后累积一定时间再移动到Permanent Generation区域。
		系统会根据内存中不同的内存数据类型分别执行不同的gc操作。

- 内存抖动

		Android里内存抖动是指内存频繁地分配和回收，而频繁的gc会导致卡顿，严重时还会导致OOM.

		内存抖动为什么会引起OOM呢？
		主要原因还是有因为大量小的对象频繁创建，导致内存碎片，从而当需要分配内存时，虽然总体上还是有剩余内存可分配，
		而由于这些内存不连续，导致无法分配，系统直接就返回OOM了。

	- 解决方法
	
			1）打Log而进行了字符串拼接，一旦这个函数被比较频繁地调用，那么就很有可能会发生内存抖动。
			改为使用stringbuilder进行优化。

- 内存优化方法

		可以通过各种内存泄露检测组件，MAT查看内存占用，Memory Monitor跟踪整个App的内存变化情况,
		Heap Viewer查看当前内存快照, Allocation Tracker追踪内存对象的来源,
		以及利用崩溃上报平台从多个方面对App内存进行监控和优化。

	- 图片分辨率适配: 使用缓存池
	- 图片压缩
	- ListView复用
	- 序列化数据使用protobuf可以比xml省30%内存，慎用shareprefercnce
	- dex优化，代码优化，谨慎使用外部库
		
		proguard是android自带的混淆器，会对java的类名，函数名，变量名等重新命名，给一个非常短的名字。
		有两个作用，一个是使得反编译的代码不容易理解，另一个就是减少了dex文件的大小。

	- 使用ArrayMap及SparseArray

			ArrayMap及SparseArray是android的系统API，是专门为移动设备而定制的。
			用于在一定情况下取代HashMap而达到节省内存的目的


- 突破OOM,绕过dalvikvm heapsize的限制的方法
	
		首先要明白，java程序发生OMM并不是表示RAM不足，如果RAM真的不足，这时Android的memory killer会起作用，
		memory killer会杀死一些优先级比较低的进程来释放物理内存，让高优先级程序得到更多的内存。

		为什么会OOM呢？其实就是申请的内存超过了Dalvik Heap的最大值
		
		1）使用分进程的方式突破每个进程的Dalvik Heap内存限制。
		创建子进程的方法：
			使用android:process标签, 从activity里将service在另一个进程中启动：
			在manifest.xml中的service节点中加入以下，
			android:process="com.example.admin.myapplication.MyService"

		2）使用jni在native heap上申请空间（推荐使用）
			nativeheap的增长并不受dalvik vm heapsize的限制

		3）使用显存（操作系统预留RAM的一部分作为显存）
			使用OpenGL textures等API，texture memory不受dalvik vm heapsize限制。
			再比如Android中的GraphicBufferAllocator申请的内存就是显存。

		4）app需要使用大内存

			<application 。。。
			android:largeHeap="true">

- 内存状态

	- 查看app占用的内存
	
			adb shell dumpsys meminfo [package-name/pid]
			例如：adb shell dumpsys meminfo com.example.admin.myapplication
	
	- adb shell procrank //查看进程的pss，rss等信息
	
			VSS- Virtual Set Size 虚拟耗用内存（包含共享库占用的内存）
			RSS- Resident Set Size 实际使用物理内存（包含共享库占用的内存）
			PSS- Proportional Set Size 实际使用的物理内存（比例分配共享库占用的内存）	
			USS- Unique Set Size 进程独自占用的物理内存（不包含共享库占用的内存）

			一般来说内存占用大小有如下规律：VSS >= RSS >= PSS >= USS

	- vm heapsize

			adb shell
			getprop | grep dalvik.vm.heapgrowthlimit

	- adb shell cat /proc/meminfo 查看系统RAM使用情况
	
			MemTotal：可以使用的RAM总和（小于实际RAM，操作系统预留了一部分）
			MemFree：未使用的RAM
			Cached：缓存（这个也是app可以申请到的内存）
			HightTotal：RAM中地址高于860M的物理内存总和，只能被用户空间的程序使用。
			HightFree：RAM中地址高于860M的未使用内存
			LowTotal：RAM中内核和用户空间程序都可以使用的内存总和（对于512M的RAM: lowTotal= MemTotal）
			LowFree: RAM中内核和用户空间程序未使用的内存

# Activity #

- 文件

	- ActivityRecord.java
	- ActivityStack.java


- Activity displayed延迟

	- 参考
			
			https://blog.csdn.net/q1183345443/article/details/62225092
	
	- log
	
			02-27 16:07:47.816929  2667  2733 I ActivityManager: Displayed com.android.settings/.SubSettings: +30s71ms
		
			=> 这个Activity的displayed延迟了30多秒
	
	- 分析
	
			原理：AMS启动Activity的时候，先会调用ActivityStackSupervisor的startSpecificActivityLocked方法，
			这个方法里面：如果进程没有启动，则先启动进程，否则去调用ActivityThrread的handleLaunchActivity()。
			在Activity的handleLaunchActivity中先后会调用Activity的onCreate和onResume函数，
			然后才是到WMS的addWindow创建窗口, 窗口创建了之后才会把所有与这个AppWindowToken的窗口置为一个准备显示的状态。
			这个时候就会去打印这个log，也会计算这个activity的要被显示时的延时。
			所以这中间应用的onCreate和onResume耗时的可能性比较大才会最终导致打印这个log。
	
			void startSpecificActivityLocked()
			{
				r.task.stack.setLaunchTime(r); //设置Launch time
			}
	
			reportLaunchTimeLocked函数会把当前的时间减去 Launchtime的时间（Activity启动到显示的时间差），然后打印displayed的延迟时间的log。
			这个时间差就是Activity的Launchtime时间到这个AppWindowToken下的所有窗口都到一个准备显示状态的时间差。
	
			private void reportLaunchTimeLocked(final long curTime) {  
				final long thisTime = curTime - displayStartTime;  //本次延时：当前时间-Launch time
				final long totalTime = stack.mLaunchStartTime != 0  

				StringBuilder sb = service.mStringBuilder;  
				sb.setLength(0);  
				sb.append("Displayed ");  
				sb.append(shortComponentName);  
				sb.append(": ");  
				TimeUtils.formatDuration(thisTime, sb);   // => 打印本次display activity的延时
				if (thisTime != totalTime) {  
					sb.append(" (total ");  // => 总的延时
					TimeUtils.formatDuration(totalTime, sb);  
					sb.append(")");  
				}  
				Log.i(TAG, sb.toString());  
				
			}
	
# systrace #

	参考
	https://blog.csdn.net/omnispace/article/details/77620667
	https://blog.csdn.net/neacy_zz/article/details/50404863
	https://www.jianshu.com/p/8c946102261c
	
	Android platform tool里提供的systrace.py是个python脚本，它通过执行“adb shell atrace ***”命令去读取内核的“/sys/kernel/debug/tracing/trace”节点来获取内核的跟踪信息，
	从而做出统计和分析，也就是说它本质上使用了内核的ftrace跟踪器。
	
	Android上内置的linux应用程序atrace会设置ftrace相应的选项并使能ftrace，这样内核里就保留ftrace信息，最后以统计信息形式dump出来。
	
	用来分析速度和流程性不够（如画面卡顿）性能问题。
	
	注意：
	1）User版本是不可以抓Trace的，只有ENG版本或者Userdebug版本才可以。
		
- 抓取方法
	
		1）android studio -> device monitor -> 点击android systrace图标，弹出配置选项后，进行抓取
		这种方式在windows上也可以抓取
		
		2) 命令行
		cd android-sdk/platform-tools/systrace   //进入到android studio的systrace目录
		python systrace.py --time=10 -o mynewtrace.html sched gfx view wm
		注意：貌似在windows上运行systrace会有错误
		
		使用python systrace.py -h来获得命令行帮助
		
		抓取结束后，会生成对应的Trace文件，然后用Chrome浏览器打开。
		
- 自定义systrace

	
- 分析systrace

		1）Frame
		
		每个应用都有一行专门显示frame，每一帧就显示为圆圈。
		正常绘制是1秒60帧，大约一帧16.6毫秒，在这个值以下是正常颜色绿色。
		如果超过它就会变成红色、黄色，非绿色的都说明有问题。当遇到红色的时候肯定当前的性能需要优化。
		这时需要通过’w’键放大那一帧，然后按‘m’键高亮，进一步分析问题。
		按's'是缩小
		
		2）Alerts
		
		Systrace能自动分析trace中的事件，并能自动高亮性能问题作为一个Alerts，建议调试人员下一步该怎么做。
		比如对于丢帧是，点击黄色或红色的Frames圆点便会有相关的提示信息；
		另外，在systrace的最右上方，有一个Alerts tab可以展开，这里记录着所有的的警告提示信息。
	
	
# traceview #

	参考
	https://blog.csdn.net/u011240877/article/details/54347396