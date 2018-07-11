
# TRACE32 #

    iso下载：
    http://www.trace32.com/wiki/index.php/TRACE32_Update

    user guide:
    http://www.trace32.com/wiki/index.php/TRACE32_Main#iTSP_User.27s_Guide

- cmm语法

        # 查看类型
        y.b.type

        # 64bit 查看kernel页表( 也是init进程的）
        mmu.dump pagetable 0xFFFFFFC000000000
        
        # 如果要查看出问题时刻当前进程的页表,需要切换到对应的cpu context后再mmu.dump pt <地址>
        其他情况只能手动walk对应进程的pagetable
        
        # 64bit查看某个地址处的符号	
        d.v %y.q 地址
        
        # 获取某个成员变量的虚拟地址
        v.address
        
        &kcache_total_objects=V.ADDRESS(((struct kmem_cache_node*[])&kmemCacheNodePtr)->total_objects)
        &kcache_nr_objects=D.LONG(&kcache_total_objects)

        # 物理地址读取数据
        v.value((*(((struct msm_rtb_layout *)(a:00:&msm_rtb_layout_next)))).log_type)
        
        # 获取结构体的某个成员的offset
        &kmem_cache_list_offset=v.value((int)(&((struct kmem_cache *)0)->list))
        
        # 获得某个结构体的大小
        v.sizeof(struct list_head)
        
        # 将字符类型的指针直接转换为"地址->字符串方式"显示
        V.STRING(((struct kmem_cache*)&compareSlub)->name)
        返回：0xC097E4C8 -> "kmem_cache_node"
        
        # 用split截取最后的一项
        &tmp=string.split("&tmp", "\", -1)
        
        
        # 获取地址对应的函数名
        &mm_get_unmapped_area=y.varname(D:&mm_get_unmapped_area)

        sYmbol.FUNCTION(0xFFFFFF800908D778) //这个更准确
        
        # 查看section
        y.l.sec
        
        # 图形化显示
        VAR.DRAW
        
        ETA.PROfileChart.sYmbol
        
        # 字符串截取
        STRing.CUT("abcdef",1) ; result "bcdef"
        STRing.CUT("abcdef",-1) ; result "abcde"
        
        STRing.MID("abcdef",2.,2.) ; result "cd"
        STRing.MID("abcdef",2.,100.) ; result "cdef"
        STRing.MID("abcdef",10.,100.) ; result ""

        # 格式化字符串
        &tmpstr=format.string("&callAddrName", 55., ' ')

        # 格式化
        参考：Display Formats
        
        Var.Watch %Decimal.on %Hex.on i %Hex.OFF k
        ==》Decimal and hex for variable i, but Decimal only for variable k
        
        %m: 都展开后多行显示
        
        # 使用64位整形数
        var.new u64[&entrymax] \ion_clients

        # 强制转型为u32
        &end_idx=v.value((u32)((*(secdbg_log)).idx_irq_exit[&cpu_idx].counter+1.))%(&total_logs+0.)
        
        # 位置
        POS 1. 0. 32. 8 (x,y,width,height)
        
        # 数组用法
        ((struct msm_rtb_layout [&NR_ENTRIES])(a:00:&rtbpaddr))[&idx].caller

        # var.TAB显示数组
        var.tab %s %h (*((*(((struct task_struct)*0xFFFFFFC0A13CAD00).files)).fdt)).fd[0...1000]
        
        # 将指针显示为数组
        (static struct lpm_debug *) lpm_debug = 0xE8BFC000
        
        v.v (struct lpm_debug[0x100])0xE8BFC000
        
        # 显示数组索引
        %i
        
        # var.chain显示list链表
        Var.CHAIN [%<format>] <first> <next> [<pointer> …]]
        
        The first expression must be the first element of the list. The second expression specifies the pointer to the
        next element in the first element.
        
        比如：
        var.chain %h %s (*((*(((struct task_struct)*0xFFFFFFC0A13CAD00).mm)).mmap)) ;(*((*(((struct task_struct)*0xFFFFFFC0A13CAD00).mm)).mmap)).vm_next
        ==>注意:分号不能少，第一个参数要用取一次值：(*(XXXX)), 第二个参数是指针
        
        # 加载进程所需的库
        d.load.Elf *libc.so d:0x398:0xb6eef000 /noclear /nocode /noinclude /gnu /gcc3
        在上面的命令中： D: <spaceid>: < Library start address > 

- 传递带空格的参数

        方法1：
        传递时用引号
        子函数内获取时再自赋值一次，去掉引号
        比如：
        PRIVATE &x &y &z
        &x="My entry issue"
        &y=77.
        &z=TRUE()
        GOSUB level1 "&x" &y &z
        ENDDO
        
        level1:
        (
        PRIVATE &r &s &t
        ENTRY &r &s &t
        &r=&r // Removes quotes from string
        RETURN
        )
        
        方法2：
        用PARAMETERS来接收参数
        比如：
        // Script entry_issue3_params.cmm
        PRIVATE &x &y &z
        &x="My entry issue"
        &y=77.
        &z=TRUE()
        GOSUB level1 "&x" "&y" "&z"
        ENDDO
        level1:
        (
        PARAMETERS &r &s &t
        RETURN
        )


- 显示运行命令的信息

        log.type

- ANC

        Data.LONG(ANC:0xC3FDC0C4) // ANC: indicates
        // physical address (A)
        // No Cache (NC)
        
