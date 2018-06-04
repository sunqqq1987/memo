
# 资源 #
	
- 极客学院
	
		http://wiki.jikexueyuan.com/project/tensorflow-zh/get_started/basic_usage.html

- blog

		1) http://blog.csdn.net/akadiao/article/category/7212456
	
# TF环境搭建 #

	TF官网安装guide: https://www.tensorflow.org/install/
	stackoverflow上： https://stackoverflow.com/questions/tagged/tensorflow

- 1) ubuntu上安装Virtualenv

		1）sudo apt-get install python3-pip python3-dev python-virtualenv # for Python 3.n

		2）virtualenv --system-site-packages -p python3 <targetDirectory> # for Python 3.n
		=> targetDirectory 是自己主目录下的某个文件夹，如：~/tools/tensorflow

		3) source ~/tools/tensorflow/bin/activate
		=> 激活虚拟环境. 之后就可以进行各种pip安装软件了
		
		4）安装 pip 8.1 或更高版本
		(tensorflow)$ easy_install -U pip

		5）安装 TensorFlow
		(tensorflow)$ pip3 install --upgrade tensorflow     # for Python 3.n
		(tensorflow)$ pip3 install --upgrade tensorflow-gpu # for Python 3.n and GPU
		
		6) 如果要关闭上述虚拟环境，执行：
		(env)$ deactivate
		
- 2) 安装Anaconda

	以下是windows上安装方式，linux也有相应的安装方法，见官网
	
	- (1) 可以从官网下载，但是从 https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/ 下载更快,
	
		版本为：Anaconda3-5.0.1-Windows-x86_64.exe 
	
	- (2) 更换为阿里云pip源. 目的是为了在国内获取更快的下载速度。
	
	- (3) 之后按以下为tensorflow设置一个运行环境：
	
			conda info --envs # 查看conda的env
			conda create --name tfenv python==3.6.3 # 创建conda env，python版本为3.6.3 
													(最好从anaconda官网上查看支持的python版本)
			activate tfenv # 激活env
		
	- (4) 在tfenv下安装tesorflow
	
		- 先查看可以下载的tf安装包：conda search tensorflow, 也可以用pip search
	
				(tensorflow_env) C:\Users\Administrator>pip search tensorflow
				Fetching package metadata .............
				r-tensorflow                 0.8.2                  r3.4.1_0  defaults
				                             1.4              r342h0bf44f9_0  defaults
				tensorflow                   1.1.0               np112py35_0  defaults
				                             1.1.0               np112py36_0  defaults
				                             1.2.1                    py35_0  defaults
				                          *  1.2.1                    py36_0  defaults
				tensorflow-gpu               1.1.0               np112py35_0  defaults
				                             1.1.0               np112py36_0  defaults
	
		- 选择cpu版的1.2.1安装：pip install tensorflow==1.2.1
		
		- 最后查看当前环境下已安装的包：conda list
	
	- (5) pip升级tensorflow

			pip3 install --upgrade tensorflow --trusted-host pypi.python.org --proxy=http://IP:PORT
			=> 使用proxy并消除SSL错误

- 3) 安装pycharm

	- 在官网下载pycharm-professional-2017.3.3.exe 或 2018版pycharm
	
	- pycharm激活
	
			参考： https://www.cnblogs.com/-nbloser/p/8570648.html

			1）要先修改hosts文件:

			Windows文件位置：C:\Windows\System32\drivers\etc
			Linux和mac的hosts文件路径为：/etc
			在文件末尾添加：0.0.0.0 account.jetbrains.com

			2）然后输入激活码
			页可以从 http://idea.lanyus.com/ 获得激活码
	
	- linux上安装pycharm
	
			1) tar -xzf pycharm-2018.1.tar.gz 
			2) Run pycharm.sh from the bin subdirectory
	
	- 启动pycharm后将新建工程的python解析器指定为tf的环境目录
	
			C:\ProgramData\Anaconda3\envs\tensorflow_env	

# Tensorboard #

- 资料
	
		官方：https://www.tensorflow.org/programmers_guide/tensorboard_histograms

- 启动tensorbloard, 查看logs文件夹下的事件

		1) 在pycharm的terminal中运行： tensorboard --logdir="logs/"
		2）在chrome浏览器中运行1中生成地址, 如 http://NWD00P5OFU02K0G:6006，即可查看计算图

- tf.summary.histogram直方图

		以正太分布为例：参考 http://blog.csdn.net/akadiao/article/details/79551180
		1）offset模式
		
		其中，横轴表示值，纵轴表示数量，每个切片显示一个直方图，切片按步骤（步数或时间）排列；
		旧的切片较暗，新的切片颜色较浅．
		如图，可以看到在第393步时，以4.91为中心的bin中有161个元素． 
		另外，直方图切片并不总是按步数或时间均匀分布，而是通过水塘抽样reservoir sampling来抽取所有直方图的一个子集，以节省内存．
		
		2）OVERLAY模式

		其中，横轴表示值，纵轴表示某步时的数量．
		各个直方图切片不再展开，而是全部绘制在相同的y轴上．这样不同的线表示不同的步骤（步数或时间）
		如图，可以看到在第5步时，以0.11为中心的bin中有183个元素． 
		OVERLAY模式用于直接比较不同直方图的计数．


# TF Lite #

- 官方资料

		1)官方：https://www.tensorflow.org/mobile/

		2) lite demo: 
		\tensorflow\tensorflow\contrib\lite\java\demo

		guide: https://www.tensorflow.org/mobile/tflite/demo_android
		
		GITHUB上的readme:
		https://github.com/tensorflow/tensorflow/tree/master/tensorflow/contrib/lite#building-tensorflow-lite-and-the-demo-app-from-source

		TensorFlow Android Camera Demo: 
		\tensorflow\tensorflow\examples\android

- 模型转换

		参考：
		https://github.com/tensorflow/tensorflow/tree/master/tensorflow/contrib/lite
		-> README.md -> Step 2. Model format conversion

		https://www.tensorflow.org/mobile/tflite/devguide
		-> Convert the model format

		方式有2种：
		1）先用bazel将pb和ckpt文件转换为frozen的pb文件，然后调用buzel生成TFLITE格式
		Here is a sample command line to convert the frozen Graphdef to '.tflite' format 
		for The Tensorflow Optimizing Converter supports both float and quantized models, 
		however, different configuration parameters are needed depending on whether a FLOAT 
		or QUANTIZED mode is being used. (Here is a link to the pb file).

		- 如何导出.pb/ckpt/frozen pb文件
				
				https://blog.csdn.net/sinat_29957455/article/details/78511119
				https://github.com/tensorflow/models/blob/master/research/slim/export_inference_graph.py

		- 怎么使用frozen pb：
		
				https://blog.csdn.net/tengxing007/article/details/55671018

		
		2）用python代码转换

		python api参考：
		https://github.com/tensorflow/tensorflow/blob/master/tensorflow/contrib/lite/toco/g3doc/python_api.md

		it is also possible to use the Tensorflow Optimizing Converter through protos 
		either from Python or from the command line see the documentation here. 
		A developer can then integrate the conversion step into their model design workflow 
		to ensure that a model will be easily convertible to a mobile inference graph. 
		For example,

			import tensorflow as tf
	
			img = tf.placeholder(name="img", dtype=tf.float32, shape=(1, 64, 64, 3))
			val = img + tf.constant([1., 2., 3.]) + tf.constant([1., 4., 4.])
			out = tf.identity(val, name="out")
			with tf.Session() as sess:
			  tflite_model = tf.contrib.lite.toco_convert(sess.graph_def, [img], [out])
			  open("converteds_model.tflite", "wb").write(tflite_model)
	
		Tensorflow Optimizing Converter(TOCO) tool 使用方法见：
		https://github.com/tensorflow/tensorflow/blob/master/tensorflow/contrib/lite/toco/g3doc/cmdline_examples.md

- andorid app使用tflite模型

		Because Android apps need to be written in Java, and core TensorFlow is in C++, 
		a JNI library is provided to interface between the two. 
		Its interface is aimed only at inference.

		使用方法参考：https://github.com/tensorflow/tensorflow/tree/master/tensorflow/contrib/lite/g3doc


# TF 语法 #

- 经验

	- 1）在计算图中，涉及到常量的函数，都必须用常量，不能是变量。
	
			x = tf.constant(list_of_points1_[0], shape=(1, 2)) //list_of_points1_ 必须是const array

	- 2）将定义计算图和运行计算图的过程分离，这样才有利于明确输入和输出
		
			参考： https://blog.csdn.net/u014432647/article/details/75276718
			形如：
			# 定义计算图
			def build_graph(height, width): 
				...
				x_input = tf.placeholder(tf.float32, [1, height, width, 1], name="x_input")
				...
				return dict(x_input=x_input, output=ouput)
	
			# 运行计算图
			def train_graph(graph):
				init = tf.global_variables_initializer()
			    with tf.Session() as sess:
			        writer = tf.summary.FileWriter("logs/", sess.graph)
			        sess.run(init)
					...
					feed_dict = {
	                    graph['x_input']: x
	                }
	                r = sess.run(graph['ouput'], feed_dict)
					...
				writer.close()
				
				#输出tflite
				tflite_model = tf.contrib.lite.toco_convert(sess.graph_def, [graph['x_input']], [graph['r']])
	       		open("converted_model.tflite", "wb").write(tflite_model)
			
			# 入口
			g = build_graph(height, width)
			run_graph(g)

	- 3) 直接生成tflite时，输入参数的维度必须是固定的，即常数，否则toco_convert()时会报错

	- 4）placeholder的维度不需固定
	
	- 5) 当调用 get_tensor_by_name()获取pb中的tensor却提示找不到，
	
		需要在转换模型的时候，在convert_variables_to_constants()加上输出的张量名
	
	- 6）计算图中不要使用类似数组方式的索引，改用tf.gather()类函数，否则生成不了pb文件
	

- 打印计算图中的变量

		https://blog.csdn.net/shwan_ma/article/details/78879620

		方式1：
		print("variables:")
        variable_names = [v.name for v in tf.trainable_variables()]
        values = sess.run(variable_names)
        for k, v in zip(variable_names, values):
            print("Variable: ", k)
            print("Shape: ", v.shape)
            print(v)

		方式2：
		print("trainable_variables:")
	    variable_names = [c.name for c in tf.trainable_variables()]
	    print(variable_names)
		
- 计算图的理解

		https://blog.csdn.net/qian99/article/details/70500166

- Tensor数据相关的运算及函数讲解

		https://blog.csdn.net/wyl1987527/article/details/62458057

	- Tensor 和 numpy array互转

			1) numpy array 到 Tensor

			numpyData = np.zeros((1,10,10,3),dtype=np.float32)
			tf.convert_to_tensor(numpyData)
			
			2) Tensor到 numpy array
			
			eval()
			tf.constant([1,2,3]).eval()


- 变量的初始化方式

		https://www.cnblogs.com/tengge/p/6360971.html

- 变量常量类型

		https://blog.csdn.net/xierhacker/article/details/53103979

- tensorflow函数与numpy函数的选择

		https://blog.csdn.net/abiggg/article/details/79054518

		tensorflow的计算一般可分成两个阶段：
			第一阶段，定义所有的计算过程，即计算流图。在这个阶段，所有的变量均无实际参数值，仅仅表示一个计算过程；
			第二阶段，执行运算，创建会话（Session)，此时才会对变量进行赋值；
		而numpy的计算，会直接对具体的参数值进行运算。
		因此，在tensoflow的第一阶段，表示计算过程时，必段选用tensorflow的函数；
		而在第二阶段，或者对已有具体参数值进行运算时，则需选择numpy。

- convert_variables_to_constants()

		https://blog.csdn.net/sinat_29957455/article/details/78511119

- feed_dict

		https://blog.csdn.net/pianzang5201/article/details/78661465

		import tensorflow as tf  
  
		#设置两个乘数，用占位符表示  
		input1 = tf.placeholder(tf.float32)  
		input2 = tf.placeholder(tf.float32)  
		#设置乘积  
		output = tf.multiply(input1, input2)  
		  
		with tf.Session() as sess:  
		    #用feed_dict以字典的方式填充占位  
		    print(sess.run(output, feed_dict={input1:[8.],input2:[2.]}))  

		=> [ 16.]

- 图像处理

	- 实例
		
		Tensorflow学习笔记之存取图像文件：
		https://blog.csdn.net/index20001/article/details/73843070
		
		Tensorflow中图像处理函数(图像大小调整)：
		https://blog.csdn.net/zsean/article/details/76383100
		
		https://www.cnblogs.com/polly333/p/7481685.html

		TensorFlow与OpenCV，读取图片，进行简单操作并显示
		https://blog.csdn.net/helei001/article/details/52400497

- 优化器optimizer

		# 创建一个optimizer.  
		opt = GradientDescentOptimizer(learning_rate=0.1)  
		
		# 计算<list of variables>相关的梯度  
		# grads_and_vars为tuples (gradient, variable)组成的列表。 
		grads_and_vars = opt.compute_gradients(loss, <list of variables>)  
		  
		#对梯度进行想要的处理，比如cap处理  
		capped_grads_and_vars = [(MyCapper(gv[0]), gv[1]) for gv in grads_and_vars]  
		  
		# 令optimizer运用capped的梯度(gradients)  
		opt.apply_gradients(capped_grads_and_vars)

- tf.pad()

		https://blog.csdn.net/zhang_bei_qing/article/details/75090203

- tf.argmax()

		返回沿着某个维度最大值的下标
		argmax(self, axis=None, fill_value=None, out=None)

		a = np.arange(6).reshape(2,3)
		print(a)
		=>
		[[0 1 2]
 		[3 4 5]]

		print(a.argmax()) # 不指明维度参数时，按扁平化后处理（即一维）
		=> 5
		print(a.argmax(0)) # axis=0 按行方向找 
		=> [1 1 1]
		print(a.argmax(1)) # axis=1 按列方向找
		=> [2 2]

- collection

		tensorflow的collection提供一个全局的存储机制，不会受到变量名生存空间的影响。一处保存，到处可取。
		
		tf.add_to_collection：把变量放入一个集合，把很多变量变成一个列表
		tf.get_collection：从一个结合中取出全部变量，是一个列表
		tf.add_n：把一个列表的东西都依次加起来

		实例：
		v1 = tf.get_variable(name='v1', shape=[1], initializer=tf.constant_initializer(0))  
		tf.add_to_collection('loss', v1)  
		v2 = tf.get_variable(name='v2', shape=[1], initializer=tf.constant_initializer(2))  
		tf.add_to_collection('loss', v2)  
		  
		with tf.Session() as sess:  
		    sess.run(tf.initialize_all_variables())  
		    print tf.get_collection('loss')  
			=>
			[<tensorflow.python.ops.variables.Variable object at 0x7f6b5d700c50>, <tensorflow.python.ops.variables.Variable object at 0x7f6b5d700c90>]

		    print sess.run(tf.add_n(tf.get_collection('loss')))
			=> [ 2.]

- 正则化

		一般可以通过减少特征或者惩罚不重要特征的权重来缓解过拟合，但是我们通常不知道该惩罚那些特征的权重，
		而正则化就是帮助我们惩罚特征权重的，即特征的权重也会成为模型的损失函数一部分。
		可以理解为，为了使用某个特征，我们需要付出loss的代价（loss为给权重weight加的一个loss，正则化），
		除非这个特征非常有效，否贼就会被loss上的增加覆盖效果。这样我们就能筛选出最有效的特征，减少特征权重防止过拟合。
		
		一般来说，L1正则会制造稀疏的特征，大部分无用特征的权重会被至为0,
		L2正则会让特征的权重不过大，使得特征的权重比较平均。       
		tensorflow.nn.l2_loss(weight) 就是计算weight的L2 loss
		
		实例：
	
		weights = tf.constant([[1., -2.], [-3., 4.]])
		with tf.Session() as sess:
			print(sess.run(tf.contrib.layers.l1_regularizer(.5)(weights)))
			# (1+2+3+4)*.5 ⇒ 5
			print(sess.run(tf.contrib.layers.l2_regularizer(.5)(weights)))
			# (1+4+9+16)*.5*.5 ⇒ 7.5

- tf.nn.relu

		ReLU是线性修正，公式为：g(x) = max(0, x),
    	它的作用是如果计算出的值小于0，就让它等于0，否则保持原来的值不变.

		a = tf.constant([-1.0, 2.0, 3.0])
		with tf.Session() as sess:
		    b = tf.nn.relu(a)
		    print(sess.run(b))
		==> [ 0.  2.  3.]

		其他激励函数：
		http://blog.csdn.net/DaVinciL/article/details/75313391

- softmax
		
		softmax模型可以用来给不同的对象分配概率.
		它会正则化这些权重值，使它们的总和等于1，以此构造一个有效的概率分布

- tf.random_normal与tf.truncated_normal的区别

		1）tf.truncated_normal使用方法

		tf.truncated_normal(shape, mean=0.0, stddev=1.0, dtype=tf.float32, seed=None, name=None)
		
		从截断的正态分布中输出随机值。 
		生成的值服从具有指定平均值mean和标准偏差stddev的正态分布，如果生成的值大于平均值2个标准偏差的值则丢弃重新选择。
		
		在正态分布的曲线中，横轴区间（μ-σ，μ+σ）内的面积为68.268949%。 
		横轴区间（μ-2σ，μ+2σ）内的面积为95.449974%。 
		横轴区间（μ-3σ，μ+3σ）内的面积为99.730020%。 
		X落在（μ-3σ，μ+3σ）以外的概率小于千分之三，在实际问题中常认为相应的事件是不会发生的，基本上可以把区间（μ-3σ，μ+3σ）看作是随机变量X实际可能的取值区间，这称之为正态分布的“3σ”原则。 
		在tf.truncated_normal中如果x的取值在区间（μ-2σ，μ+2σ）之外则重新进行选择。这样保证了生成的值都在均值附近。
		
		参数:
		
		    shape: 一维的张量，也是输出的张量。
		    mean: 正态分布的均值。 
		    stddev: 正态分布的标准差。
		    dtype: 输出的类型。
		    seed: 一个整数，当设置之后，每次生成的随机数都一样。
		    name: 操作的名字
		
		2）tf.random_normal使用方法
		
		tf.random_normal(shape, mean=0.0, stddev=1.0, dtype=tf.float32, seed=None, name=None)
		
		从正态分布中输出随机值。
		参数:
		
		    shape: 一维的张量，也是输出的张量。
		    mean: 正态分布的均值。
		    stddev: 正态分布的标准差。
		    dtype: 输出的类型。
		    seed: 一个整数，当设置之后，每次生成的随机数都一样。
		    name: 操作的名字。
		
		代码
		
		a = tf.Variable(tf.random_normal([2,2],seed=1))
		b = tf.Variable(tf.truncated_normal([2,2],seed=2))
		init = tf.global_variables_initializer()
		with tf.Session() as sess:
		    sess.run(init)
		    print(sess.run(a))
		    print(sess.run(b))
		
		输出：
		[[-0.81131822  1.48459876]
		 [ 0.06532937 -2.44270396]]
		[[-0.85811085 -0.19662298]

- embedding_lookup

		简单的讲就是根据input_ids中的id，寻找embedding中的对应元素，比如，input_ids=[1,3,5]，
		则找出embedding中下标为1,3,5的行向量组成一个矩阵返回。

		实例：
		
		# 使用palceholder定义了一个未知变量input_ids用于存储索引，和一个已知变量embedding(一个5*5的对角矩阵)
		input_ids = tf.placeholder(dtype=tf.int32, shape=[None])
		embedding = tf.Variable(np.identity(5, dtype=np.int32))

		input_embedding = tf.nn.embedding_lookup(embedding, input_ids)
		
		sess = tf.InteractiveSession()
		sess.run(tf.global_variables_initializer())
		print(embedding.eval())
		=>
		embedding = [[1 0 0 0 0]
             [0 1 0 0 0]
             [0 0 1 0 0]
             [0 0 0 1 0]
             [0 0 0 0 1]]

		print(sess.run(input_embedding, feed_dict={input_ids:[1, 2, 3, 0, 3, 2, 1]}))
		=>
		input_embedding = [[0 1 0 0 0]
                   [0 0 1 0 0]
                   [0 0 0 1 0]
                   [1 0 0 0 0]
                   [0 0 0 1 0]
                   [0 0 1 0 0]
                   [0 1 0 0 0]]

- tf.concat()矩阵连接
	
		tf.concat(concat_dim, values, name='concat') 是连接两个矩阵的操作
		=> 注意，最新版本的tesorflow, 第一个参数和第二个参数位置互换了。
	
		第一个参数concat_dim：必须是一个数，表明在哪一维上连接，
		第二个参数values：就是两个或者一组待连接的tensor了

		实例：

		如果concat_dim是0，那么第一个维度上连接，也就是行合并
			t1 = [[1, 2, 3], [4, 5, 6]]  
			t2 = [[7, 8, 9], [10, 11, 12]]  
			tf.concat(0, [t1, t2]) 
			=> 
			[[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]] 

		如果concat_dim是1，那么在第二个维度上连接，也就是列合并
			t1 = [[1, 2, 3], [4, 5, 6]]  
			t2 = [[7, 8, 9], [10, 11, 12]]  
			tf.concat(1, [t1, t2]) 
			=> 
			[[1, 2, 3, 7, 8, 9], [4, 5, 6, 10, 11, 12]]
		
		参考：http://blog.csdn.net/mao_xiao_feng/article/details/53366163

- tf.gather()

		https://blog.csdn.net/Cyiano/article/details/76087747

		类似于数组的索引，可以把向量中某些索引值提取出来，得到新的向量，适用于要提取的索引为不连续的情况。这个函数只适合在一维的情况下使用。
		
		import tensorflow as tf 

		a = tf.Variable([[1,2,3,4,5], [6,7,8,9,10], [11,12,13,14,15]])
		index_a = tf.Variable([0,2])
		
		b = tf.Variable([1,2,3,4,5,6,7,8,9,10])
		index_b = tf.Variable([2,4,6,8])
		
		with tf.Session() as sess:
		    sess.run(tf.global_variables_initializer())
		    print(sess.run(tf.gather(a, index_a)))
		    print(sess.run(tf.gather(b, index_b)))
		
		#  [[ 1  2  3  4  5]
		#   [11 12 13 14 15]]
		
		#  [3 5 7 9]

- tf.gather_nd()

		允许在多维上进行索引，例子只展示了一种很简单的用法，更复杂的用法可见官网
		
		import tensorflow as tf 

		a = tf.Variable([[1,2,3,4,5], [6,7,8,9,10], [11,12,13,14,15]])
		index_a = tf.Variable([[0,2], [0,4], [2,2]])
		
		with tf.Session() as sess:
		    sess.run(tf.global_variables_initializer())
		    print(sess.run(tf.gather_nd(a, index_a)))
		
		#  [ 3  5 13]


- tf.slice()

		https://blog.csdn.net/chenxieyy/article/details/53031943

		函数原型 tf.slice(inputs,begin,size,name='')
		用途：从inputs中抽取部分内容
		inputs：可以是list,array,tensor
		begin：n维列表，begin[i] 表示从inputs中第i维抽取数据时，相对0的起始偏移量，也就是从第i维的begin[i]开始抽取数据
		size：n维列表，size[i]表示要抽取的第i维元素的数目

		import tensorflow as tf  
		import numpy as np  
		x=[[1,2,3],[4,5,6]]  
		y=np.arange(24).reshape([2,3,4])  
		z=tf.constant([[[1,2,3],[4,5,6]], [[7,8,9],[10,11,12]],  [[13,14,15],[16,17,18]]]  
		sess=tf.Session()  
		begin_x=[1,0]        #第一个1，决定了从x的第二行[4,5,6]开始，第二个0，决定了从[4,5,6] 中的4开始抽取  
		size_x=[1,2]         # 第一个1决定了，从第二行以起始位置抽取1行，也就是只抽取[4,5,6] 这一行，在这一行中从4开始抽取2个元素  
		out=tf.slice(x,begin_x,size_x)  
		print sess.run(out)  #  结果:[[4 5]]  

		例子2：
		f = tf.Variable([1, 2, 3, 4])
		idx_beg = tf.Variable([0])
		idx_size = tf.Variable([3])
		ff = tf.slice(f, idx_beg, idx_size)
		print("ff,", ff)

- tf.reshape()
		
		tf.reshape(tensor, shape, name=None) 
		函数的作用是将tensor变换为参数shape的形式。 
		其中shape为一个列表形式，特殊的一点是列表中可以存在-1。
		-1代表不用我们自己指定这一维的大小，函数会自动计算，但列表中只能存在一个-1。
		（当然如果存在多个-1，就是一个存在多解的方程了）
		
		实例：
		
		# tensor 't' is [1, 2, 3, 4, 5, 6, 7, 8, 9]
		# tensor 't' has shape [9]
		reshape(t, [3, 3]) ==> [[1, 2, 3],
		                        [4, 5, 6],
		                        [7, 8, 9]]
		
		# tensor 't' is [[[1, 1], [2, 2]],
		#                [[3, 3], [4, 4]]]
		# tensor 't' has shape [2, 2, 2]
		reshape(t, [2, 4]) ==> [[1, 1, 2, 2],
		                        [3, 3, 4, 4]]
		
		# tensor 't' is [[[1, 1, 1],
		#                 [2, 2, 2]],
		#                [[3, 3, 3],
		#                 [4, 4, 4]],
		#                [[5, 5, 5],
		#                 [6, 6, 6]]]
		# tensor 't' has shape [3, 2, 3]
		# pass '[-1]' to flatten 't'
		reshape(t, [-1]) ==> [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6]
		
		# -1 can also be used to infer the shape
		
		# -1 is inferred to be 9:
		reshape(t, [2, -1]) ==> [[1, 1, 1, 2, 2, 2, 3, 3, 3],
		                         [4, 4, 4, 5, 5, 5, 6, 6, 6]]
		# -1 is inferred to be 2:
		reshape(t, [-1, 9]) ==> [[1, 1, 1, 2, 2, 2, 3, 3, 3],
		                         [4, 4, 4, 5, 5, 5, 6, 6, 6]]
		# -1 is inferred to be 3:
		reshape(t, [ 2, -1, 3]) ==> [[[1, 1, 1],
		                              [2, 2, 2],
		                              [3, 3, 3]],
		                             [[4, 4, 4],
		                              [5, 5, 5],
		                              [6, 6, 6]]]
		
		# tensor 't' is [7]
		# shape `[]` reshapes to a scalar
		reshape(t, []) ==> 7

		http://blog.csdn.net/lxg0807/article/details/53021859

- tf.dropout()

		tf.nn.dropout是TensorFlow里面为了防止或减轻过拟合而使用的函数，它一般用在全连接层。

		Dropout就是在不同的训练过程中随机扔掉一部分神经元。也就是让某个神经元的激活值以一定的概率p，让其停止工作，
		这次训练过程中不更新权值，也不参加神经网络的计算。
		但是它的权重得保留下来（只是暂时不更新而已），因为下次样本输入时它可能又得工作了。

		tf.nn.dropout(x, keep_prob, noise_shape=None, seed=None,name=None) 
		第一个参数x：指输入
		第二个参数keep_prob: 设置神经元被选中的概率,在初始化时keep_prob是一个占位符,  keep_prob = tf.placeholder(tf.float32) 。
		tensorflow在run时设置keep_prob具体的值，例如keep_prob: 0.5
		第五个参数name：指定该操作的名字。

		http://blog.csdn.net/huahuazhu/article/details/73649389

- tf.nn.conv2d()卷积
	
		参考：http://blog.csdn.net/mao_xiao_feng/article/details/78004522

		tf.nn.conv2d(input, filter, strides, padding, use_cudnn_on_gpu=None, name=None)
			input:  输入数据,[batch（可以理解为图片数), height（图高), width(图宽), in_channels(图片的输入通道数)]
			filter: 卷积核W,[height(卷积核高度），width（卷积核宽度），in_channels(图片的输入通道数)，out_channels（卷积核个数，输出通道数）]
			strides: 卷积时在图像每一维上的步长,一维向量，长度为4，图像通常为[1, x, x, 1]
			padding: 卷积方式，'SAME'为等长卷积, 'VALID'为窄卷积
			输出一个feature map：shape是[batch, height, width, out_channels]，表示batch张out_channels个[height_x, width_x]的图片
			这里[height_x, width_x]是卷积步长的影响。


# TF issues #

- 1）运行时总是显示warning信息

	加入以下2行：

	    import os
	    os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

- 2）name 'tempfile' is not defined

	tf版本<=1.7, workaround: 加入以下行

		import tempfile
		import subprocess
		
		tf.contrib.lite.tempfile = tempfile
		tf.contrib.lite.subprocess = subprocess


# 卷积神经网络CNN #

	例如，经常发生的，当你的训练数据不足的时候，参数又太多，你就可能训练不出来。一个非常简单的例子，大家可以想象 N 元的一个方程组，
	然后我们假设只有 N 个数据，并且这些数据是完全可分的，也就是我们是可以完全求解。但完全求解可能会导致过拟合，
	因为训练数据在真实环境下都是有噪音的，也就是没有办法做到完全避免随机因素的影响。在这种情况下如果你过于贴合训练数据，
	那么就有可能没有办法去收敛到未知的数据。

	所以这就是参数过多可能引发的问题，即过拟合和训练不出来。那怎样去解决这两个问题呢？卷积神经网络就是一个很好的方法。

	http://blog.csdn.net/xiangz_csdn/article/details/68060321
	
- cnn-text-classification-tf代码分析
		
		英文CNN分类： eng-text-classification-cnn
		https://www.cnblogs.com/wilde/p/8353639.html
		http://lib.csdn.net/article/aiframework/67084?knId=1756

		中文文本CNN分类： chn-text-classification-cnn-rnn
		https://github.com/gaussic/text-classification-cnn-rnn

		MNIST CNN:
		http://blog.csdn.net/akadiao/article/details/78366422


# Android Neural Networks API #

	https://developer.android.com/ndk/guides/neuralnetworks/index.html