
# 一. reference类(抽象类） #

Reference本身是一个接口，表示一个引用，不能直接使用，有四个它的派生类供我们使用，它们分别是：SoftReference,WeakReference,PhantomReference，FinalizerReference.

Reference子类都具有如下特点：

	1.Reference子类 不能无参化直接创建，必须至少以强引用对象为构造参数，创建各自的子类对象；
	2.因为1中以强引用对象为构造参数创建对象，因此，使得原本强引用所指向的堆内存中的对象将不再只与强引用本身直接关联，
	与Reference的子类对象的引用也有一定联系。且此种联系将可能影响到对象的垃圾回收。

/android/libcore/ojluni/src/main/java/java/lang/ref/Reference.java

    public abstract class Reference<T> {
    
    volatile T referent; /* Treated specially by GC */  //====> referent是引用实例所引用的对象，也就是实际的强引用对象。
   	Reference类也被称为引用类，它的实例 Reference Instance就是引用实例. 
    								由于Reference是一个抽象类，它的实例只能是子类软(soft)引用,弱(weak)引用,
    								虚(phantom)引用中的某个.
                               
     该类提供了两个构造函数：
	149
	150    Reference(T referent) {
	151        this(referent, null);
	152    }
	153
	154    Reference(T referent, ReferenceQueue<? super T> queue) {  //带ReferenceQueue的构造函数
	155        this.referent = referent;
	156        this.queue = queue;  //====>
	157    }
	
	58    final ReferenceQueue<? super T> queue; //===> queue是当前引用实例（软引用,弱引用,虚引用中的一个）所注册的引用队列。
	                                                     一旦实际的强引用对象（referent）的可达性发生适当的变化（不再被引用）后，
														此引用实例将会被添加到queue中。
	
	74    Reference queueNext; //====> 只要当前引用加入到了queue后，queueNext指向queue中的下一个引用。
			如果当前引用被移出queue, queueNext指向ReferenceQueue.sQueueNextUnenqueued（标记作用，表示已经移出queue）
	75
	83    Reference<?> pendingNext;  //====> 被GC设置的、已经形成了循环链表的、但未加入到ReferenceQueue的引用list，
			这个list会被ReferenceQueueDaemon线程读取
	
	
	95    public T get() {  //====> 如果应用对象被清除，那么返回null
	96        return getReferent();
	97    }
	98
	99    private final native T getReferent();
	100
	108    public void clear() { //====> 清除引用对象
	109        this.referent = null;
	110    }
	       
	       定义队列操作（具体有ReferenceQueue来实现）
	124    public boolean isEnqueued() {
	125        // Contrary to what the documentation says, this method returns false
	126        // after this reference object has been removed from its queue
	127        // (b/26647823). ReferenceQueue.isEnqueued preserves this historically
	128        // incorrect behavior.
	129        return queue != null && queue.isEnqueued(this);
	130    }
	
	143    public boolean enqueue() {
	144       return queue != null && queue.enqueue(this);
	145    }


## # ReferenceQueuue # ##

/android/libcore/ojluni/src/main/java/java/lang/ref/ReferenceQueue.java

ReferenceQueue的作用就是JAVA GC与Reference引用对象之间的中间层，
我们可以在外部通过ReferenceQueue（rq.poll()方法）及时地根据所监听的对象的可达性状态变化而采取处理操作。

通过poll方法弹出队列头部存储的Reference．
通过remove方法可以将poll变成block的，即队列为空时remove方法可以将当前线程阻塞住，等到enqueue时通过notify再将block唤醒．
通过add方法将参数表示的Reference添加到unenqueued描述的一个队列中,并通过ReferenceQueue.class.notifyAll()唤醒被阻塞住的ReferenceQueueDaemon守护线程。


当对象的可达性发生改变的时候，GC收集器将引用对象加入到该referenceQueue


## # ReferenceQueueDaemon # ##

/android/libcore/libart/src/main/java/java/lang/Daemons.java

ReferenceQueueDaemon在应用启动后就开始工作，任务是从ReferenceQueue.unqueue中读出需要处理的Reference list（GC释放的内存的对象所对应的Reference 的list）,并将读出的Reference放入到构造其自身时传入的ReferenceQueue中。
虚拟机在每次GC完成后会调用ReferenceQueue.add方法将这次GC释放的内存的对象所对应的Reference添加到ReferenceQueue.unqueue中

ReferenceQueue是起到了一个监控对象生命周期的作用。即当对象被GC回收时，倘若为它创建了带ReferenceQueue的Reference，那么会将这个带ReferenceQueue的Reference加入到构造它时传入的ReferenceQueue中。
这样我们遍历这个ReferenceQueue就知道被监控的对象是否被GC回收了



## # FinalizerReference # ##

FinalizerReference主要是为了协助FinalizerDaemon守护线程完成对象的finalize工作而生的．

/android/libcore/luni/src/main/java/java/lang/ref/FinalizerReference.java

简单来说，FinalizerReference就是一个派生自Reference的类，内部实现了一个由head,prev,next维护的队列,还有一个自己定义的成员变量：static的ReferenceQueue对象queue。


在add方法中,构造了一个FinalizerReference对象（以要加入的对象和自身的queue为参数），并将它加入到他自身维护的一个head队列中．
根据前面对ReferenceQueue的说明，当这个被FinalizerReference引用的对象被GC释放其所占用的内存堆空间时，会把这个对象的FinalizerReference引用插入到这个queue中。
这个add方法同样是从虚拟机中反调回来的，当一个对象实现了finalize方法，虚拟机中能够检测到，并且反调这个add方法将实现了finalize方法的对象当做参数传出来。
即所有实现了finalize方法的对象的生命周期都被FinalizerReference的queue所监控着，当GC发生时queue中就会插入当前正准备释放内存的对象的FinalizerReference引用。
到这里能很清晰看出这个也是一个典型的围绕这个queue成员变量的生产者消费者模型，生产者已经找到，接下来看下哪里去消费这个queue呢？我们还是将目光转向Daemons.java


remove方法从其自身维护的队列中删除指定的Reference。
另外看到FinalizerReference的get方法返回的是zombie成员。这个成员是在虚拟机中从referent拷贝过来的。

    @Override public T get() {
    	return zombie;
    }


## # FinalizerDaemon # ##

FinalizerDaemon是Daemons.java中定义的另一个守护线程，FinalizerReference中定义的queue的消费者就是它。

 /android/libcore/libart/src/main/java/java/lang/Daemons.java

总结起来，FinalizerReference和FinalizerDaemon组合起来完成了在合适的时机去调用我们实现的finalize方法的工作:
虚拟机检测到有对象实现了finalize方法会调用FinalizerReference的add方法使得在GC的时候能将实现了finalize方法的对象的引用加入到FinalizerReference的queue成员中。
而FinalizerDaemon则从FinalizerReference的queue中取出跟踪的引用并调用被引用对象的finalize方法。 



# 二、强引用 #

常见形式如：A a = new A();等。强引用a本身存储在栈内存中，其存储指向内存中对象(new A())的地址。
一般情况下，当对内存中的对象不再有任何强引用指向它时，垃圾回收机器开始考虑可能要对此内存进行的垃圾回收。
如当进行编码：a = null，此时，刚刚在堆中分配地址并新建的对象没有其他的任何引用(引用a不指向它了），当系统进行垃圾回收时，堆内存将被垃圾回收。

对象和引用的区别

    Person person;
    person = new Person("张三");
    person = new Person("李四");

这里让person先指向了“张三”这个对象，然后又指向了“李四”这个对象。也就是说，Person person，这句话只是声明了一个Person类的引用，它可以指向任何Person类的实例


# 三、 SoftReference #

SoftReference表示一个对象的软引用
SoftReference所引用的对象在发生GC时，如果该对象只被这个SoftReference所引用，那么在内存使用情况已经比较紧张的情况下会释放其所占用的内存，若内存比较充实，则不会释放其所占用的内存．比较常用于一些Cache的实现．
其构造函数中允许传入一个ReferenceQueue．

    SoftReference.java
    public class SoftReference<T> extends Reference<T>

使用：
软引用的一般使用形式如下：

    A a = new A();
    SoftReference<A> srA = new SoftReference<A>(a);

通过对象的强引用为参数，创建了一个SoftReference对象，并使栈内存中的srA指向此对象。
此时，进行如下编码：a = null，对于原本a所指向的A对象的垃圾回收有什么影响呢？

	import java.lang.ref.SoftReference;
	public class ReferenceTest {
	
	public static void main(String[] args) {
	
	A a = new A();
	
	SoftReference<A> srA = new SoftReference<A>(a);
	
	a = null; //======>
	
	if (srA.get() == null) {
	System.out.println("a对象进入垃圾回收流程");
	} else {
	System.out.println("a对象尚未被回收" + srA.get());
	}
	
	// 垃圾回收
	System.gc();
	
	if (srA.get() == null) {
	System.out.println("a对象进入垃圾回收流程");
	} else {
	System.out.println("a对象尚未被回收" + srA.get());
	}
	
	}
	}
	
	class A {
	
	}
	##输出结果为：
	
	1 a对象尚未被回收A@4807ccf6
	2 a对象尚未被回收A@4807ccf6

    当 a = null后，堆内存中的A对象将不再有任何的强引用指向它，但此时尚存在srA引用的对象指向A对象。
    当第一次调用srA.get()方法返回此指示对象时，由于垃圾回收器很有可能尚未进行垃圾回收，此时get()是有结果的，这个很好理解。
    当程序执行System.gc();强制垃圾回收后，通过srA.get()，发现依然可以得到所指示的A对象，说明A对象并未被垃圾回收。
    那么，软引用所指示的对象什么时候才开始被垃圾回收呢？需要满足如下两个条件：
    1.当其指示的对象没有任何强引用对象指向它；
    2.当虚拟机内存不足时。

因此，SoftReference变相的延长了其指示对象占据堆内存的时间，直到虚拟机内存不足时垃圾回收器才回收此堆内存空间。



# 四、WeakReference #

WeakReference表示一个对象的弱引用，WeakReference所引用的强对象在发生GC时，如果该强对象只被这个WeakReference所引用，那么不管当前内存使用情况如何都会释放该强对象所占用的内存．
其构造函数中允许传入一个ReferenceQueue．

    WeakReference.java
    public class WeakReference<T> extends Reference<T>

弱引用的一般使用形式如下：

    A a = new A();
    WeakReference<A> wrA = new WeakReference<A>(a);

当没有任何强引用指向此对象时， 其垃圾回收又具有什么特性呢？

	import java.lang.ref.WeakReference;
	public class ReferenceTest {
	
	    public static void main(String[] args) {
	
	        A a = new A();
	
	        WeakReference<A> wrA = new WeakReference<A>(a);
	
	        a = null; //=========
	
	        if (wrA.get() == null) {
	            System.out.println("a对象进入垃圾回收流程");
	        } else {
	            System.out.println("a对象尚未被回收" + wrA.get());
	        }
	
	        // 垃圾回收
	        System.gc();
	
	        if (wrA.get() == null) {
	            System.out.println("a对象进入垃圾回收流程");
	        } else {
	            System.out.println("a对象尚未被回收" + wrA.get());
	        }
	
	    }
	
	}
	
	class A {
	
	}
	##输出结果为：
	a对象尚未被回收A@52e5376a
	a对象进入垃圾回收流程

因此，对弱引用特点总结为：
WeakReference不改变原有强引用对象的垃圾回收时机，一旦其指示的对象没有任何强引用对象时，此指示的对象即进入正常的垃圾回收流程。

其主要使用场景见于：当前已有强引用指向强引用对象，此时由于业务需要，需要增加对此对象的引用，同时又不希望改变此引用的垃圾回收时机，此时WeakReference正好符合需求，常见于一些与生命周期的场景中。

对于SoftReference和WeakReference，还有一个构造器参数为ReferenceQueue<T>，当SoftReference或WeakReference所指示的对象确实被垃圾回收后，其引用将被放置于ReferenceQueue中。
注意上文中，当SoftReference或WeakReference的get()方法返回null时，仅表明其指示的对象已经进入垃圾回收流程，但此时其指示的对象不一定已经被垃圾回收。
而只有确认指示的对象被垃圾回收后，其引用（SoftReference或WeakReference）才会被放置于ReferenceQueue中。

看以下例子：
	
	public class ReferenceTest {
	
	    public static void main(String[] args) {
	
	        A a = new A();
	
	        ReferenceQueue<A> rq = new ReferenceQueue<A>();
	        WeakReference<A> wrA = new WeakReference<A>(a, rq);
	
	        a = null;
	
	        if (wrA.get() == null) {
	            System.out.println("a对象进入垃圾回收流程");
	        } else {
	            System.out.println("a对象尚未被回收" + wrA.get());
	        }
	
	        System.out.println("rq item:" + rq.poll());
	
	        // 垃圾回收
	        System.gc();
	
	        if (wrA.get() == null) {
	            System.out.println("a对象进入垃圾回收流程");
	        } else {
	            System.out.println("a对象尚未被回收" + wrA.get());
	        }
	
	        /*
	        try {
	            Thread.sleep(1000);
	        } catch (InterruptedException e) {
	            e.printStackTrace();
	        }
	        */
	
	        System.out.println("rq item:" + rq.poll());
	
	    }
	}
	
	class A {
	
	    @Override
	    protected void finalize() throws Throwable {
	        super.finalize();
	        System.out.println("in A finalize");
	    }
	
	}
	
	##输出结果为：
	1 a对象尚未被回收A@302b2c81
	2 rq item:null
	3 a对象进入垃圾回收流程
	4 rq item:null
	5 in A finalize
	
	由此，验证了“仅进入垃圾回收流程的SoftReference或WeakReference引用尚未被加入到ReferenceQueue”。
	
	！！！如果将上面的sleep代码enable, 
	##输出结果为：
	1 a对象尚未被回收A@6276e1db
	2 rq item:null
	3 a对象进入垃圾回收流程
	4 in A finalize
	5 rq item:java.lang.ref.WeakReference@645064f

可见等待对象A被垃圾回收后，weakReference引用才进入它的ReferenceQueue.


# 五、PhantomReference 虚引用 #

PhantomReference表示一个虚引用， 说白了其无法引用一个对象，即对指示的对象的生命周期没有影响
    
    PhantomReference.java
    public class PhantomReference<T> extends Reference<T>
    
    62public T get() {
    63return null;
    64}

与SoftReference或WeakReference相比，PhantomReference主要差别体现在如下几点：

    1.PhantomReference只有一个构造函数PhantomReference(T referent, ReferenceQueue<? super T> q)，
	因此，PhantomReference使用必须结合ReferenceQueue；

    2.不管有无强引用指向PhantomReference的指示对象，PhantomReference的get()方法返回结果都是null。

与WeakReference相同，PhantomReference并不会改变其指示的对象的垃圾回收时机。
且可以总结出：
ReferenceQueue的作用主要是用于监听SoftReference/WeakReference/PhantomReference的指示对象是否已经被垃圾回收。


# 参考 #

    http://blog.csdn.net/KM_Cat/article/details/51607231
    大猫品Android[三][Reference深入浅出]
    
    https://www.cnblogs.com/lwbqqyumidi/p/4151833.html
    Java/Android引用类型及其使用分析

