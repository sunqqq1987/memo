# android OutOfMemoryError #

    log:

    07-03 20:42:34.094 10031  2011 32761 W zygote  : Throwing OutOfMemoryError "Failed to allocate a 38291456 byte allocation with 2097152 free bytes and 5MB until OOM, max allowed footprint 46567600, growth limit 50331648"
    07-03 20:42:34.128 10031  2011 32761 E AndroidRuntime: FATAL EXCEPTION: IntentService[SendBugReportService]
    07-03 20:42:34.128 10031  2011 32761 E AndroidRuntime: Process: com.google.XXX, PID: 2011
    07-03 20:42:34.128 10031  2011 32761 E AndroidRuntime: java.lang.OutOfMemoryError: Failed to allocate a 38291456 byte allocation with 2097152 free bytes and 5MB until OOM, max allowed footprint 46567600, growth limit 50331648

    1)对应的art code:

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

    4)检查是否触发kill app的动作，搜“kill”

    5)检查系统的可用内存
    

    