# ubuntu #

- 安装火狐中文版

        https://blog.csdn.net/qq_37772981/article/details/79943848

- 设置代理

        1）临时设置
        在终端中输入命令：
        export HTTP_PROXY="http://usr:pwd@proxy_IP:PORT"
        export HTTPS_PROXY="https://usr:pwd@proxy_IP:PORT"

- 查看ubuntu的版本

        cat /etc/issue
        
- 查看ubuntu系统是32位还是64位

        uname -m
        
- ubuntu自带VI编辑器不好用

        Ubuntu预安装的是tiny版本，我们要安装vim的full版本。
        首先，先卸掉旧版的vi：

        sudo apt-get remove vim-common
        sudo apt-get install vim

- 添加用户

        一般linux创建用户的方法如下，
        sudo useradd samlin930_smb
        sudo useradd samlin930_smb
        sudo userdel samlin930_smb
        
        但是ubuntu发行版本有另外的方法：
        sudo adduser samlin930_smb
        然后按提示输入root用户密码和新建账户的密码

- 修改密码

        passwd username1

- ssh带密码登录远程主机

        sudo apt-get install sshpass
        sshpass -p "XXX" ssh user@IP

－ ssh/scp免密码的方式

        使用密钥文件.

        假设主机A（192.168.100.3）用来获到主机B（192.168.100.4）的文件。
        在主机A上执行如下命令来生成配对密钥：
        ssh-keygen -t rsa
        遇到提示回车默认即可，公钥被存到用户目录下.ssh目录，比如root存放在：
        /root/.ssh/id_rsa.pub

        将 .ssh 目录中的 id_rsa.pub 文件复制到 主机B 的 ~/.ssh/ 目录中，并改名为 authorized_keys.
        这样用scp、ssh命令不需要密码来获取主机B的文件了

- 使用国内源

        清华： https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/
        其他： https://www.linuxidc.com/Linux/2017-01/139458.htm

- SSH连接vmware虚拟机

        apt-get install openssh-server

- vm-tool不能安装，且不能复制到虚拟机

        1）卸载sudo apt-get remove open-vm-tools 
        2）重新安装sudo apt-get install open-vm-tools-desktop
        3）sudo reboot

- 看图片

        display pic.png

- 软件安装时遇到缺少依赖

        sudo apt-get -f install

－　多窗口工具

        sudo apt-get install doublecmd-qt

－　wine

        1) 安装wine
        参考： https://wiki.winehq.org/Ubuntu


        2）用wine来装msi
        wine start xx.msi

        3) wine启动非exe的方法
        wine start .wine/drive_c/xxl_start_arm_sim.bat

- beyond compare 破解

        https://blog.csdn.net/zmlovelx/article/details/80426035


# vscode #

    帮助文档：https://code.visualstudio.com/docs/getstarted/tips-and-tricks
    
    1）从 https://code.visualstudio.com/Download 下载deb包 进行安装

    2）安装preview 插件：Markdown Preview Enhanced
    ctl + K, V 进行preview

    3）安装生成pdf的插件：Markdown PDF
    右键,markdown-pdf: Export (pdf)

    4) ctrl+ -/+ 进行字体缩放

    5) 更改颜色主题
    ctrl+k, ctrl+T

    6)关闭右侧的预览界面
    设置里面搜索 "editor.minimap.enabled":
    设置为false即可

    7)以点的方式显示空格
    使用选项："editor.renderWhitespace": "all"

    8)tab用4个空格代替
    使用： "editor.detectIndentation": false

    9)显示终端
    ctrl+shift+M

    10)文件和修改处的跳转
        在最近打开的文件间切换
        Navigate entire history:  Ctrl+Tab

        导航到打开的文件
        Ctrl+P

        最近修改地方间的跳转
        Navigate back:      Ctrl+Alt+-
        Navigate forward:   Ctrl+Shift+-

    11)选择
        选择一个单词
        Ctrl+D

        选择一行
        Shift+Alt+Right

        选择多行
        按shift后点击鼠标

        选择列
        按住Shift+Alt后拖动鼠标

    12)查找
        查找文件
        ctr+p 后输入部分文件名

    13)排除workspace下的某个folder中的特定目录 folder1

    在settings.json中加入：
    "files.exclude": {
        "**/folder1": true
      },

   
    
# 1 ATOM #

- 快捷键

    http://blog.csdn.net/sinlov/article/details/51560316

- 设置tab为空格

    File => Settings,在 Editor 下:
    atomic soft tabs 去掉
    soft tabs 选中
    tab length 值为 2
    tab type 值为 soft

- 常见package

    Markdown Preview Enhanced

    markdown-writer
    Add your keymaps To add the original default keymaps, run command (cmd + shift + p),
    enter Markdown Writer: Create Default Keymaps.

    pdf导出(markdown-themeable-pdf、pdf-view)
    同步滚动(markdown-scroll-sync)
    代码增强(language-markdown)
    表格编辑(markdown-table-editor)

# 2 pycharm #

- 快捷键
    
        Alt+Enter： 采取快捷菜单中的建议，此时import命令会被添加到导入模块的代码部分
        Ctrl+P:     brings up a list of valid parameters.
        Ctrl+Shift+Backspace:  (Navigate | Last Edit Location)
        Use Ctrl+Shift+F7:         (Edit | Find | Highlight Usages in File)
        Use F3 and Shift+F3:     keys to navigate through highlighted usages
        Ctrl+E:                    (View | Recent Files) brings a popup list of the recently visited files
        Ctrl+空格:      using basic code completion

# xx-net #

    1）开启ipv6
    https://github.com/XX-net/XX-Net/wiki/IPv6-Linux

    sudo miredo

    2）参考以下进行linux系统的相关设置
    https://github.com/XX-net/XX-Net/wiki/How-to-use

    ./start
    
    3)部署个人APP ID


# 3 IPV6 Teredo隧道 #

- 参考

        参考这个开启WIN7上的Teredo隧道
        http://bbs.pcbeta.com/viewthread-1580771-1-1.html

        https://github.com/XX-net/XX-Net/issues/6918#issuecomment-334978237

- 使能teredo
        
        当使用xx-net仍然无法访问外网时，运行：XX-NET\code\default\gae_proxy\local\ipv6_tunnel\enable_ipv6.bat

- 其他

        This address is an IPv4 address:
        IP v4 :    
        decimal     :  192.168.9.230    
        binary     :  11000000101010000000100111100110    
        octal     :  0300.0250.011.0346    
        hexadecimal     :  0xC0.0xA8.0x09.0xE6    
        long     :  3232238054    
        
        IP v6 :    
        6 to 4 address     :  2002:C0A8:9E6:0:0:0:0:0    
        :  2002:C0A8:9E6::    
        IPv4-mapped address     :  0:0:0:0:0:FFFF:192.168.9.230    
        :  ::FFFF:192.168.9.230    
        :  ::FFFF:C0A8:09E6    
        IPv4-compatibility address    :  0:0:0:0:0:0:192.168.9.230    
        :  ::192.168.9.230    
        :  ::C0A8:09E6    
    
        1. ifconfig /all 查看 Teredo Tunneling Pseudo-Interface 隧道适配器存在。
        如果没有，确保服务里的IP helper services 已经自动开启了
        
        2. netsh int ipv6 show teredo
        
        Teredo 参数
        ---------------------------------------------
        类型                    : enterpriseclient (Group Policy)
        服务器名称              : teredo.remlab.net (Group Policy)
        客户端刷新间隔          : 30 秒
        客户端端口                : unspecified
        状态                    : qualified
        客户端类型              : teredo client
        网络                    : managed
        NAT                     : symmetric (port)
        NAT 特殊行为   : UPNP: 否，PortPreserving: 否
        本地映射           : 192.168.0.58:59581
        外部 NAT 映射    : 123.151.146.189:45812
        
        
        检查路由表，netsh int ipv6 show route，看看你设置的是不是唯一的::/0项。
        netsh int ipv6 show route
        
        teredo.remlab.net
        teredo.trex.fi
        win10.ipv6.microsoft.com
        
        route DELETE ::/0
        
        netsh int ipv6 add route ::/0 "Teredo Tunneling Pseudo-Interface" metric=1

# windows环境变量 #

    1.查看path变量值
    C:\Users>echo %path%
    
    2.设置环境变量abcd (当前窗口有效)
    C:\Users>set abcd="aaaaaaa"
    
    3.追加环境变量(当前窗口有效)
    set path=%path%;D:\Java\jdk1.6.0_24\bin
    
    4. 环境变量立即生效
    以修改环境变量“PATH”为例，修改完成后，进入DOS命令提示符，输入：set PATH=C: ，关闭DOS窗口。
    再次打开DOS窗口，输入：echo %PATH% ，可以发现“我的电脑”->“属性”->“高级”->“环境变量”中设置的 PATH 值已经生效。
    不用担心DOS窗口中的修改会影响环境变量的值，DOS窗口中的环境变量只是Windows环境变量的一个副本而已。
    但是对副本的修改却会引发Windows环境变量的刷新，这正是我们想要的!
    
    SET _JAVA_OPTIONS=-Xmx512M

# java环境变量 #

    1. 在系统环境变量里设置：
    JAVA_HOME:
    C:\Program Files\Java\jdk1.8.0_152
    
    CLASSPATH:
    .;%JAVA_HOME%\lib\dt.jar;%JAVA_HOME%\lib\tools.jar;
    
    Path里添加：
    %JAVA_HOME%\bin;%JAVA_HOME%\jre\bin;
    
    JRE_HOME:
    C:\Program Files\Java\jre1.8.0_152
    
    2. 检查是否设置成功:
    java -version
    或javac
    看能否正常输出
    
    3. 命令窗口里临时更改环境变量：
    set JAVA_HOME=C:\Program Files (x86)\Java\jdk1.8.0_144
    set CLASSPATH=%JAVA_HOME%\lib\dt.jar;%JAVA_HOME%\lib\tools.jar
    set path=%path%;%JAVA_HOME%\bin


# diagnostics tracking service导致vhost占用CPU高 #

    1. 如果是cpu 的卡顿的话，禁用DIAGTRACK service服务
    方法如下 用键盘按WIN+R调出“运行”程序，输入services.msc
    在本地服务找到diagnostics tracking service服务，双击打开，停止该服务并且设置启动类型为禁用，
    提示“恢复”标签，一栏中的“重新启动该服务”选项应该改为“无操作”

# source insight #

    1)下载 3.5 版本
    https://www.sourceinsight.com/download/

    注册码：
    SI3US-205035-36448
    SI3US-466908-65897
    SI3US-368932-59383
    SI3US-065458-30661
    SI3US-759512-70207

    2)创建一个Custom Command: ShellExecute open %d. 然后关联一个快捷键。
    或者 explorer /select,%f

    3.50.0058(或60),注册码是SI3US-361500-17409


# ultraedit #

    使用正则表达式 ^p$ 将空行替换为空，相当于删除了空行。

# markdwon #

    https://www.jianshu.com/p/82e730892d42

    多级无序列表
    - 1
       - 2
          - 3
              - 4
    
# make #

- $(if CONDITION,THEN-PART[,ELSE-PART])

        对于参数“CONDITION”，在函数执行时忽略其前导和结尾空字符并展开：
        - 如果展开结果非空，则条件为真，就将第二个参数“THEN_PATR”作为函数的计算表达式，函数的返回值就是“THEN-PART”的计算结果；
        - 如果展开结果为空，将第三个参数“ELSE-PART”作为函数的表达式，返回结果为表达式“ELSE-PART”的计算结果。

# bat #

- DOS批处理中%~dp0表示什么意思

        文件内容如下：
        @echo off
        echo [INFO] %~dp0
        pause
        
        运行install.bat，命令行输出如下：
        [INFO] D:\jeesite\bin\
        
        即：输出install.bat文件所在的路径，
        %0代表文件本身
        d代表盘符
        p代表路径
        
        用于为了避免使用绝对路径的情况，如1.bat中需要调用当前目录下的2.bat：
        
        1.bat的内容：
        @echo off
        REM ======================================================
        REM call 2.bat
        REM ======================================================
        call %~dp0\2.bat
    
- 不显示执行的命令

        方法有：
        1）在命令前加@，适用于命令数较少的情况
        如：
        @REM getelf
        
        2）在所有的命令前加 @echo off
        如：
        @echo off
        REM getelf 