# -*- coding: utf-8 -*-

# waifu2x.py by @marcan42 based on https://github.com/nagadomi/waifu2x
# MIT license, see https://github.com/nagadomi/waifu2x/blob/master/LICENSE

# 必要なモジュールのインポート
import json, sys, numpy as np  # jsonサポート、システム、数値ユーティリティ(と思われる)

from reportlab.lib.utils import flatten
from scipy import misc, signal  # scipyより、その他処理、信号処理
from PIL import Image
import os
import tensorflow as tf

import operator
from functools import reduce


from tensorflow.python.framework import graph_util

# ------workaround for err below: -----------
#    NameError: name 'tempfile' is not defined
import tempfile
import subprocess

tf.contrib.lite.tempfile = tempfile
tf.contrib.lite.subprocess = subprocess

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'
# Model export script: https://mrcn.st/t/export_model.lua (needs a working waifu2x install)

# infile, outfile = sys.argv[1:]

# infile = "miku_small.png"
# outfile = "miku_small_tflite.png"

# infile = "girl3.png"
# outfile = "girl3_tflite.png"


print("graph-------")
# ----------- graph ------------------------------
# x_input = tf.placeholder(tf.float32, [2048 * 2048], name="x_input")  # need to fix dimension
x_input = tf.placeholder(tf.float32, [1, None, None, 1], name="x_input")

# init_val = tf.constant(0.01, shape=[2048 * 2048], dtype=tf.float32)
init_val = tf.constant(0.01, dtype=tf.float32)
# init_val = tf.constant(0.01, shape=[1, None, None, 1], dtype=tf.float32)  # issue
x_output = tf.Variable(init_val, name="x_output")

# x_output = tf.placeholder(tf.float32, [2048 * 2048], name="x_output")  # need to fix dimension

# x_target_len = tf.placeholder(tf.int32, [1], name="x_target_len")

# # attention: need to use float32, otherwise TOCO convert will fail.
# x_resize_height = tf.placeholder(tf.float32, [1], name="x_resize_height")
# x_resize_width = tf.placeholder(tf.float32, [1], name="x_resize_width")
# print(x_resize_height)
# print(x_resize_width)

# m_W = tf.placeholder(tf.float32, [None, None, None, None, 3], name="m_W")  # element: (64, 64, 3, 3)
m_W = tf.placeholder(tf.float32, [None, None], name="m_W")  # element: (64, 64, 3, 3)
m_nInputPlane = tf.placeholder(tf.int32, [None, 1], name="m_nInputPlane")  # 1D
m_bias = tf.placeholder(tf.float32, [None, None], name="m_bias")  # 1D, element: 1D
m_nOutputPlane = tf.placeholder(tf.int32, [None, 1], name="m_nOutputPlane")  # 1D

# # get resize_len
# idx_h = tf.Variable([0])
# idx_w = tf.Variable([0])
# resize_height = tf.gather_nd(x_resize_height, [0])
# # print("resize_height,", resize_height)
# resize_height = tf.cast(resize_height, 'int32')
#
# resize_width = tf.gather_nd(x_resize_width, idx_w)
# resize_width = tf.cast(resize_width, 'int32')
# print("resize_height,", resize_height)
# print("resize_width,", resize_width)

# x = None

# -------move to user code when init-----[------------
# #if s == 0:  # first, need to convert x_input to well-size for calc
# idx_beg = tf.Variable([0])
# # idx_size = tf.Variable([resize_height * resize_width])
# resize_len = tf.multiply(resize_height, resize_width)
# # resize_len = 10
# print("resize_len,", resize_len)
# idx_size = tf.Variable([resize_len])  # issue
# # idx_size = tf.Variable([resize_height * resize_width], dtype=tf.float32)  # issue
# x0 = tf.slice(x_input, idx_beg, idx_size)  # x_t = x_t[: resize_width*resize_height]
# #
# # print("x0,", x0)

# # reshape to 4D for calc
# x = tf.reshape(x, (1, resize_height, resize_width, 1))

# -----------------------]

x = x_input  # ----need x_input is well matched size. x.shape= (1, 204, 204, 1)
print("x,", x)

# ------
for s in range(14):
    #
    idx_n1 = tf.Variable([s, 0])  # get m_nOutputPlane[0]
    n1 = tf.gather_nd(m_nInputPlane, idx_n1)  # step["nOutputPlane"]
    # print("n1,", n1)

    idx_n2 = tf.Variable([s, 0])  # get m_nOutputPlane[0]
    n2 = tf.gather_nd(m_nOutputPlane, idx_n2)  # step["nOutputPlane"]
    # print("n2,", n2)

    idx_w = tf.Variable([s])  # get m_W[0]
    w1 = tf.gather_nd(m_W, idx_w)  # np.array(step["weight"]
    W = tf.reshape(w1, (3, 3, n1, n2))  # shape=(3, 3, step["nInputPlane"], step["nOutputPlane"])

    idx_b = tf.Variable([s])  # get m_bias[0]
    b1 = tf.gather_nd(m_bias, idx_b)  # np.array(step["bias"])

    b = tf.reshape(b1, (1, n2, 1, 1))  # b = tf.reshape(b1, (1, 32, 1, 1))
    b = tf.transpose(b, (0, 2, 3, 1))

    conv_r = tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding="VALID", data_format="NHWC")
    add_r = tf.add(conv_r, b)
    max_t = tf.maximum(add_r, 0.1 * add_r)
    x = max_t

x_output = max_t

# print("s=", s)

# covert max_t to fixed_size

# reshape to 1D
# x_out = np.reshape(max_t2, [-1])
# print("1D, x_out.shape=", x_out.shape)
#
# # pad target to fixed size for output to model
# # to int
# print(target_len[0])
# target_len = int(target_len[0])
# print(target_len)
#
# print("target_len=", target_len)
# pad_len = (2048 * 2048) - target_len
# x_out = np.pad(x_out, (0, pad_len), 'constant')
# print("after pad, x_out.shape=", x_out.shape)
#
# print("end part:", x_out[target_len - 2], x_out[target_len - 1], x_out[target_len], x_out[target_len + 1])

# x_output = max_t
# print("x_output,", x_output)

print()

print()
print("train------")

# infile = "audio176.png"
# outfile = "audio176_tflite.png"

# infile = "audio88.png"
# outfile = "audio88_pb_output.png"

infile = "miku_small.png"
outfile = "miku_small_tflite.png"

scalemodelpath = "scale2.0x_model.json"
denoisemodelpath = "noise3_model.json"

model_list = []
model_list.append(json.load(open(scalemodelpath)))
model_list.append(json.load(open(denoisemodelpath)))
print("len(model_list)=", len(model_list))

def flatten(a):
    if not isinstance(a, (list, )):
        return [a]
    else:
        b = []
        for item in a:
            b += flatten(item)
    return b

# model init
W_l = []
b_l = []
nInputPlane_l = []
nOutputPlane_l = []
i=0
for model in model_list:
    for step in model:
        if i == 0:
            print("step[weight]=", np.transpose(np.array(step["weight"]), (2, 3, 1, 0)))

            i=1

        W_l.append(flatten(step["weight"]))  # p_arr = np.append(p_arr,p_) #直接向p_arr里添加p_

        b_l.append(flatten(step["bias"]))
        nInputPlane_l.append(np.reshape(np.array(step["nInputPlane"]), (-1)))
        nOutputPlane_l.append(np.reshape(np.array(step["nOutputPlane"]), (-1)))


print(W_l[0])
print(W_l[1])
im = Image.open(infile).convert("YCbCr")

target_width = 2 * im.size[0]
target_height = 2 * im.size[1]
print("target, 2x img size= %d, %d" % (target_height, target_width))

im = misc.fromimage(im.resize((target_width, target_height), resample=Image.NEAREST)).astype("float32")

print("---len(model_list[0])=", len(model_list[0]))
print("---len(model_list[1])=", len(model_list[1]))

# print(model_list[0])

planes = [np.pad(im[:, :, 0], len(model_list[0]) + len(model_list[1]), "edge") / 255.0]
planes = np.array(planes)
planes = planes.reshape(1, planes.shape[1], planes.shape[2], 1)
planes = np.transpose(planes, (0, 3, 1, 2))
print("planes.shape=", planes.shape)

print()

height = planes.shape[2]
width = planes.shape[3]

# --- train ---------------------------
print("train_graph(height=%d, width=%d)" % (height, width))

init = tf.global_variables_initializer()
with tf.Session() as sess:
    writer = tf.summary.FileWriter("logs/", sess.graph)

    print("trainable_variables:")
    variable_names = [c.name for c in tf.trainable_variables()]
    print(variable_names)

    print("begin init")
    sess.run(init)

    print("init done")

    # --- this part should be init in user code ---------------------[
    print("---nInputPlane=", model_list[0][0]["nInputPlane"])

    x_in = np.reshape(planes, (1, model_list[0][0]["nInputPlane"], planes.shape[2], planes.shape[3]))
    x_in = np.transpose(x_in, (0, 2, 3, 1))
    print("x_in.shape=", x_in.shape)

    print("len(W_l)=", len(W_l))
    print("len(W_l)=", len(W_l[0]))
    # print("len(W_l)=", len(W_l[0][0]))
    # print("len(W_l)=", len(W_l[0][0][0]))
    # print("len(W_l)=", len(W_l[0][0][0][0]))
    w_a = np.array(W_l)
    b_a = np.array(b_l)
    nInputPlane_a = np.array(nInputPlane_l)
    nOutputPlane_a = np.array(nOutputPlane_l)
    # ----------------------------------------------------------]

    #print("W_l[1]=", W_l[1])
    # w_a = np.array(list(W_l))
    print("w_a.shape=", w_a.shape)
    print("b_a.shape=", b_a.shape)
    print("nInputPlane_a.shape=", nInputPlane_a.shape)
    print("nOutputPlane_a.shape=", nOutputPlane_a.shape)
    feed_dict = {
        x_input: x_in,
        # m_W: [W_l], m_bias: b_a, m_nInputPlane: nInputPlane_a, m_nOutputPlane: nOutputPlane_a
        m_W: W_l
    }

    img_r = sess.run([x_output], feed_dict)
    print("img_r.shape=", img_r.shape)

    print()

    writer.close()
    print("---log done.")

    # --- direct save as tflite----------------
    tflite_model = tf.contrib.lite.toco_convert(sess.graph_def,
                                                [x_input, m_W, m_bias, m_nInputPlane, m_nOutputPlane],
                                                [x_output])
    open("converted_model.tflite", "wb").write(tflite_model)
    print("---save tflite done.")

    # # --- ckpt ---(fail)----------------
    # tf.train.Saver().save(sess, './test.ckpt')
    # print("---save ckpt done.")

    # # --- pb ----------------------------
    # pb_file = "./frozen.pb"
    # # Turn all the variables into inline constants inside the graph and save it.
    # frozen_graph_def = graph_util.convert_variables_to_constants(
    #     sess, sess.graph_def, ['x_input', 'x_resize_height', 'x_resize_width', 'x_target_len',
    #                            'm_W', 'm_bias', 'm_nInputPlane', 'm_nOutputPlane',
    #                            'x_output'])
    #
    # # 将计算图写入到模型文件中
    # model_f = tf.gfile.GFile(pb_file, "wb")
    # model_f.write(frozen_graph_def.SerializeToString())
    # print("---save frozen pb done.")

    # # reshape to 1D
    # x_in = np.reshape(x_in, (-1))
    # print("1D, x_in.shape=", x_in.shape)
    #
    # # pad to fixed size as input
    # resize_len = x_in.shape[0]
    # print("resize_len=", resize_len)
    # pad_len = (2048 * 2048) - resize_len
    # x_in = np.pad(x_in, (0, pad_len), 'constant')
    # print("after pad, x_in.shape=", x_in.shape)
    # -------------------------------------------------]

    # print()
    # print("height=", height)
    # height_a = np.array([float(height)])
    #
    # width_a = np.array([float(width)])
    # target_len_a = np.array([target_width * target_height])
    # print(height_a, width_a, target_len_a)
    #
    # w_a = np.array([W_l])
    # b_a = np.array([b_l])
    # nInputPlane_a = np.array([nInputPlane_l])
    # nOutputPlane_a = np.array([nOutputPlane_l])
    #
    # print(height, width)
    # print("target_len=", target_len_a)
    #
    # feed_dict = {
    #     x_input: x_in, x_target_len: target_len_a, x_resize_height: height_a, x_resize_width: width_a,
    #     m_W: w_a, m_bias: b_a, m_nInputPlane: nInputPlane_a, m_nOutputPlane: nOutputPlane_a
    # }
    # img_r = sess.run([x_output], feed_dict=feed_dict)
    # print("img_r.shape=", img_r.shape)

    #
    # # ---------user code ------------------[--
    #
    # # # to int
    # # print(resize_height[0])
    # # resize_height = int(resize_height[0])
    # # print(resize_height)
    # #
    # # print(resize_width[0])
    # # resize_width = int(resize_width[0])
    # # print(resize_width)
    # #
    # # # get resize_len
    # # x_t = x_t[: resize_width*resize_height]
    # #
    # # # reshape to 4D for calc
    # # x = np.reshape(x_t, (1, resize_height, resize_width, 1))
    # # print("4D, x.shape=", x.shape)
    # # i=0
    # # for model in model_list:
    # #     for step in model:
    # #
    # #         W = np.transpose(np.array(step["weight"]), (2, 3, 1, 0))
    # #         b = np.reshape(np.array(step["bias"]), (1, step["nOutputPlane"], 1, 1))
    # #         b = np.transpose(b, (0, 2, 3, 1))
    # #
    # #         conv_r = tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding="VALID", data_format="NHWC", name="conv_r")
    # #         add_r = tf.add(conv_r, b, name="add_r")
    # #         max_t = tf.maximum(add_r, 0.1 * add_r, name="max_r")
    # #         x = max_t
    # #
    # #         # feed_dict = {
    # #         #     x_r: x, graph['W_r']: W, graph['b_r']: b
    # #         # }
    # #         # x = sess.run(graph['max_r'], feed_dict)
    # #
    # #         print("max_t.shape=", max_t.shape)
    # #         # graph['max_r'] = x
    # #         # tf.assign(graph['max_r'], x)
    # #
    # #         i=i+1
    # # print("i=", i)
    # #
    # # print("---final result, x.shape=", x.shape)
    # #
    # # max_t2 = max_t.eval()
    #
    # print("trainable_variables:")
    # variable_names = [c.name for c in tf.trainable_variables()]
    # print(variable_names)
    #
    # writer.close()
    # print("---log done.")


    # # ---------------- output image ------------------
    # # x_f = x
    # # print("x=", x)
    #
    # x_f = img_r.eval()
    # # assert len(planes) == 1
    # im[:, :, 0] = np.clip(x_f.reshape(x_f.shape[1], x_f.shape[2]), 0, 1) * 255
    #
    # misc.toimage(im, mode="YCbCr").convert("RGB").save(outfile)
    # sys.stderr.write("Done\n")
    # print("outfile=", outfile)
