android wakelock

参考：　https://www.2cto.com/kf/201805/744099.html

如何确定阻止进入suspend的原因

系统没有进入suspend，主要的原因是因为系统有锁导致.

锁一般分为：APP透过PowerManager拿锁，以及kernel wakelock.
1分析上层持锁的问题：

目前PowerManagerService的log 默认不会打开，可以通过修改：

/frameworks/base/services/core/java/com/android/server/power/PowerManagerService.java

    private static final boolean DEBUG = true;
    private static final boolean DEBUG_SPEW = DEBUG && false;
修改为:
    private static final boolean DEBUG = true;
    private static final boolean DEBUG_SPEW = true;
打开上层的log

通过syslog：搜索关键字：total_time=来确定持锁的时间.

PowerManagerService: releaseWakeLockInternal: lock=31602562 [*job*/DownloadManager:com.android.providers.downloads], flags=0x0, total_time=600051ms

或者通过正则表达式：total_time=[\d]{4,}ms 过滤出持锁时间比较长的锁.

PowerManagerService: releaseWakeLockInternal: lock=31602562 [*job*/DownloadManager:com.android.providers.downloads], flags=0x0, total_time=600051ms
PowerManagerService: releaseWakeLockInternal: lock=56317918 [*job*/DownloadManager:com.android.providers.downloads], flags=0x0, total_time=283062ms
PowerManagerService: releaseWakeLockInternal: lock=216012597 [AudioMix], flags=0x0, total_time=120003ms
PowerManagerService: releaseWakeLockInternal: lock=41036921 [AudioMix], flags=0x0, total_time=167984ms
PowerManagerService: releaseWakeLockInternal: lock=70859243 [GsmInboundSmsHandler], flags=0x0, total_time=3206ms
PowerManagerService: releaseWakeLockInternal: lock=242046348 [AudioMix], flags=0x0, total_time=122205ms

2 kernel的锁

kernel 锁默认不会打印出来，一般是待机结束后通过节点来获取：

adb shell? cat /sys/kernel/debug/wakeup_sources >? wakeup_sources.log

active_count:对应wakeup source被激活的次数.
event_count:被信号唤醒的次数?
wakeup_count:中止suspend的次数.?
expire_count:对应wakeup source超时的次数.?
active_since:上一次还活跃的时间点.时间单位跟kernel log前缀时间是一样(kernel单调递增时间).?
total_time:对应wakeup source活跃的总时长.?
max_time:对应的wakeup source持续活跃最长的一次时间.?
last_change:上一次wakeup source变化的时间(从持锁到释放or释放到持锁)，时间单位跟kernel log前缀时间是一样(kernel单调递增时间).?
prevent_suspend_time:对应wakeup source阻止进入autosleep的总累加时间.

一般情况下:
如果是复现机，前面没有捉log，也没有dump log，只有一份wakeup_sources.log
可以看下prevent_suspend_time，一般时间越大越可能是阻止系统进入suspend的wakeup sources.

如果测试前后，都有捉 wakeup_sources.log 请对两份wakeup_sources.log的total time的差值.
差值时间跟灭屏的时间对得上，一般就是这个锁引起的问题.

把捉出来的wakeup_sources.log复制到excel表格中，比较好对齐，一个是比较好计算.

其中dispsys_wakelock total_time的时间有697614mS 也就是总共有697s.

或者在待机测试结束后通过命令：

adb bugreport > bugreport.txt

搜索关键：

底层的锁：
All kernel wake locks:?
Kernel Wake lock ttyC0 : 1h 33m 15s 668ms (3856 times) realtime?
Kernel Wake lock radio-interface: 1h 20m 56s 210ms (3995 times) realtime?
Kernel Wake lock ccci3_at : 1h 9m 43s 491ms (2932 times) realtime?
Kernel Wake lock ccci_fs : 1h 0m 52s 818ms (3432 times) realtime?
Kernel Wake lock ccci3_at2 : 41m 16s 938ms (2465 times) realtime

上层的锁：
All partial wake locks:?
Wake lock 1001 RILJ: 5m 29s 768ms (13118 times) realtime?
Wake lock 1000 *alarm*: 4m 7s 823ms (2330 times) realtime?
Wake lock 1000 ConnectivityService: 59s 513ms (1 times) realtime?
Wake lock u0a111 *alarm*: 50s 334ms (751 times) realtime?
Wake lock u0a111 WakerLock:999603354: 28s 655ms (125 times) realtime?
Wake lock 1000 NetworkStats: 11s 434ms (569 times) realtime