# 命令 #

- 自动输入sudo密码

		echo password | sudo -S shutdown -h now //立刻关机；如果用1表示1分钟后关机
		参数-S,这个参数是让sudo从标准输入流读取而不是终端设备

- 查找

	- find 文件/文件夹
	
			参考：https://blog.csdn.net/guyongqiangx/article/details/73000434
				http://man.linuxde.net/find  //find命令

			注意： 带通配符匹配的部分，要加上双引号

		    find /etc -name "*srm*"  //在/etc目录下查找文件名包括srm的文件
			find /etc -name "*srm*" -type d  //查找目录？
			
			find / -name "*.txt"  2>/dev/null //忽略查找时的输出的错误log
			
			find . -iname makefile  //查找当前目录下所有名为makefile的文件，并忽略大小写
			find . -iname "*.iso" -size +100M  //查找当前目录下所有大于100MB的ISO文件

			find . -type d -name libmediaplayerservice //查找名为的libmediaservice文件夹

			find . -name "*.dts" -path "*/tests/*" //查找当前所有路径中包含tests的目录下的*.dts文件

			find . -type f | wc -l //统计当前目录下文件的数目

			-exec  //对查找结果进行指定操作
			find . -name "*.txt" -type f -print -exec rm -rf {} \;  //删除目录及其子目录下某种类型文件

			-a/-o  //多个条件合并查找
			-prune //指定排除查找的条件
			
			查找最近修改过的文件:
			find ./ -mtime 0：返回最近24小时内修改过的文件。
			find ./ -mtime 1 ： 返回的是前48~24小时修改过的文件。
			那怎么返回2天内修改过的文件？find还可以支持表达式关系运算，所以可以把最近几天的数据一天天的加起来：
			find ./ -mtime 0 -o -mtime 1 

			另外， -mmin参数-cmin / - amin也是类似的。

            
            查找大小在某个范围内的文件使用-size参数，-size +n表示大于n单位的范围，-size –n表示小于n单位的范围。
            将查出来的文件以详细列表形式显示出来:
            find . -type f -mtime -1 -size +100M -size -2G | xargs ls –l
			

	- grep 内容查找

		    grep -nR "build" ./* 2>/dev/null >../build.txt 
			//在当前目录下查找包括build的文本行(显示行号)，并将结果输出到build.txt
			//2>/dev/null 表示排除错误log
		
		    grep 'test' d* 		//查找所有以d开头的文件中包含test的行
		    grep 'test' aa bb cc //查找在aa，bb，cc文件中包含test的行

			grep -nR "BRILLO_USE_" . --exclude-dir=out //查找时排除out目录

            grep -nR "charger" . --include=*.rc //在指定后缀的文件中查找charger


            如果关键子带点，则要加\进行转义：
            grep "\.c"

            //查找多个关键字
            adb shell dmesg | grep -i 'healthd\|smb\|usb\|\[FG\]'

	- locate

    		locate libc.a  #查找libc.a的位置

	- whereis/which
	
    		whereis gcc, which gcc 	#在哪些位置有gcc文件

- 查看大小

		df -h //查看每个文件系统对应的分区的使用情况
		du -sh //查看各文件/文件夹的大小.
		ls -lh //类型du -h, 只是显示方式不一样

- 合并文件 past

		参考: https://blog.csdn.net/andy572633/article/details/7214126

		格式为: paste -d -s -file1 file2
		
		选项含义如下：
		-d 指定不同于空格或tab键的域分隔符。例如用@分隔域，使用 -d @
		-s 将每个文件合并成行而不是按行粘贴
		- 使用标准输入。例如ls -l |paste ，意即只在一列上显示输出。
		
		例子：
		文件： pas1
		ID897
		ID666
		ID982

		文件： pg pas2
		P.Jones
		S.Round
		L.Clip

		1) paste pas1 pas2 //将pas1和pas2两文件粘贴成两列
		=>
		ID897   P.Jones
		ID666   S.Round
		ID982   L.Clip
		
		2）paste -d ":" pas2 pas1 //用冒号做域分隔符
		=>
		P.Jones:ID897
		S.Round:ID666
		L.Clip:ID982
	
		3) paste -s pas1 pas2 //合并为两行, 第一行粘贴为ID号，第二行是名字
		=>
		ID897   ID666   ID982
		P.Jones S.Round L.Clip

- cp 拷贝指定的目录

    	cp -r s/c  d/   //d目录变成d/c, 注意要加-r

- scp 拷贝远程服务器上的文件到本地

		拷贝远程服务器192.168.1.112的目录/tmp/test到当前目录下。
		[root@CentOS_Test_Server tmp]# scp -r root@192.168.1.112:/tmp/test ./

- 删除指定文件(夹)外的文件(夹)

		rm -rf  !(arm64|Kconfig)
		=> 删除 除arm64和Kconfig外 的所有文件和文件夹

- tar

    	解压: tar zxvf XXX.gz -C /home/test  //-C是指定解压后的目录
        压缩文件夹：tar zcvf xxx.gz folder

- chown: 改变拥有者和群组

		格式：chown <uid>:<gid> 文件
	
		[root@localhost test6]# ll
		---xr--r-- 1 root users 302108 11-30 08:39 log2012.log
	
		[root@localhost test6]# chown mail:mail log2012.log 
		[root@localhost test6]# ll
		---xr--r-- 1 mail mail  302108 11-30 08:39 log2012.log

- chmod: 改变文件的访问权限

		格式chmod [-cfvR] [--help] [--version] mode file  
		
		文件的 所有者权限/所有者所属组的用户的权限/其他用户的权限 | 文件的所有者/文件所属的组
		-rw-r--r—  1(文件链接的个数) root root 302108 11-13 06:03 log2012.log
	
		r: 读权限，对应数字4
		w: 写权限，对应数字2
		x: 执行权限：对应数字1
		所以如果rwx，则为7
		文件类型： 普通文件(-)、目录(d)、字符设备文件(c)、块设备文件(b)、符号链接文件(l)
	
		**实例**
		
		chmod a+x log2012.log //增加文件所有用户组可执行权限
		chmod ug+w,o-x log2012.log  
		=> 设定文件text的属性为：文件属主(u)增加写权限;与文件属主同组用户(g)增加写权限;其他用户(o)删除执行权限


- who //当前有哪些会话

- 多页显示

    	ls | more

- kill进程

    	Kill –s 9 <pid> #强制杀死一个进程

- command1 || command2

	    含义： 如果||左边的command1执行失败(返回1表示失败)，就执行&&右边的command2
	
	    实例： 打印1111.txt的第一列内容，若执行不成功则执行显示facebook.txt的内容
	    [root@RHEL5 shell]# awk '{print $1}' 1111.txt || cat facebook.txt   
	    awk: cmd. line:1: fatal: cannot open file `1111.txt' for reading (No such file or directory)
	    google 110 5000
	    baidu 100 5000
	    guge 50 3000
	    sohu 100 4500

- 将某个命令的结果作为输入

		1）使用 `
		格式： `命令`
		makegpt `paste -d ":" pas2 pas1`

- 查看linux环境变量

		$ env
		=>
		_=/system/bin/env
		ANDROID_DATA=/data
		DOWNLOAD_CACHE=/data/cache
		LOGNAME=shell
		HOME=/
		ANDROID_ROOT=/system
		TERM=dumb
		SHELL=/system/bin/sh
		ANDROID_BOOTLOGO=1
		TMPDIR=/data/local/tmp
		ANDROID_ASSETS=/system/app
		BOOTCLASSPATH=/system/framework/core-oj.jar:...

# VI命令 #

		显示所有行号: set nu

		复制当前整行： yy, 5yy就是复制5行
		复制当前光标所在位置到单词尾字符的内容: yw, 2yw就是复制两个单词
		复制光标所在位置到行尾内容: y$
		复制光标所在位置到行首内容: y^
		剪切整行: dd, 如：4dd //剪切4行
		粘贴缓冲区中的内容: p
		复制第m行到第n行之间的内容：m,ny
		撤销所有在前一个编辑行上的操作: U
		跳转到指定行: 行号

- 如何删除全部内容

		在命令模式下，输入 .,$d   ，一回车就全没了。
		表示从当前行到末行全部删除掉。
		用gg表示移动到首行。


- vim 查看二进制

		方法１：vim
		vim -b egenea-base.ko   加上-b参数，以二进制打开
		然后输入命令  :%!xxd -g 1  切换到十六进制模式显示

		方法２：hexdump
		apt-get install libdata-hexdumper-perl
		安装好之后就可以直接hexdump your_binary_file

        xxl@HP-Z228:~/Downloads/br2$ hexdump -Cv Untitled-4  //字节方式显示且不要省略
        00000000  00 0a 32 0a 33 0a 35 30                           |..2.3.50|
        00000008

        hexdump -Cv testfile -s skip_bytes -n show_number_bytes //只显示某一段
        xxl@HP-Z228:~/Downloads/br2$ hexdump -Cv Untitled-4 -s 1 -n 3
        00000001  0a 32 0a                                          |.2.|
        00000004

		也可以直接使用hd命令来代替hexdump
		如果想要慢慢看 ： hd your_binary_file | more

－　vimdiff 比较两个二进制文件

		vim -bd base.ko base2.ko

		打开后就可以在两个窗口里面显示两个文件

		ctrl + W +L  把输入焦点切换到右边的窗口，激活右边的窗口后输入的命令就是针对右窗口了
		:%!xxd -g 1  切换成十六进制的一个字节的模式

		ctrl + W +H  把输入焦点切换到左边的窗口 
		:%!xxd -g 1 
		] + c  查找上一个不同点
		[ + c  查找下一个不同点

- 比较文件差异

        两种方法
        1) diff file1 file2

        2) meld file1 file2

# shell #

- echo

        参考： https://jingyan.baidu.com/article/da1091fb1620a2027949d642.html

        echo后的单引号表示强引用，单引号里面是什么就输出什么，而双引号是弱引用，变量的值会代替变量名输出。

        如果变量与其它字符相连的话，需要使用大括号（{ }）
        如：echo "${year}-${mouth}-${day}"

        如果要不换行显示，可以加参数 -n，它就会忽略当前行的换行符
        如：
        echo -n "guoke!"
        echo "Hello World!"

        原样输出字符串,若需要原样输出字符串（不进行转义），请使用单引号。
        如
        name="guoke"
        echo '$name\"'
        => guoke\"

        显示命令执行结果，这里用的是反绰号
        如：
        echo `pwd`
        =>/root

- 获取文件sha1

        sha1() {
            sha1sum $1 | awk '{print $1}'
        }
        
        sha1 "/home/cheng/vista.img"

- [和[[的区别

        区别一。在[中使用逻辑运算符，需要使用-a（and）或者-o（or）。在[[中使用逻辑运算符，需要使用&&或者||。

        区别二。[是shell命令，在它包围的表达式是它的命令行参数，所以串比较符>和<需要转义，否则就变成io重定向了。[[是shell关键字，不会做命令行扩展，所以<和>不需要进行转义。但是语法相对严格，如在[中可以用引号括起操作付，[[则不行。如if [ "-z" "ab" ]。

        区别三。[[可以做算术扩展，[则不行。如if [[ 11+1 -eq 100 ]]，而if [ 11+1 -eq 100 ]则会报错。

- basename

        basename命令用于去掉文件名的目录和后缀（strip directory and suffix from filenames），对应的dirname命令用于截取目录
        
        BOOTLOADER_EMMC    = $(shell basename $(TARGET_EMMC_BOOTLOADER))

- 截取字符串

        https://blog.csdn.net/dong18292000671/article/details/74458006

        1.从右边第几个字符开始，及字符的个数。
        代码：${var:0-11:3}
        其中的 0-11 表示右边算起第11个字符开始，3 表示截取的字符数。

- 获取当前目录

        base_path=$(cd `dirname $0`; pwd)