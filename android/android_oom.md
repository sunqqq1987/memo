# android OutOfMemoryError #

    log:

    07-03 20:42:33.680 10031  2011 32761 I zygote  : Starting a blocking GC Alloc
    07-03 20:42:33.815 10015  3029 32762 W DropBoxEntryAddedChimeraService: Could not connect to Google API Client, giving up...
    07-03 20:42:33.869 10031  2011 32761 I zygote  : Alloc concurrent copying GC freed 4(16KB) AllocSpace objects, 0(0B) LOS objects, 4% free, 42MB/44MB, paused 474us total 187.622ms
    07-03 20:42:33.869 10031  2011 32761 I zygote  : Forcing collection of SoftReferences for 36MB allocation
    07-03 20:42:33.869 10031  2011 32761 I zygote  : Starting a blocking GC Alloc
    07-03 20:42:34.094 10031  2011 32761 I zygote  : Alloc concurrent copying GC freed 5(16KB) AllocSpace objects, 0(0B) LOS objects, 4% free, 42MB/44MB, paused 469us total 223.669ms
    07-03 20:42:34.094 10031  2011 32761 W zygote  : Throwing OutOfMemoryError "Failed to allocate a 38291456 byte allocation with 2097152 free bytes and 5MB until OOM, max allowed footprint 46567600, growth limit 50331648"
    07-03 20:42:34.128 10031  2011 32761 E AndroidRuntime: FATAL EXCEPTION: IntentService[SendBugReportService]
    07-03 20:42:34.128 10031  2011 32761 E AndroidRuntime: Process: com.google.android.XXX, PID: 2011
    07-03 20:42:34.128 10031  2011 32761 E AndroidRuntime: java.lang.OutOfMemoryError: Failed to allocate a 38291456 byte allocation with 2097152 free bytes and 5MB until OOM, max allowed footprint 46567600, growth limit 50331648


    1)log的意思

    07-03 20:42:34.094 10031  2011 32761 W zygote  : Throwing OutOfMemoryError "Failed to allocate a 38291456 byte allocation with 2097152 free bytes and 5MB until OOM, max allowed footprint 46567600, growth limit 50331648"
    ==> pid(2011)的子线程tid(32761)试图分配 38291456 字节（36.5M）没有成功，所以抛出 OutOfMemoryError。
    原因是：进程2011已经申请了44M Heap, 且其中有42M被占用了，只有2M是可用的（从最后的GC LOG可以看出：4% free, 42MB/44MB），
    现在该进程尝试申请36.5M，但因系统允许该进程最多可以申请48M（growth limit 50331648，这个也匹配：[dalvik.vm.heapgrowthlimit]: [48m]），且进程 已经占用的42M+尝试申请的36.5M==86.5M > 48.5M, 
    显然超过heapgrowthlimit，因此抛出oom异常。

    也可以从"5MB until OOM"来理解： 在oom时，该进程运最大允许申请的heap是：48M-42M-512K(堆空间至少预留的，见[dalvik.vm.heapminfree]: [512k]) = 5.5M， 也就是5M左右。显然进程尝试申请36.5M会失败。

    另外，“max allowed footprint 46567600” = 44.4M，与“4% free, 42MB/44MB”匹配。

    对应的art源码:
    art/runtime/gc/heap.cc:1221:  oss << "Failed to allocate a " << byte_count << " byte allocation with " << total_bytes_free


    2)检查dalvick heapsize的设置：

    [dalvik.vm.heapgrowthlimit]: [48m]
    [dalvik.vm.heapmaxfree]: [2m]
    [dalvik.vm.heapminfree]: [512k]
    [dalvik.vm.heapsize]: [96m]
    [dalvik.vm.heapstartsize]: [5m]
    [dalvik.vm.heaptargetutilization]: [0.75]


    3)在OutOfMemoryError前一般会有GC的动作, 搜：GC freed

    07-03 20:42:33.210 10031  2011 32761 I zygote  : Alloc concurrent copying GC freed 249(7KB) AllocSpace objects, 0(0B) LOS objects, 4% free, 42MB/44MB, paused 1.564ms total 159.314ms
    07-03 20:42:33.210 10031  2011 32761 I zygote  : Forcing collection of SoftReferences for 36MB allocation


    4)检查是否有触发kill app的动作，搜“kill”


    5)检查系统的可用内存和进程数，安装了多少apk

    //整个系统的available memory
    ------ MEMORY INFO (/proc/meminfo) ------
    MemTotal:         929940 kB
    MemFree:           16264 kB
    MemAvailable:     288944 kB
    Buffers:            4552 kB
    Cached:           274988 kB
    ==> MemAvailable足够大，说明不是内存不够导致的
    
    ------ 0.005s was the duration of 'MEMORY INFO' ------
    ------ CPU INFO (top -b -n 1 -H -s 6 -o pid,tid,user,pr,ni,%cpu,s,virt,res,pcy,cmd,name) ------
    Tasks: 1300 total,   5 running,1292 sleeping,   0 stopped,   1 zombie
    Mem:    929940k total,   912028k used,    17912k free,    19688k buffers
    Swap:   262140k total,    73820k used,   188320k free,   453272k cached
    ==> buffers/caches已经最够大了

    //所有安装的apk情况
    Packages:
    Package [com.google.android.XXX] (8babd5b):
    userId=10031 //==>uid
    pkg=Package{1895210 com.google.android.XXX}
    codePath=/system/priv-app/ClockworkHomeGoogleLocalEdition
    resourcePath=/system/priv-app/ClockworkHomeGoogleLocalEdition
    legacyNativeLibraryDir=/system/priv-app/ClockworkHomeGoogleLocalEdition/lib
    primaryCpuAbi=armeabi-v7a
    secondaryCpuAbi=null
    versionCode=780726211 minSdk=25 targetSdk=25
    versionName=2.12.0.199273280.le //==>版本号
    splits=[base]
    apkSigningVersion=2
    applicationInfo=ApplicationInfo{c78cc6c com.google.android.XXX}
    flags=[ SYSTEM HAS_CODE ALLOW_CLEAR_USER_DATA ]
    privateFlags=[ PRIVILEGED HAS_DOMAIN_URLS PRIVATE_FLAG_ACTIVITIES_RESIZE_MODE_RESIZEABLE_VIA_SDK_VERSION ]
    dataDir=/data/user/0/com.google.android.XXX  //==>安装目录
    supportsScreens=[small, medium, large, xlarge, resizeable, anyDensity]
    usesLibraries:
      com.google.android.wearable
      clockwork-system
    usesLibraryFiles:
      /system/framework/com.google.android.wearable.jar
      /system/framework/clockwork-system.jar
    timeStamp=2009-01-01 08:00:00
    firstInstallTime=2009-01-01 08:00:00
    lastUpdateTime=2009-01-01 08:00:00 //=> 安装时间
    signatures=PackageSignatures{6d90109 [507d4f11]}
    installPermissionsFixed=true installStatus=1
    pkgFlags=[ SYSTEM HAS_CODE ALLOW_CLEAR_USER_DATA ]
    declared permissions:


    6)检查所有进程(包括apk和系统进程，内核进程)的memory, 看是否有pss占用超大的情况。
    如果有，那么可能是因为其他进程发生了memory leak。

    //所有进程的procrank中的USS
    ------ PROCRANK (/system/xbin/su root procrank) ------
    PID       Vss      Rss      Pss      Uss     Swap    PSwap    USwap    ZSwap  cmdline
    1025   929660K   72648K   40886K   36720K    9920K    4716K    4608K    1615K  system_server
    552   850004K   70844K   36303K   31280K    5304K     101K       0K      34K  com.google.android.XXX


    //apk的memory情况: 关注一般情况下的Heap Size大小（比如这里是4556KB）
    ------ DUMPSYS MEMINFO (/system/bin/dumpsys -t 90 meminfo -a) ------
    Applications Memory Usage (in Kilobytes):
    Uptime: 11991489 Realtime: 24094808

    ** MEMINFO in pid 552 [com.google.android.XXX] **
                    Pss      Pss   Shared  Private   Shared  Private     Swap     Heap     Heap     Heap
                    Total    Clean    Dirty    Dirty    Clean    Clean    Dirty     Size    Alloc     Free
                    ------   ------   ------   ------   ------   ------   ------   ------   ------   ------
    Native Heap     9318        0      368     9272       44       20        0    15872    10845     5026
    Dalvik Heap     3068        0      236     3064       12        0        0     4556     3417     1139
    Dalvik Other     1697        0       68     1696        0        0        0                           
            Stack      392        0        0      392        0        0        0                           
        Ashmem        2        0        4        0       12        0        0                           
        Gfx dev     2378        0      244     2256        0        0        0                           
        Other dev      122        0       68        4        0      116        0                           
        .so mmap     2738     1684      616      192     9000     1684     1804                           
        .jar mmap       88        0        0       88        0        0        0                           
        .apk mmap     1953     1472        0        0     1592     1472        0                           
        .ttf mmap      215      140        0        0      172      140        0                           
        .dex mmap    10010     8500        0        4     7104     8500        0                           
        .oat mmap     3354     1984        0        0     9708     1984       64                           
        .art mmap     1332      136      664      880     6988      136       92                           
    Other mmap     1404        0        8        4     1400      860        0                           
        Unknown      538        0       28      532       28        0      104                           
            TOTAL    38609    13916     2304    18384    36060    14912     5932    20428    14262     6165
    
    Dalvik Details
            .Heap     2700        0        0     2700        0        0        0                           
            .LOS      128        0        8      128        0        0      852                           
    .LinearAlloc      969        0       48      968        0        0        0                           
            .GC      176        0       16      176        0        0        0                           
        .JITCache      452        0        0      452        0        0        0                           
        .Zygote      156        0      228      152       12        0      556                           
    .NonMoving       84        0        0       84        0        0        0                           
    .IndirectRef      100        0        4      100        0        0        0                           
    
    App Summary
                        Pss(KB)
                            ------
            Java Heap:     4080
            Native Heap:     9272
                    Code:    14064
                Stack:      392
                Graphics:     2256
        Private Other:     3232
                System:     5313
    
                TOTAL:    38609      TOTAL SWAP (KB):     5932
    
    Objects
                Views:      179         ViewRootImpl:        1
            AppContexts:       10           Activities:        1
                Assets:        9        AssetManagers:        8
        Local Binders:      125        Proxy Binders:       69
        Parcel memory:       12         Parcel count:       51
        Death Recipients:        4      OpenSSL Sockets:        0
                WebViews:        0
    
    SQL
            MEMORY_USED:        0
    PAGECACHE_OVERFLOW:        0          MALLOC_SIZE:      117
 
    //其他信息
    07-03 18:56:42.743 10031  2011  2011 I am_on_stop_called: [0,com.google.android.clockwork.home2.activity.HomeActivity2,handleStopActivity]
    07-03 18:56:43.239  1000  1025  1039 I am_meminfo: [98275328,22351872,66469888,119189504,41852928]
    07-03 18:56:43.348  1000  1025  1039 I am_pss  : [1481,10040,com.google.android.inputmethod.pinyin,13256704,11833344,0]
    07-03 18:56:43.468  1000  1025  1039 I am_pss  : [24505,10058,com.moji.wear,20310016,17596416,0]
    07-03 18:56:43.593  1000  1025  1039 I am_pss  : [1925,10056,com.mobvoi.wear.watchface.aw,15703040,13721600,0]

    ------ CHECKIN MEMINFO (/system/bin/dumpsys -t 30 meminfo --checkin) ------
    time,12188831,24292150
    4,552,com.google.android.XXX,15872,4563,N/A,20435,10881,3423,N/A,14304,4990,1140,N/A,6130,93


    7）分析该apk是否有memory leak

    参考官方文档：http://android.xsoftlab.net/tools/debugging/debugging-memory.html

    简要来说是：按测试路径来观察apk占用的内存是否一直增长，如果是，有可能泄露
    方法：

    （1) 监测 dalvik heap中的 总heap size是否一直增加.
    Dalvik Heap     3068        0      236     3064       12        0        0     4556（总heap size)     3417     1139
    
    脚本：
    whie true; do
    adb shell dumpsys meminfo [package-name/pid] | grep "Dalvik Heap "
    sleep 5
    done

    （2）监测可能发生leak的进程的GC 情况
    07-03 20:42:33.210 10031  2011 32761 I zygote  : Alloc concurrent copying GC freed 249(7KB) AllocSpace objects, 0(0B) LOS objects, 4% free, 42MB/44MB, paused 1.564ms total 159.314ms

    脚本：
    adb logcat | grep "GC freed" | grep "被监测的pid：2011"



 