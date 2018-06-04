#!/usr/bin/python
# -*-coding:utf-8-*-

import tensorflow as tf
from datasets import datasets


def interface(inputs, w1, b1, w2, b2):
    """
        compute forword progration result
    """
    # 对w1*inputs + b1的结果做relu处理: 将负值修正为0,
    # ReLU是线性修正，公式为：g(x) = max(0, x),
    # 它的作用是如果计算出的值小于0，就让它等于0，否则保持原来的值不变
    r_lay1 = tf.nn.relu(tf.matmul(inputs, w1) + b1)
    return tf.nn.softmax(tf.matmul(r_lay1, w2) + b2)


# 注意这是输入/输出张量的维度
INPUT_D = 2500
OUTPUT_D = 5
LAYER1_NODE_NUM = 100  # layer1 node num
REG_RATE = 0.001  # 正则化scale率

TRAIN_STEPS = 1000  # 训练次数
BATCH_SIZE = 10  # 每次读取的样本数

train_data_sets = datasets()
train_data_sets.read_train_data(".", True)

x = tf.placeholder(tf.float32, [None, INPUT_D], name="x-input")
Y_true = tf.placeholder(tf.float32, [None, OUTPUT_D], name="y-input")

# 从截断的正态分布中输出随机值. shape: 一维的张量，也是输出的张量
# b1,b2是列向量
w1 = tf.Variable(tf.truncated_normal([INPUT_D, LAYER1_NODE_NUM], stddev=0.1))
b1 = tf.Variable(tf.constant(0.0, shape=[LAYER1_NODE_NUM]))

w2 = tf.Variable(tf.truncated_normal([LAYER1_NODE_NUM, OUTPUT_D], stddev=0.1))
b2 = tf.Variable(tf.constant(0.0, shape=[OUTPUT_D]))

y = interface(x, w1, b1, w2, b2)

# loss
cross_entropy = tf.reduce_mean(-tf.reduce_sum(Y_true * tf.log(y + 1e-10)))
# cross_entropy = -tf.reduce_sum(Y_true * tf.log(y + 1e-10))
# 正则化w1,w2
regularizer = tf.contrib.layers.l2_regularizer(REG_RATE)
regularization = regularizer(w1) + regularizer(w2)
loss = cross_entropy + regularization


train_step = tf.train.GradientDescentOptimizer(0.01).minimize(loss)

# training
init_op = tf.global_variables_initializer()
sess = tf.InteractiveSession()
sess.run(init_op)

saver = tf.train.Saver()

for step in range(TRAIN_STEPS):
    batch_xs, batch_ys = train_data_sets.train.next_batch(BATCH_SIZE)
    _, train_loss = sess.run([train_step, loss],
                             feed_dict={x: batch_xs, Y_true: batch_ys})
    print('Train step: ', step, ', train_loss: ', train_loss)

print("\ntrain done")

MODEL_PATH = "./model_softmax_layer1_L2/model.md"
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
