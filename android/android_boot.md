
Init.cpp (system\core\init):    am.QueueEventTrigger("early-init");  //1 先on early-init
Init.cpp (system\core\init):    am.QueueEventTrigger("init");  //2. on init
Init.cpp (system\core\init):    am.QueueEventTrigger("charger");  //3.kernel的cmdline里有：android.bootmode=charger是执行
Init.cpp (system\core\init):    am.QueueEventTrigger("late-init"); //3.非charger情况下on late-init, 它里面触发on early-boot, on boot

Init.cpp (z:\home\xxl\aosp\system\core\init):

    // Don't mount filesystems or start core system services in charger mode.
    std::string bootmode = GetProperty("ro.bootmode", "");
    if (bootmode == "charger") {
        am.QueueEventTrigger("charger");
    } else {
        am.QueueEventTrigger("late-init");  //触发on late-init


init.rc中：
on late-init
    trigger early-fs
    trigger fs
    trigger post-fs
    trigger post-fs-data

    # Load properties from /system/ + /factory after fs mount. Place
    # this in another action so that the load will be scheduled after the prior
    # issued fs triggers have completed.
    trigger load_system_props_action

    # Remove a file to wake up anything waiting for firmware
    trigger firmware_mounts_complete

    trigger early-boot //4
    trigger boot  //5 触发on boot


on boot
    ifup lo
    hostname localhost
    domainname localdomain

    class_start default  //========启动default类的service（方式1）


========启动service的方式2：

service data_on /system/bin/ext_data_on.sh  -u
    user root
    disabled //默认是disable
    oneshot

但我们可以通过 property_set("ctl.start", service_xx) 来启动，
比如：
proprietories-source/phoneserver/ps_service.c:643:   property_set("ctl.start", "data_on");  //启动服务配置网卡参数

命令：setprop ctl.start qtnrfon


================================
service 启动分析

参考：https://blog.csdn.net/chaoy1116/article/details/44751443

/system/core/init/...:

static int do_class_start(const std::vector<std::string>& args) {
        /* Starting a class does not start services
         * which are explicitly disabled.  They must
         * be started individually.
         */
    ServiceManager::GetInstance().
        ForEachServiceInClass(args[1], [] (Service* s) { s->StartIfNotDisabled(); });
    return 0;
}

-> bool Service::StartIfNotDisabled() {
    if (!(flags_ & SVC_DISABLED)) { //没有设置disabled的service
        return Start();
    } else {
        flags_ |= SVC_DISABLED_START;
    }
    return true;
}

-> bool Service::Start() 
{
    ...
    LOG(INFO) << "starting service '" << name_ << "'...";
     pid_t pid = -1;
    if (namespace_flags_) {
        pid = clone(nullptr, nullptr, namespace_flags_ | SIGCHLD, nullptr);
    } else {
        pid = fork();
    }
}


=================================
service adbd /sbin/adbd --root_seclabel=u:r:su:s0 --device_banner=recovery
    #这个服务不会同与他同trigger（触发器）下的服务自动启动。他必须被明确的按名启动。