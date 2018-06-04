# SoftMax Regression分类器 #

- [视频1](http://v.youku.com/v_show/id_XMjczMDMyOTg0OA==.html?spm=a2h0j.8191423.playlist_content.5!14~5~5~A&&f=49399706&from=y1.2-3.4.14)

<img src="./pic_SoftMax_R/10.jpg" width= 600><br><br><br>
<img src="./pic_SoftMax_R/11.jpg" width= 600><br><br><br>
<img src="./pic_SoftMax_R/12.jpg" width= 800><br><br><br>
<img src="./pic_SoftMax_R/13.jpg" width= 700><br><br><br>
	
	注意：以下图中，行\列是反的

<img src="./pic_SoftMax_R/14.jpg" width= 700><br><br><br>
<img src="./pic_SoftMax_R/15.jpg" width= 700><br><br><br>
<img src="./pic_SoftMax_R/16.jpg" width= 700><br><br><br>
<img src="./pic_SoftMax_R/17.jpg" width= 700><br><br><br>

	evidence_i是输入样本图片x是数字i的证据（或者说是概率），而evidence就是输入样本图片为各个数字的概率
	W_ij是图片x的第j个像素值x_j的权重（比如像素i对于判断图片x是数字i更有利，则该点处的权重更大）
	b_i代表图片x是数字i的偏置，目的是去掉输入本身的干扰

<img src="./pic_SoftMax_R/1.jpg" width= 800><br><br><br>
<img src="./pic_SoftMax_R/2.jpg" width= 800><br><br><br>
<img src="./pic_SoftMax_R/20.jpg" width= 200><br><br><br>
<img src="./pic_SoftMax_R/3.jpg" width= 700><br><br><br>
<img src="./pic_SoftMax_R/4.jpg" width= 700><br><br><br>
<img src="./pic_SoftMax_R/5.jpg" width= 800><br><br><br>
<img src="./pic_SoftMax_R/6.jpg" width= 800><br><br><br>

- **mnist实例**

[视频2](http://v.youku.com/v_show/id_XMjczMDM1ODMyNA==.html?spm=a2h0j.8191423.playlist_content.5!15~5~5~A&&f=49399706&from=y1.2-3.4.15)

<img src="./pic_SoftMax_R/1_1.jpg" width= 700><br><br><br>
<img src="./pic_SoftMax_R/1_2.jpg" width= 700><br><br><br>
<img src="./pic_SoftMax_R/1_3.jpg" width= 500><br><br><br>
	
**在tensorboard 1.2.1中，启动tensorbloard的查看log的命令如下**：

	1) 在pycharm的terminal中运行： tensorboard --logdir=logs/mnist_softmax
	2）在chrome浏览器中运行1中生成地址：http://NWD00P5OFU02K0G:6006  即可查看计算图
	
<img src="./pic_SoftMax_R/1_4.jpg" width= 700><br><br><br>
<img src="./pic_SoftMax_R/1_5.jpg" width= 600><br><br><br>
<img src="./pic_SoftMax_R/1_6.jpg" width= 700><br><br><br>
<img src="./pic_SoftMax_R/1_7_1.jpg" width= 500><br><br><br>
<img src="./pic_SoftMax_R/1_7.jpg" width= 700><br><br><br>
<img src="./pic_SoftMax_R/1_8.jpg" width= 700><br><br><br>
<img src="./pic_SoftMax_R/1_9.jpg" width= 700><br><br><br>
<img src="./pic_SoftMax_R/1_10.jpg" width= 500><br><br><br>
<img src="./pic_SoftMax_R/1_11.jpg" width= 700><br><br><br>