#!/usr/bin/python
# -*-coding:utf-8-*-


import tensorflow as tf
import nn_interface
from datasets import datasets

INPUT_NODE = 2500
OUTPUT_NODE = 5
REG_RATE = 0.001

TRAIN_STEPS = 1000  # 训练次数
BATCH_SIZE = 10  # 每次读取的样本数


def train(data_sets):
    """
        train model
    """
    x = tf.placeholder(tf.float32, [None, INPUT_NODE], name="x-input")
    Y_true = tf.placeholder(tf.float32, [None, OUTPUT_NODE], name="y-input")

    # inference: 前向预测, 创建多层神经网络模型
    # 使用L2正则化
    reg = tf.contrib.layers.l2_regularizer(REG_RATE)
    y = nn_interface.interface(x, reg)

    # loss
    cross_entropy = tf.reduce_mean(-tf.reduce_sum(Y_true * tf.log(y + 1e-10)))
    # cross_entropy = -tf.reduce_sum(Y_true * tf.log(y + 1e-10))
    loss = cross_entropy + tf.add_n(tf.get_collection("losses")) # 将全部的losses变量取出来，与交叉熵相加

    train_step = tf.train.GradientDescentOptimizer(0.01).minimize(loss)

    # training
    init_op = tf.global_variables_initializer()
    sess = tf.InteractiveSession()
    sess.run(init_op)

    saver = tf.train.Saver()

    for step in range(TRAIN_STEPS):
        batch_xs, batch_ys = data_sets.train.next_batch(BATCH_SIZE)
        _, train_loss = sess.run([train_step, loss],
                                 feed_dict={x: batch_xs, Y_true: batch_ys})
        print('Train step: ', step, ', train_loss: ', train_loss)

    print("\ntrain done")

    MODEL_PATH = "./model_nn_layer3/model.md"
    path = saver.save(sess, MODEL_PATH)
    print("save model %s done" % MODEL_PATH)

    saver.restore(sess, MODEL_PATH)
    print("\nrestore model %s done" % MODEL_PATH)

    # 用测试样本来评估准确率
    print("\n-----------Evaluate--------------")
    test_data_sets = datasets()
    test_data_sets.read_test_data(".", True)

    test_feed = {x: test_data_sets.test.text,
                 Y_true: test_data_sets.test.label}
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(Y_true, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    accuracy_score = sess.run(accuracy, feed_dict=test_feed)
    print("accuracy_score= %s" % accuracy_score)


def main(argv=None):
    data_sets = datasets()
    data_sets.read_train_data(".", True)
    train(data_sets)


if __name__ == "__main__":
    tf.app.run()
