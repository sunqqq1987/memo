# Android 内存泄露 #

# 参考 #

	http://wetest.qq.com/lab/view/161.html 专项：Android 内存泄露实践分析
	http://wetest.qq.com/lab/view/107.html Android应用内存泄露分析、改善经验总结
	
	http://wetest.qq.com/lab/view/359.html?from=adsout_qqtips_past2_359&sessionUserType=BFT.PARAMS.249884.TASKID&ADUIN=409893904&ADSESSION=1515131011&ADTAG=CLIENT.QQ.5527_.0&ADPUBNO=26632
	我这样减少了26.5M Java内存！
	=>  快速Dump Android java heap脚本
	
	
- 内存泄漏

	- 常见的内存泄露问题

			1)单例（主要原因还是因为一般情况下单例都是全局的，有时候会引用一些实际生命周期比较短的变量，导致其无法释放）
			2)静态变量（同样也是因为生命周期比较长）
			3)Handler内存泄露
			4)匿名内部类（匿名内部类会引用外部类，导致无法释放，比如各种回调）
			5)资源使用完未关闭（BraodcastReceiver，ContentObserver，File，Cursor，Stream，Bitmap）

	- 解决办法
	
			1）开源工具leakcanary, 适用于app层
	
			其原理是监控每个activity，在activity ondestory后，在后台线程检测引用，然后过一段时间进行gc，
			gc后如果引用还在，那么dump出内存堆栈，并解析进行可视化显示。使用LeakCanary可以快速地检测出Android中的内存泄露。
		
			2）native层的泄漏，可以打开malloc的debug模式
			adb shell setprop libc.debug.malloc 1
			
# 泄漏情况 #

	1） 单实例持有activity的context
	 Activty是间接继承于Context的，当按back, Activity退出时，Activity应该被回收， 但是单例AppManager中又持有它的引用，导致Activity回收失败，造成内存泄漏。
	
	public class AppManager {

		private static AppManager mInstance;

		private Context mContext;

		private AppManager(Context context){
			this.mContext= context;

			//正确的方法：不管外面传入什么Context，最终都会使用Applicaton的Context，而我们单例的生命周期和应用的一样长，这样就防止了内存泄漏。
			//this.context=context.getApplicationContext();
		}

		public static AppManager getInstance(Context context){
			if (mInstance== null){
				mInstance= new AppManager(context); //构造函数时就保存了activity的引用
			}
			return mInstance;
		}
	}
	
	2）handler持有外部类的引用
	
	//测试Handler 引起的内存泄漏
	public class SecondActivity extends AppCompatActivity {

		@Override
		protected void onCreate(Bundle savedInstanceState) {
			super.onCreate(savedInstanceState);
			setContentView(R.layout.activity_second);

			Log.e("error", "xxl. onCreate");

			//参考：https://www.cnblogs.com/andashu/p/6440944.html
			// SecondActivity代码中有一个延迟10秒执行的消息Message，当按back ( 或在SecondActivit界面旋转后，或当Activity进入后台或者开启设置里面的不保留活动时），SecondActivity被销毁。
			// 但由于SecondActivity的Handler对象mHandler为非静态匿名内部类对象，它会自动持有外部类SecondActivity的引用，从而导致SecondActivity无法被回收，造成内存泄漏。
			// 解决办法：将Handler声明为静态内部类，就不会持有外部类SecondActivity的引用，其生命周期就和外部类无关，如果Handler里面需要context的话，可以通过弱引用方式引用外部类。
			mHandler.postDelayed(new Runnable() {
				@Override
				public void run() {
					// ...

					Message message = new Message();
					message.what = 1;

					Log.e("error", "xxl. message sent!");
					//Runnable Thread线程发出Handler消息，通知更新UI
					mHandler.sendMessage(message);
				}
			}, 10000);

		}

		//mHandler为非静态匿名内部类对象，它会持有外部类secondactivity的引用
		private final Handler mHandler= new Handler() {
			@Override
			public void handleMessage(Message msg){
				// ....

				switch (msg.what) {
					case 1:
						//update UI
						Log.e("error", "xxl. message handled!");
						break;
				}
				super.handleMessage(msg);
			}
		};

	}

	3）asynctask
	public class FifthActivity extends AppCompatActivity {

		@Override
		protected void onCreate(Bundle savedInstanceState) {
			super.onCreate(savedInstanceState);
			setContentView(R.layout.activity_fifth);

			// This async task is an anonymous class and therefore has a hidden reference to the outer
			// class MainActivity. If the activity gets destroyed before the task finishes (e.g. rotation),
			// the activity instance will leak.
			// 当按back后，asynctask还没有执行完（sleep了）而一直持有FifthActivity的引用，导致 FifthActivity  的内存无法被回收
			new AsyncTask<Void, Void, Void>() {
				@Override protected Void doInBackground(Void... params) {
					// Do some slow work in background
					SystemClock.sleep(10000);
					return null;
				}
			}.execute();
		}
	}
	
	4)
	
		public class SixthActivity extends AppCompatActivity {

		@Override
		protected void onCreate(Bundle savedInstanceState) {
			super.onCreate(savedInstanceState);
			setContentView(R.layout.activity_sixth);

			//按back返回后，SixthActivity存在内存泄漏，原因就是非静态内部类LeakThread持有外部类SixthActivity的引用，而SixthActivity中做了sleep操作，导致SixthActivity的内存无法被释放。
			LeakThread leakThread = new LeakThread();
			leakThread.start();
		}

		class LeakThread extends Thread {
			@Override
			public void run() {
				try {
					Thread.sleep(10 * 1000);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
			}
		}
	}

	
	5）
	
	public class ThirdActivity extends AppCompatActivity {

		//非静态的内部类InnerClass会自动持有外部类ThirdActivity的引用，创建的静态实例mInner就会一直持有ThirdActivity的引用，导致ThirdActivity需要销毁的时候没法正常销毁。
		private static InnerClass mInner= null;

		@Override
		protected void onCreate(Bundle savedInstanceState) {
			super.onCreate(savedInstanceState);
			setContentView(R.layout.activity_third);

			if (mInner== null) {
				mInner= new InnerClass();
			}
		}

		//非静态的内部类
		public class InnerClass{

		}
	}
	
	6) SecondActivity代码中有一个延迟10秒执行的消息Message，当按back ( 或在SecondActivit界面旋转后，或当Activity进入后台或者开启设置里面的不保留活动时），SecondActivity被销毁。
	   但由于SecondActivity的Handler对象mHandler为非静态匿名内部类对象，它会自动持有外部类SecondActivity的引用，从而导致SecondActivity无法被回收，造成内存泄漏。
	   解决办法：将Handler声明为静态内部类，就不会持有外部类SecondActivity的引用，其生命周期就和外部类无关，如果Handler里面需要context的话，可以通过弱引用方式引用外部类。
	
# leakcanary #

	最新的LeakCanary开源控件，可以很好的帮助我们发现内存泄露的情况

	github:
	https://github.com/square/leakcanary
	https://github.com/liaohuqiu/leakcanary-demo

# 使用Android Studio（3.0）的 Android Profiler工具 #

		run -> profile app 后选择指定的进程，就可以看到memory的占用情况
	
		我们可以很清晰的看到

		1）进程总内存占用： 180M
		2）JavaHeap： 48M
		3）NativeHeap：native层的 so 中调用malloc或new创建的内存 —— 28M
		4）Graphics：OpenGL和SurfaceFlinger相关内存 ——58M
		5）Stack：线程栈——1.89M
		6）Code：dex+so相关代码占用内存——37.75M
		7）Other

# 使用 MAT 工具 #

	参考： http://blog.csdn.net/u012760183/article/details/52068490
	
	Eclipse MAT工具下载地址
	https://www.eclipse.org/mat/
	
	1. 打开AS中的Android Device Monitor工具,标记要检测的应用的包名,在怀疑发生leak的activity后，手动做一次GC, 最后dump出hprof文件
	2. 直接在android studio中打开，用自带的工具分析leak
		或者用android sdk中提供给的工具 hprof-conv.exe 将Android导出的hprof转换为java程序的hprof文件，然后用MAT工具分析leak

		hprof-conv 源文件 输出文件

- Shallow Size

		对象自身占用的内存大小，不包括它引用的对象。
		针对非数组类型的对象，它的大小就是对象与它所有的成员变量大小的总和。当然这里面还会包括一些java语言特性的数据存储单元。
		针对数组类型的对象，它的大小是数组元素对象的大小总和。

- Retained Size

		Retained Size=当前对象大小+当前对象可直接或间接引用到的对象的大小总和。(间接引用的含义：A->B->C, C就是间接引用)
		换句话说，Retained Size就是当前对象被GC后，从Heap上总共能释放掉的内存。
		不过，释放的时候还要排除被GC Roots直接或间接引用的对象。他们暂时不会被被当做Garbage。
