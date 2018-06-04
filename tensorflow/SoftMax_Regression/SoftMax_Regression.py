import argparse
import os
import sys
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

FLAGS = None


# 在tf 1.2.1 版本中用tf.app.run运行函数时，必须带一个参数, 否则会报错
def main(my_argv):
    print('---------开始设计计算图--------------')
    # 告诉tensorflow模型将会被构建在默认的graph上
    with tf.Graph().as_default():

        # input:  定义输入节点
        with tf.name_scope('Input'):
            X = tf.placeholder(tf.float32, shape=[None, 784], name='X')
            Y_true = tf.placeholder(tf.float32, shape=[None, 10], name='Y_true')

        # inference: 前向预测，穿件一个线性模型：y=x*w+b
        with tf.name_scope('Inference'):
            W = tf.Variable(tf.zeros([784, 10]), name='Weight')
            b = tf.Variable(tf.zeros([10]), name='Bias')
            logits = tf.add(tf.matmul(X, W), b)

            # softmax把logits变成预测概率分布
            with tf.name_scope('Softmax'):
                Y_pred = tf.nn.softmax(logits=logits)

        # Loss: 定义损失节点
        with tf.name_scope('Loss'):
            TrainLoss = tf.reduce_mean(-tf.reduce_sum(Y_true * tf.log(Y_pred), axis=1))

        # Train: 定义训练节点
        with tf.name_scope('Train'):
            # Optimizer: 创建一个梯度下降优化器
            Optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
            # Train: 定义训练节点将梯度下降法应用于Loss
            TrainStep = Optimizer.minimize(TrainLoss)

        # Evaluate: 定义评估节点
        with tf.name_scope('Evaluate'):
            correct_pred = tf.equal(tf.argmax(Y_pred, 1), tf.argmax(Y_true, 1))
            accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))s

        # initial: 添加所有variable类型的变量的初始化节点
        Initop = tf.global_variables_initializer()

        print('----把计算图写入事件文件，在tensorboard里面查看')
        writer = tf.summary.FileWriter(logdir='logs/mnist_softmax', graph=tf.get_default_graph())
        writer.close()

        print('------开始运行计算图----------')

        # 加载MNIST数据
        mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)

        # 声明一个交互式会话
        sess = tf.InteractiveSession()

        # 初始化变量：w, b
        sess.run(Initop)

        # 开始按批次训练：总共训练1000次，每次100个样本
        for step in range(1000):
            batch_xs, batch_ys = mnist.train.next_batch(100)
            # 将当前批次的样本喂（feed)给计算图中的输入站位符， 启动训练节点开始训练
            # run()函数的第一个参数是要用到的变量列表, 注意：我们不需要第一个返回值
            _, train_loss = sess.run([TrainStep, TrainLoss],
                                     feed_dict={X: batch_xs, Y_true: batch_ys})
            # 打印每次的损失
            print('Train step: ', step, ', train_loss: ', train_loss)

        # 运行评估节点，获得预测的准确率
        accuracy_score = sess.run(accuracy, feed_dict={X: mnist.test.images,
                                                       Y_true: mnist.test.labels})

        print('模型准确率： ', accuracy_score)


# 调用main()函数
if __name__ == '__main__':

    # 首先申明一个参数解析器对象
    parser = argparse.ArgumentParser()
    # 为参数解析器添加参数： data_dir(指定数据集存放的路径)
    parser.add_argument('--data_dir', type=str,
                        default='../MNIST_data/',
                        help='数据集存放路径')

    # 解析已知的参数，放到到FLAGS中
    FLAGS, unparsed = parser.parse_known_args()

    print('sys.argv[0]=', sys.argv[0])

    # 运行Tensorflow应用
    tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
