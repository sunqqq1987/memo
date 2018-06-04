#!/usr/bin/python
# -*-coding:utf-8-*-

import tensorflow as tf

INPUT_D = 2500
OUTPUT_D = 5
LAYER_NODE1 = 100  # layer1 node num
REG_RATE = 0.01


def get_w(shape, regularizer=None):
    """
        get weight variable
    """
    w = tf.get_variable(
        "weights", shape,
        initializer=tf.truncated_normal_initializer(stddev=0.1))

    if regularizer is not None:
        tf.add_to_collection("losses", regularizer(w))

    return w


def interface(inputs, reg):
    """
        compute forword progration result
    """
    with tf.variable_scope("layer1"):
        ws = get_w([INPUT_D, LAYER_NODE1], reg)
        bs = tf.get_variable(
            "biases", [LAYER_NODE1],
            initializer=tf.constant_initializer(0.0))
        layer1 = tf.nn.relu(tf.matmul(inputs, ws) + bs)

    with tf.variable_scope("layer2"):
        ws = get_w([LAYER_NODE1, LAYER_NODE1], reg)
        bs = tf.get_variable(
            "biases", [LAYER_NODE1],
            initializer=tf.constant_initializer(0.0))
        layer2 = tf.nn.relu(tf.matmul(layer1, ws) + bs)

    with tf.variable_scope("layer3"):
        ws = get_w([LAYER_NODE1, OUTPUT_D], reg)
        bs = tf.get_variable(
            "biases", [OUTPUT_D],
            initializer=tf.constant_initializer(0.0))
        layer3 = tf.nn.softmax(tf.matmul(layer2, ws) + bs)

    return layer3
