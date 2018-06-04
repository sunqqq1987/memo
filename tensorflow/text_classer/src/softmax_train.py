#!/usr/bin/python
# -*-coding:utf-8-*-

import tensorflow as tf
from datasets import datasets


# 注意这是输入/输出张量的维度
INPUT_D = 2500
OUTPUT_D = 5

TRAIN_STEPS = 1000  # 训练次数
BATCH_SIZE = 10  # 每次读取的样本数

train_data_sets = datasets()
train_data_sets.read_train_data(".", True)

x = tf.placeholder(tf.float32, [None, INPUT_D])
Y_true = tf.placeholder(tf.float32, [None, OUTPUT_D])

W = tf.Variable(tf.zeros([INPUT_D, OUTPUT_D]))
b = tf.Variable(tf.zeros([OUTPUT_D]))
y = tf.nn.softmax(tf.matmul(x, W) + b)

# loss
cross_entropy = tf.reduce_mean(-tf.reduce_sum(Y_true * tf.log(y + 1e-10), axis=1))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

# training
init_op = tf.global_variables_initializer()

sess = tf.InteractiveSession()

sess.run(init_op)

saver = tf.train.Saver()

for step in range(TRAIN_STEPS):
    batch_xs, batch_ys = train_data_sets.train.next_batch(BATCH_SIZE)
    _, train_loss = sess.run([train_step, cross_entropy],
                             feed_dict={x: batch_xs, Y_true: batch_ys})
    print('Train step: ', step, ', train_loss: ', train_loss)

print("W:")
print(W.eval())
print("b:")
print(b.eval())

print("\ntrain done")

MODEL_PATH = "./model_softmax/model.md"
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
