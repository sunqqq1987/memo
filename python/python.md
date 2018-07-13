# 设置为阿里云的pip源 #

在当前用户的目录下创建pip文件夹，然后创建pip.ini文件，写入如下内容: 

    [global]
    index-url = https://mirrors.aliyun.com/pypi/simple/
    [install]
	trusted-host = mirrors.aliyun.com

注意最好用notepad++创建ini文件，否则可能不起效。

# 全局配置 #

查看
    
    vi ~/.gitconfig
    git config --list
  
修改

    git config --global user.name "输入你的用户名"

# 常见语法 #

- 参考：http://www.runoob.com/python/python-func-zip.html

- struct模块

    	参考：　https://www.cnblogs.com/hushaojun/p/6489350.html

		pack、unpack、pack_into、unpack_from函数

		#!/usr/bin/env python  
		#encoding: utf8  

		import sys  
		reload(sys)  
		sys.setdefaultencoding("utf-8")  
		
		import struct  
		
		a = 20  
		b = 400   
		
		# pack  
		str = struct.pack("ii", a, b)  
		print 'length: ', len(str)          # length:  8  
		print str                           # 乱码：   
		print repr(str)                     # '\x14\x00\x00\x00\x90\x01\x00\x00'  
		
		# unpack  
		str2 = struct.unpack("ii", str)  
		print 'length: ', len(str2)          # length:  2  
		print str2                           # (20, 400)  
		print repr(str2)                     # (20, 400)

		＃calcsize
		print "len: ", struct.calcsize('i')       # len:  4  
		print "len: ", struct.calcsize('ii')      # len:  8  
		print "len: ", struct.calcsize('f')       # len:  4  
		print "len: ", struct.calcsize('ff')      # len:  8  
		print "len: ", struct.calcsize('s')       # len:  1  
		print "len: ", struct.calcsize('ss')      # len:  2  
		print "len: ", struct.calcsize('d')       # len:  8  
		print "len: ", struct.calcsize('dd')      # len:  16

		＃pack_into，unpack_from
		from ctypes import create_string_buffer  
  
		buf = create_string_buffer(12)  
		print repr(buf.raw)     # '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  
		
		struct.pack_into("iii", buf, 0, 1, 2, -1)  
		print repr(buf.raw)     # '\x01\x00\x00\x00\x02\x00\x00\x00\xff\xff\xff\xff'  
		
		print struct.unpack_from("iii", buf, 0)     # (1, 2, -1)

		＃struct 类型表
		Format	C Type	Python type	Standard size	Notes
		x 	pad byte 	no value 	  	 
		c 	char 	string of length 1 	1 	 
		b 	signed char 	integer 	1 	(3)
		B 	unsigned char 	integer 	1 	(3)
		? 	_Bool 	bool 	1 	(1)
		h 	short 	integer 	2 	(3)
		H 	unsigned short 	integer 	2 	(3)
		i 	int 	integer 	4 	(3)
		I 	unsigned int 	integer 	4 	(3)
		l 	long 	integer 	4 	(3)
		L 	unsigned long 	integer 	4 	(3)
		q 	long long 	integer 	8 	(2), (3)
		Q 	unsigned long long 	integer 	8 	(2), (3)
		f 	float 	float 	4 	(4)
		d 	double 	float 	8 	(4)
		s 	char[] 	string 	1 	 
		p 	char[] 	string 	  	 
		P 	void * 	integer 	  	(5), (3)




- Couter类

		Counter类的目的是用来跟踪值出现的次数。它是一个无序的容器类型，以字典的键值对形式存储，其中元素作为key，其计数作为value。
		
		most_common([n])方法：
		返回一个TopN列表。如果n没有被指定，则返回所有元素。当多个元素计数值相同时，排列是无确定顺序的。

		>>> c = Counter('abracadabra')
		>>> c.most_common()
		[('a', 5), ('r', 2), ('b', 2), ('c', 1), ('d', 1)]
		>>> c.most_common(3)
		[('a', 5), ('r', 2), ('b', 2)]

		http://www.pythoner.com/205.html

- zip()

		zip() 函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表。
		如果各个迭代器的元素个数不一致，则返回列表长度与最短的对象相同，利用 * 号操作符，可以将元组解压为列表。

		>>>a = [1,2,3]
		>>> b = [4,5,6]
		>>> c = [4,5,6,7,8]
		>>> zipped = zip(a,b)     # 打包为元组的列表
		[(1, 4), (2, 5), (3, 6)]
		>>> zip(a,c)              # 元素个数与最短的列表一致
		[(1, 4), (2, 5), (3, 6)]
		>>> zip(*zipped)          # 与 zip 相反，可理解为解压，返回二维矩阵式
		[(1, 2, 3), (4, 5, 6)]

		用法1：构建word与id之间的映射关系，即word是key, id是value
	    word_to_id = dict(zip(words, range(len(words))))
	    return words, word_to_id
		
# dict用法

	http://www.runoob.com/python/python-dictionary.html

# 字符串截取 （用括号）#
    
    str = '0123456789′
    print str[0:3] 		#截取第一位到第三位的字符
    print str[:] 		#截取字符串的全部字符
    print str[6:] 		#截取第七个字符到结尾
    print str[:-3] 		#截取从头开始到倒数第三个字符之前
    print str[2] 		#截取第三个字符
    print str[-1] 		#截取倒数第一个字符
    print str[::-1] 	#创造一个与原字符串顺序相反的字符串
    print str[-3:-1] 	#截取倒数第三位与倒数第一位之前的字符
    print str[-3:] 		#截取倒数第三位到结尾
    print str[:-5:-3] 	#逆序截取，具体啥意思没搞明白？

# 字符串格式化 #

http://www.cnblogs.com/xxby/p/5571620.html

- 实例

	    print("{:5d} {:7.2f}".format(fahrenheit , celsius))
	    	{:5d}的意思是替换为 5 个字符宽度的整数，宽度不足则使用空格填充。
	    
	    <  内容左对齐
	    >  内容右对齐(默认)
	    ＝ 内容右对齐，将符号放置在填充字符的左侧，且只对数字类型有效。 即使：符号+填充物+数字
	    ^  内容居中

- 格式化位所占宽度

	    s1 ='---{:*^20s}----'.format('welcome') #中间是welcom3,两侧均匀补齐*,直到满20个字符
	    print(s1)
	    ==> ---******welcome*******----
	    
	    s2 ='---{:*>20s}----'.format('welcome') #welcome的前面补齐*,直到满20个字符
	    print(s2)
	    ==> ---*************welcome----
	    
	    s3 ='---{:*<20s}----'.format('welcome') #welcome的后面补齐*,直到满20个字符
	    print(s3)
	    ==> ---welcome*************----


# 正则表达式 #

http://www.runoob.com/python/python-reg-expressions.html

- 实例

	    [Pp]ython	匹配 "Python" 或 "python"
	    rub[ye]	匹配 "ruby" 或 "rube"
	    [aeiou]	匹配中括号内的任意一个字母
	    [0-9]	匹配任何数字。类似于 [0123456789]
	    [a-z]	匹配任何小写字母
	    [A-Z]	匹配任何大写字母
	    [a-zA-Z0-9]	匹配任何字母及数字
	    [^aeiou]	除了aeiou字母以外的所有字符
	    [^0-9]	匹配除了数字外的字符

- 其他匹配参考

		http://blog.jobbole.com/74844/

# Anaconda #


- **conda命令**

	    # 查看conda的env
	    conda info --envs
	    
	    # 创建conda env
	    conda create --name tfenv python==3.6.3
	    
	    # 激活env
	    activate tfenv
	
	    # 查找package信息
	    conda search numpy
	    
	    # 查看当前环境下已安装的包
	    conda list
	    
	    # 安装package
	    conda install -n python34 numpy # 如果不用-n指定环境名称，则被安装在当前活跃环境 也可以通过-c指定通过某个channel安装
	    conda install tensorflow==1.2.1 # 安装指定版本的tensorflow
	
	    # 更新package
	    conda update -n python34 numpy
	    
	    # 删除package
	    conda remove -n python34 numpy
	    
	    # 更新conda，保持conda最新
	    conda update conda
	    
	    # 更新anaconda
	    conda update anaconda


# scrapy #

.....

# pip #

- 安装pip3

        sudo apt-get install python3-pip

        sudo pip3 install pycrypto  //pip3方式安装pycrypto包

- **命令**

	    # 安装模块
		pip install --upgrade pip --trusted-host pypi.python.org
		=> 等同于 easy_install -U pip
	    
	    # 更新模块
	    1) 使用控制台命令进入到pip的安装路径：D:/Python27/Lib/site-packages
	    2) 使用更新命令行：pip install -U PackageName
	   
	    # 卸载模块
	    1) 使用控制台命令进入到pip的安装路径：D:/Python27/Lib/site-packages
	    2）使用更新命令行：pip uninstall PackageName
	    
	    # 查看安装的模块
	    pip list

	- 设置代理并消除SSL错误（SSL: CERTIFICATE_VERIFY_FAILED ）的方法

	    1）使用anconda安装scrapy 
	    注意：win7 64 bit系统上安装anacoda2 64bit, win10上可以安装anaconda2 32bit版本
	    先设置IE代理，再：
	    
	    conda config --set ssl_verify false
	    conda install scrapy
	    conda install lxml
	    
	    2）使用pip安装
	    
	    pip install pyspider --trusted-host pypi.python.org --proxy=IP:PORT
	    
	    或者设置IE代理后：
	    pip install pyspider --trusted-host pypi.python.org

- **安装selenium**

    	pip install selenium --trusted-host pypi.python.org


- **安装beautifulsoup4**

    	pip install beautifulsoup4 --trusted-host pypi.python.org


- **安装lxml**

	    1.在网址 http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml 下,搜索lxml，下载Python对应的lxml版本。
	    2.打开cmd,进入到lxml下载的文件夹，运行如下命令(注意：一定要下载Python对应的lxml版本)：
	    pip install lxml-3.7.1-cp27-cp27m-win32.whl


# python issue #

- UnicodeEncodeError: 'gbk' codec can't encode character u'\ubb38'
    
		在文件开始处加上：#coding: utf8

- SSL错误

    	git config --global http.sslVerify false

# python自动化 #

## beautifulsoup4 ##

- findAll()
	
		http://blog.csdn.net/winterto1990/article/details/47624167
		
		1）属性都放着attrs这个字典中，当某个属性的值不是定值的时候，可以使用   '属性名':True  这种方式。

		2） 返回HTML文档中attribute1和attribute2属性的tag标签:
		findAll("tag",{"classs":{"attribute1","attribute2"}})
		
		3）多属性查找：
		newMash = soup.find("div", attrs={"id": "newMash", "class": "mask", "style": True})
		
		4）class名带空格时，不要用selenium默认的:
		browser.find_element_by_class_name("layui-layer-ico layui-layer-close layui-layer-close1") //失败
		需要用find:
		soup.find("a", attrs={"class": "layui-layer-ico layui-layer-close layui-layer-close1"})


- css选择器
		
		http://blog.csdn.net/zjiang1994/article/details/52669080
		https://www.cnblogs.com/kongzhagen/p/6472746.html
		
		通过标签父子关系定位（少用吧）
		find_element_by_css_selector("父标签>子标签") 
		find_element_by_css_selector("span>input")
		=> 表示选择父标签为span的所有input元素

- 其它

		# classes1=browser.find_elements_by_class_name("cta")
		# for cls in classes1:
			#print "href is: " + cls.get_attribute("href")
			##option.click()
		
		
		#<input id="kw" class="s_ipt" name="wd" value="" maxlength="255" autocomplete="off">
		#通过id方式定位
		#browser.find_element_by_id("kw").send_keys("selenium")
		#通过name方式定位
		#browser.find_element_by_name("wd").send_keys("selenium")
		#通过tag name方式定位
		#browser.find_element_by_tag_name("input").send_keys("selenium")
		#通过class name 方式定位
		#browser.find_element_by_class_name("s_ipt").send_keys("selenium")
		#通过CSS方式定位
		#browser.find_element_by_css_selector("#kw").send_keys("selenium")
		#通过xpath方式定位
		#browser.find_element_by_xpath("//input[@id='kw']").send_keys("selenium")
		#在form/span[1]层级标签下有个input标签的id=kw的元素, not work
		#browser.find_element_by_xpath("//input[@id='kw']/form/span").send_keys("selenium")
		#firefox最简xpath
		#browser.find_element_by_xpath("//*[@id='kw']").send_keys("selenium")
		
		#通过文字链接来定位
		#browser.find_element_by_link_text("贴吧").click()
		#time.sleep(10)  # 休眠3秒
		
		#<input id="su" class="bg s_btn" value="百度一下" type="submit">
		#browser.find_element_by_id("su").click()
		#time.sleep(5)  # 休眠3秒
		
		#获得属性值。
		#select = driver.find_element_by_tag_name("select")
		#allOptions = select.find_elements_by_tag_name("option")
		#for option in allOptions:
		#	print "Value is: " + option.get_attribute("value")
		#	option.click()
		
		#将滚动条移动到页面的顶部
		#js="var q=document.documentElement.scrollTop=0"
		#driver.execute_script(js)
		
		#http://www.cnblogs.com/fnng/p/3606934.html
		#将用户名密码写入浏览器cookie
		#driver.add_cookie({'name':'Login_UserNumber', 'value':'username'})
		#driver.add_cookie({'name':'Login_Passwd', 'value':'password'})
	
		#news = browser.find_element_by_xpath("//div[@id='title-box']/a[1]").text
		#print news
		
		
		#href = browser.find_element_by_xpath("//div[@id='title-box']/a[1]").get_attribute('href')
		#name = browser.find_element_by_xpath("//div[@id='title-box']/a[2]").get_attribute('name')
		#print href

# Selenium #
	
- 插件下载：http://docs.seleniumhq.org/download/

- PhantomJS

		PhantomJS命令行选项
		https://www.cnblogs.com/themost/p/6907183.html0

		phantomjs_path = r'C:\ProgramData\Anaconda3\envs\tensorflow_env\Scripts\phantomjs-2.1.1\phantomjs.exe'
		# 关闭图片加载，开启缓存，忽略https错误
		phantomjs_service_args = ['--load-images=no', '--disk-cache=yes', '--ignore-ssl-errors=true']
    	browser = webdriver.PhantomJS(executable_path=phantomjs_path, service_args=phantomjs_service_args)

- Chromedriver for chrome
		
- geckodriver for firefox
	
		https://github.com/mozilla/geckodriver/
		下载：https://github.com/mozilla/geckodriver/releases
		
		cus_profile_dir= r"D:\tool\firefox\ssl-p3"
		browser= webdriver.Firefox(cus_profile_dir)


## 后台运行python脚本 ##

    	nohup python ./transfer_cl.py &

		ps -A | grep "python" 来获得pid，最后可以通过kill来将其杀掉

## 软件list ##

	    python27
	    psutil-4.3.0.win32-py2.7.exe#md5=1497af4fd8cfacfd40649d61c4593611.exe
	    PIL-1.1.7.win32-py2.7.exe
	    pywin32-220.win32-py2.7.exe
	    python-xlib-master.zip
	    PyMouse-0.4.tar.gz
	    wxPython3.0-win32-3.0.2.0-py27.exe
	    pyHook-1.5.1.win32-py2.7.exe
	    source+pyhk0.36_py2.6.zip

- not work well for simulate cursor left and right click

		# slect all->copy by simulate cursor
	
		win32api.SetCursorPos((x,y))
		win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
		win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)
		print "R click"
		time.sleep(2)
		
		win32api.SetCursorPos((x+140,y+140))
		print "prepare L click..."
		time.sleep(1) 
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x+140,y+140,0,0)
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x+140,y+140,0,0)
		print "sleet all"
		time.sleep(2)
		
		win32api.SetCursorPos((x,y))
		win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
		win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)
		print "R click"
		time.sleep(2)
		
		win32api.SetCursorPos((x+60,y+60))
		print "prepare L click..."
		time.sleep(1) 
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x+60,y+60,0,0)
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x+60,y+60,0,0)
		print "copy done!"
		time.sleep(2)
		
		win32api.SetCursorPos((x,y))
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
		win32api.SetCursorPos((x-60,y-60))
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
	
	
- not work for select all->copy by pymouse

		m = PyMouse()
		#m.position()#获取当前坐标的位置
		m.move(x,y)
		m.click(x,y,2) #右键
		print "R click"
		time.sleep(4) 
		m.click(x,y,3)
		
		m.move(x+140,y+140)
		print "prepare L click..."
		time.sleep(4)
		m.click(x,y,1) #左键
		#m.click(x,y,1) #左键
		#m.click(x,y,1) #左键
		print "select all,done"
		#time.sleep(4) 
		
		m.move(x-150,y-150)
		m.click(x-150,y-150,1)
		
		m.move(x,y)
		m.click(x,y,2) #右键
		print "R click"
		#time.sleep(4) 
	

- not work for send key envent

		##not work for ctrl+a -> ctrl+c
	
		win32api.PostMessage(0x000506c0, win32con.WM_KEYDOWN, win32con.VK_CONTROL, 0)
		win32api.PostMessage(0x000506c0, win32con.WM_KEYDOWN, VK_CODE['a'], 0) #a
		time.sleep(0.2)
		win32api.PostMessage(0x000506c0, win32con.WM_KEYUP, VK_CODE['a'], 0)
		win32api.PostMessage(0x000506c0, win32con.WM_KEYUP, win32con.VK_CONTROL, 0)

- pymouse

		#not work
	
		mouse=PyMouse()
		mouse.position()  #获取当前坐标的位置
		mouse.move(x,y)  #鼠标移动到(x,y)位置
		mouse.click(x,y)  #移动并且在(x,y)位置点击
		#1: left, 2: middle???, 3: right
		mouse.click(x,y,2) #移动并且在(x,y)位置点击,右键
		print "right click, done"