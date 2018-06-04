
# numpy #

- numpy.concatenate

		a = np.array([[1, 2], [3, 4]])
		b = np.array([[5, 6]])
		np.concatenate((a, b), axis=0) # 按行方向拼接
		=>
		array([[1, 2],
		       [3, 4],
		       [5, 6]])

		np.concatenate((a, b), axis=1) # 按列方向拼接
		=>
		array([[1, 2, 5],
		       [3, 4, 6]])	

- 奇异值分解SVD

		https://www.cnblogs.com/tgycoder/p/6266786.html

- 方差var、协方差cov

		http://blog.csdn.net/maoersong/article/details/21823397

- 均值mean()

		num1 = numpy.array([[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]])
	    print(num1)
		=>
		[[1 2 3]
		 [2 3 4]
		 [3 4 5]
		 [4 5 6]]

	    print(numpy.mean(num1))  # 对所有元素求均值
		=> 3.5
	    print(numpy.mean(num1, 0))  # 压缩行，对各列求均值
		=> [ 2.5  3.5  4.5]
	    print(numpy.mean(num1, 1))  # 压缩列，对各行求均值	
		=> [ 2.  3.  4.  5.]

- 范围range()

		>>> c = [i for i in range(0,5)]     #从0 开始到4，不包括5，默认的间隔为1  
		>>> c  
		[0, 1, 2, 3, 4]  
		>>> c = [i for i in range(0,5,2)]   #间隔设为2  
		>>> c  
		[0, 2, 4]  	

- 随机函数shuffle与permutation的区别

		函数shuffle与permutation都是对原来的数组进行重新洗牌（即随机打乱原来的元素顺序）；
		区别在于shuffle直接在原来的数组上进行操作，改变原来数组的顺序，无返回值。
		而permutation不直接在原来的数组上进行操作，而是返回一个新的打乱顺序的数组，并不改变原来的数组。

		a = np.arange(12)  
		print a  
		np.random.shuffle(a) 
		print a
		==>
		[ 0  1  2  3  4  5  6  7  8  9 10 11]  
		[11  6  4 10  3  0  7  1  9  2  5  8] 

		b = np.random.permutation(a)  
		print b  
		print a  
		==>  
		[10  4  8 11  1  7  6  2  0  9  5  3]  
		[ 0  1  2  3  4  5  6  7  8  9 10 11]  


- enumerate()

		用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中

		seq = ['one', 'two', 'three']
		for i, element in enumerate(seq, start=0):
		    print i, seq[i]
		=>
		0 one
		1 two
		2 three

- np.pad()
		
		将numpy数组按指定的方法填充成指定的形状
		https://blog.csdn.net/hustqb/article/details/77726660

		1) 一维数组填充
		import numpy as np
		arr1D = np.array([1, 1, 2, 2, 3, 4])

		print('constant:  ' + str(np.pad(arr1D, (2, 3), 'constant')))  # （2，3）表示数组的前面填充两个，后面填充三个，constant: 填充的数据是0
		print('edge:  ' + str(np.pad(arr1D, (2, 3), 'edge')))  # edge： 填充的数据是边缘值
		print('linear_ramp:  ' + str(np.pad(arr1D, (2, 3), 'linear_ramp')))  # linear_ramp： 边缘递减的填充方式
		print('maximum:  ' + str(np.pad(arr1D, (2, 3), 'maximum')))  # maximum, mean, median, minimum分别用最大值、均值、中位数和最小值填充
		print('mean:  ' + str(np.pad(arr1D, (2, 3), 'mean')))
		print('median:  ' + str(np.pad(arr1D, (2, 3), 'median')))
		print('minimum:  ' + str(np.pad(arr1D, (2, 3), 'minimum')))
		print('reflect:  ' + str(np.pad(arr1D, (2, 3), 'reflect')))  # reflect： 关于边缘对称填充
		print('symmetric:  ' + str(np.pad(arr1D, (2, 3), 'symmetric')))  # symmetric: 关于边缘外的空气对称
		print('wrap:  ' + str(np.pad(arr1D, (2, 3), 'wrap')))  # wrap：用原数组后面的值填充到前面，前面的值填充到后面

		=> 
		constant:  [0 0 1 1 2 2 3 4 0 0 0]
		edge:  [1 1 1 1 2 2 3 4 4 4 4]
		linear_ramp:  [0 0 1 1 2 2 3 4 3 1 0]
		maximum:  [4 4 1 1 2 2 3 4 4 4 4]
		mean:  [2 2 1 1 2 2 3 4 2 2 2]
		median:  [2 2 1 1 2 2 3 4 2 2 2]
		minimum:  [1 1 1 1 2 2 3 4 1 1 1]
		reflect:  [2 1 1 1 2 2 3 4 3 2 2]
		symmetric:  [1 1 1 1 2 2 3 4 4 3 2]
		wrap:  [3 4 1 1 2 2 3 4 1 1 2]


		print('constant3:  ' + str(np.pad(arr1D, (3), 'constant')))  # 数组的前后都填充3个0
		print('constant03:  ' + str(np.pad(arr1D, (0,3), 'constant')))  # 仅仅数组的后面填充3个0
		=> 
		constant3:  [0 0 0 1 1 2 2 3 4 0 0 0]
		constant03:  [1 1 2 2 3 4 0 0 0]

- np.reshape

		numpy.reshape(a, newshape, order=’C’)
		
		参数
		a：array_like
		    要重新形成的数组。
		newshape：int或tuple的整数
		    新的形状应该与原始形状兼容。如果是整数，则结果将是该长度的1-D数组。一个形状维度可以是-1。在这种情况下，从数组的长度和其余维度推断该值。
		order：{'C'，'F'，'A'}可选
		    使用此索引顺序读取a的元素，并使用此索引顺序将元素放置到重新形成的数组中。'C'意味着使用C样索引顺序读取/写入元素，最后一个轴索引变化最快，回到第一个轴索引变化最慢。
			'F'意味着使用Fortran样索引顺序读取/写入元素，第一个索引变化最快，最后一个索引变化最慢。注意，'C'和'F'选项不考虑底层数组的内存布局，而只是参考索引的顺序。
			'A'意味着在Fortran类索引顺序中读/写元素，如果a 是Fortran 在内存中连续的，否则为C样顺序。

		注意：形状变化的原则是数组元素不能发生改变,否则会发生错误。 如：
		a = np.array([1,2,3,4,5,6])
		d = np.reshape(a, (2,3)  //=> ok
		d2 = np.reshpae(a,(2,2)) //==> 失败

- 数组切片和索引

		https://blog.csdn.net/qq_18433441/article/details/55805619
	
		1）一维数组

		b = np.array([1,2,3,4,5,6]) 
		c = b[:3]  # 只获取前3个元素。注意不包括索引为3的元素
		print(str(c))
		=> [1 2 3]
		