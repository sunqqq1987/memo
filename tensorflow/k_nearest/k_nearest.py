import numpy as np
import tensorflow as tf

from tensorflow.examples.tutorials.mnist import input_data

# 解决编译时的warnning问题
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# 导入MNIST数据集
mnist = input_data.read_data_sets("../MNIST_data/", one_hot=True)  # one_hot表示一个数据张量中只有一个1，其他都是0

# 对MNIST数据集做数量限制
Xtrain, Ytrain = mnist.train.next_batch(5000)  # 5000是训练样本,这些样本的分类信息保存在Ytrain中，Ytrain,Ytest都是1X10的向量
Xtest, Ytest = mnist.test.next_batch(200)  # 200是测试样本，它的真实的分类信息保存在Ytest中
print('Xtrain.shape:', Xtrain.shape, ',Xtest.shape', Xtest.shape)
print('Ytrain.shape:', Ytrain.shape, ',Ytest.shape', Ytest.shape)

# 计算图输入占位符
xtrain = tf.placeholder("float", [None, 784])  # xtrain 是个列宽为784的不定维向量
xtest = tf.placeholder("float", [784])  # xtest是个行向量，列宽是784

# 使用L1距离进行最近邻计算。
# reduce_sum()是缩减求和，axis=1表示将当前测试样本与5000个训练样本的距离张量，分别沿着各自张量的方向axis，缩减为1列
distance = tf.reduce_sum(tf.abs(tf.add(xtrain, tf.negative(xtest))), axis=1)

# 预测：获得测试样本与训练样本有最小距离的训练样本的索引（根据最近邻的类标签进行判断）
pred = tf.arg_min(distance, 0)

# 使用最近邻分类器的准确率，用来判断给定的一条测试样本是否预测正确
accuracy = 0.

# 初始化节点
init = tf.global_variables_initializer()

# 启动会话
with tf.Session() as sess:
    sess.run(init)
    ntest = len(Xtest)  # 测试样本的数量
    # 在测试集上进行循环
    for i in range(ntest):

        # 获取当前测试样本的最近邻所对应的训练样本的索引
        kn_idx = sess.run(pred, feed_dict={xtrain: Xtrain, xtest: Xtest[i, :]})  # 每次只输入第i个测试样本

        # 获得最近邻预测标签，然后与该测试样本的真实的类标签比较
        # 因为Ytrain,Ytest都是1X10的one_hot向量,所以用argmax返回最大数的索引后比较
        pred_class_label = np.argmax(Ytrain[kn_idx])  # Ytrain[kn_idx]是预测到的对应训练样本的分类
        true_class_label = np.argmax(Ytest[i])  # Ytest[i]是第i个测试样本的真实分类
        print("test", i, "pred_class_label:", pred_class_label,
              "true_class_label:", true_class_label)

        # 计算准确率
        if pred_class_label == true_class_label:
            accuracy += 1

    print("done")
    accuracy /= ntest
    print("Accuracy:", accuracy)

