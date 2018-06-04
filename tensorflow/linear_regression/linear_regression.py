import numpy as np
import matplotlib.pyplot as plt

import os
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG-LEVEL'] = '2'


# 训练数据集
train_X = np.asarray([3.3, 4.4, 5.5, 6.71, 6.93, 4.168,9.779,6.182,7.59,2.167,
                      7.042,10.791,5.313,7.997,5.654,9.27,3.1])
train_Y = np.asarray([1.7,2.76,2.09,3.19,1.694,1.573,3.366,2.596,2.53,1.22,
                      2.827, 3.465,1.65,2.904,2.42,2.94,1.3])
n_train_samples = train_X.shape[0]

print('训练样本数量：', n_train_samples)


# 产生测试样本
test_X = np.asarray([6.83,4.688,8.9,7.91,5.7,8.7,3.1,2.1])
test_Y = np.asarray([1.84,2.273,3.2,2.831,2.92,3.24,1.35,1.03])
n_test_samples = test_X.shape[0]

print('测试样本数量：', n_test_samples)

# 展示原始数据分布
plt.plot(train_X, train_Y, 'ro', label='Original Train Points')
plt.plot(test_X, test_Y, 'b*', label='Original Test Points')
plt.legend()
plt.show()

with tf.Graph().as_default():
    # 定义输入节点：
    with tf.name_scope('Input'):
        X = tf.placeholder(tf.float32, name='X')
        Y_true = tf.placeholder(tf.float32, name='Y_True')

    # 定义预测节点
    with tf.name_scope('Inference'):
        W = tf.Variable(tf.zeros([1]), name='Weight')
        b = tf.Variable(tf.zeros([1]), name='Bias')

        # infernce: y=wx+b
        Y_pred = tf.add(tf.multiply(X, W), b)

    # 定义损失节点
    with tf.name_scope('Loss'):
        # 添加损失
        TrainLoss = tf.reduce_mean(tf.pow((Y_true-Y_pred), 2))/2

    with tf.name_scope('Train'):
        # Optimizer
        Optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)

        # Train:
        TrainOp = Optimizer.minimize(TrainLoss)

    with tf.name_scope('Evaluate'):
        # 添加评估节点：
        EvalLoss = tf.reduce_mean(tf.pow((Y_true-Y_pred), 2))/2

    # 初始化：
    InitOp = tf.global_variables_initializer()

    # save graph
    writer = tf.summary.FileWriter(logdir='logs', graph=tf.get_default_graph())
    writer.close()

    print('开启会话，运行计算图，训练模型')
    sess = tf.Session()
    sess.run(InitOp)

    # 重复训练一千次
    for step in range(1000):

        # 方法1：feed_dict里指定了整个训练数据集，也就是每次传入整个训练集进行训练
        # _, train_loss, train_w, train_b = sess.run([TrainOp, TrainLoss, W, b],
        #                                           feed_dict={X: train_X, Y_true: train_Y})

        # 方法2：每次传入一个训练样本就行训练
        for tx, ty in zip(train_X, train_Y):
            _, train_loss, train_w, train_b = sess.run([TrainOp, TrainLoss, W, b],
                                                       feed_dict={X: tx, Y_true: ty})

        # 每隔几步训练后，输出当前模型的损失
        if (step + 1) % 5 == 0:
            print('step:', '%04d' % (step + 1), "train_loss=", "{:9f}".format(train_loss),
                  "W=", train_w, "b=", train_b)

            # # ---展示当前训练后的拟合曲线
            # plt.plot(train_X, train_Y, 'ro', label='Original Train Points')
            # plt.plot(test_X, test_Y, 'b*', label='Original Test Points')
            # plt.plot(train_X, train_w * train_X + train_b, label='Fitted Line')
            # plt.legend()
            # plt.show()   # 会阻塞，需要手动关闭打开的图。当然也有实时自动更新的方法。。。

        # 每隔几步训练后，对当前模型进行测试
        if (step + 1) % 10 == 0:
            test_loss = sess.run(EvalLoss, feed_dict={X: test_X, Y_true: test_Y})

            print('step:', '%04d' % (step + 1), "test_loss=", "{:9f}".format(test_loss),
                  "W=", train_w, "b=", train_b)

    print('训练完毕')

    W, b = sess.run([W, b])
    print("得到的模型参数：", "W=", W, "b=", b)

    training_loss = sess.run(TrainLoss, feed_dict={X: train_X, Y_true: train_Y})
    print("训练上的损失：", training_loss)

    test_loss = sess.run(EvalLoss, feed_dict={X: test_X, Y_true: test_Y})
    print("测试上的损失：", test_loss)

    # ---展示拟合曲线
    plt.plot(train_X, train_Y, 'ro', label='Original Train Points')
    plt.plot(test_X, test_Y, 'b*', label='Original Test Points')
    plt.plot(train_X, W*train_X + b, label='Fitted Line')
    plt.legend()
    plt.show()


