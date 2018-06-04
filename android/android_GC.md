
# ART的GC日志具体的格式 #


    I/art: <GC_Reason> <GC_Name> <Objects_freed>(<Size_freed>) AllocSpace Objects, 
	       <Large_objects_freed>(<Large_object_size_freed>) <Heap_stats> LOS objects, <Pause_time(s)>

## 引起GC原因 ##

ART的引起GC原因（GC_Reason）要比DVM多一些，有以下几种：

    Concurrent： 并发GC，不会使App的线程暂停，该GC是在后台线程运行的，并不会阻止内存分配。

    Alloc：当堆内存已满时，App尝试分配内存而引起的GC，这个GC会发生在正在分配内存的线程。

    Explicit：App显示的请求垃圾收集，例如调用System.gc()。与DVM一样，最佳做法是应该信任GC并避免显示的请求GC，
	显示的请求GC会阻止分配线程并不必要的浪费 CPU 周期。如果显式的请求GC导致其他线程被抢占，
	那么有可能会导致 jank（App同一帧画了多次)。

    NativeAlloc：Native内存分配时，比如为Bitmaps或者RenderScript分配对象， 这会导致Native内存压力，从而触发GC。

    CollectorTransition：由堆转换引起的回收，这是运行时切换GC而引起的。
	收集器转换包括将所有对象从空闲列表空间复制到碰撞指针空间（反之亦然）。
	当前，收集器转换仅在以下情况下出现：在内存较小的设备上，App将进程状态从可察觉的暂停状态变更为可察觉的非暂停状态（反之亦然）。

    HomogeneousSpaceCompact：齐性空间压缩是指空闲列表到压缩的空闲列表空间，通常发生在当App已经移动到可察觉的暂停进程状态。
	这样做的主要原因是减少了内存使用并对堆内存进行碎片整理。

    DisableMovingGc：不是真正的触发GC原因，发生并发堆压缩时，由于使用了 GetPrimitiveArrayCritical，收集会被阻塞。
	一般情况下，强烈建议不要使用 GetPrimitiveArrayCritical，因为它在移动收集器方面具有限制。

    HeapTrim：不是触发GC原因，但是请注意，收集会一直被阻塞，直到堆内存整理完毕。
    
    Background:
    

## 垃圾收集器名称 ##

GC_Name指的是垃圾收集器名称，有以下几种：

    Concurrent mark sweep (CMS)：CMS收集器是一种以获取最短收集暂停时间为目标收集器，采用了标记-清除算法（Mark-Sweep）实现。 
	它是完整的堆垃圾收集器，能释放除了Image Space之外的所有的空间。

    Concurrent partial mark sweep：部分完整的堆垃圾收集器，能释放除了Image Space和Zygote Spaces之外的所有空间。
	关于Image Space和Zygote Spaces可以查看Android内存优化（一）DVM和ART原理初探这篇文章。

    Concurrent sticky mark sweep：分代收集器，它只能释放自上次GC以来分配的对象。
	这个垃圾收集器比一个完整的或部分完整的垃圾收集器扫描的更频繁，因为它更快并且有更短的暂停时间。

    Marksweep + semispace：非并发的GC，复制GC用于堆转换以及齐性空间压缩（堆碎片整理）。
    
    MarkSweep类用来回收Zygote Space和Allocation Space的垃圾，PartialMarkSweep类用来回收Allocation Space的垃圾，
	StickyMarkSweep类用来回收上次GC以来在Allcation Space上分配的最终又没有被引用的垃圾。

其他信息

	Objects freed：本次GC从非Large Object Space中回收的对象的数量。
	Size_freed：本次GC从非Large Object Space中回收的字节数。
	Large objects freed： 本次GC从Large Object Space中回收的对象的数量。
	Large object size freed：本次GC从Large Object Space中回收的字节数。
	Heap stats：堆的空闲内存百分比 （已用内存）/（堆的总内存）。
	Pause times：暂停时间，暂停时间与在GC运行时修改的对象引用的数量成比例。
	目前，ART的CMS收集器仅有一次暂停，它出现GC的结尾附近。移动的垃圾收集器暂停时间会很长，会在大部分垃圾回收期间持续出现。

# 实例分析 #

    I/art : Explicit concurrent mark sweep GC freed 104710(7MB) AllocSpace objects, 
			21(416KB) LOS objects, 33% free, 25MB/38MB, paused 1.230ms total 67.216ms

	这个GC日志的含义为：引起GC原因是Explicit；垃圾收集器为CMS收集器；释放对象的数量为104710个，释放字节数为7MB；
	释放大对象的数量为21个，释放大对象字节数为416KB；堆的空闲内存百分比为33%，已用内存为25MB，堆的总内存为38MB；
	GC暂停时长为1.230ms，GC总时长为67.216ms。

