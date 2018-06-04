# -*- coding: utf-8 -*-

# waifu2x.py by @marcan42 based on https://github.com/nagadomi/waifu2x
# MIT license, see https://github.com/nagadomi/waifu2x/blob/master/LICENSE

# 必要なモジュールのインポート
import json, sys, numpy as np  # jsonサポート、システム、数値ユーティリティ(と思われる)
from scipy import misc, signal  # scipyより、その他処理、信号処理
from PIL import Image
import os
import tensorflow as tf

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
# outfile = "miku_small_pb_out.png"

# infile = "mik4.png"
# outfile = "mik4_pb_output.png"

# infile = "girl3.png"
# outfile = "girl3_pb_output.png"

infile = "audio88.png"
outfile = "audio88_pb_output.png"

im = Image.open(infile).convert("YCbCr")

target_width = 2 * im.size[0]
target_height = 2 * im.size[1]
print("target, 2x img size= %d, %d" % (target_height, target_width))

im = misc.fromimage(im.resize((target_width, target_height), resample=Image.NEAREST)).astype("float32")

# followings depend on model data
len_model_list0 = 7
len_model_list1 = 7
nInputPlane = 1

planes = [np.pad(im[:, :, 0], len_model_list0 + len_model_list1, "edge") / 255.0]
planes = np.array(planes)
planes = planes.reshape(1, planes.shape[1], planes.shape[2], 1)
planes = np.transpose(planes, (0, 3, 1, 2))
print("planes.shape=", planes.shape)

print()


def recognize(planes, nInputPlane, pb_file_path, ouput_img_path):
    with tf.Graph().as_default():
        output_graph_def = tf.GraphDef()

        with open(pb_file_path, "rb") as f:
            output_graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(output_graph_def, name="")

        with tf.Session() as sess:
            init = tf.global_variables_initializer()
            sess.run(init)

            # --- get tensors
            # 'x_input', 'x_resize_height', 'x_resize_width', 'x_target_len', 'max_r'
            x_input = sess.graph.get_tensor_by_name("x_input:0")
            print(x_input)
            print("x_input.shape=", x_input.shape)

            x_resize_height = sess.graph.get_tensor_by_name("x_resize_height:0")
            print(x_resize_height)
            print("x_resize_height.shape=", x_resize_height.shape)

            x_resize_width = sess.graph.get_tensor_by_name("x_resize_width:0")
            print(x_resize_width)
            print("x_resize_width.shape=", x_resize_width.shape)

            x_target_len = sess.graph.get_tensor_by_name("x_target_len:0")
            print(x_target_len)
            print("x_target_len.shape=", x_target_len.shape)

            max_r = sess.graph.get_tensor_by_name("max_r:0")
            print(max_r)
            print("max_r.shape=", max_r.shape)

            # Maximum_13 = sess.graph.get_tensor_by_name("Maximum_13:0")
            # print(Maximum_13)
            # print("Maximum_13.shape=", Maximum_13.shape)

            # --- init ------------------------------------
            print()
            x_in = np.reshape(planes, (1, nInputPlane, planes.shape[2], planes.shape[3]))
            x_in = np.transpose(x_in, (0, 2, 3, 1))

            # reshape to 1D
            x_in = np.reshape(x_in, (-1))
            print("1D, x_in.shape=", x_in.shape)

            # pad to fixed size as input
            resize_len = x_in.shape[0]
            print("resize_len=", resize_len)
            pad_len = (2048 * 2048) - resize_len
            x_in = np.pad(x_in, (0, pad_len), 'constant')
            print("after pad, x_in.shape=", x_in.shape)

            print()

            height_t = planes.shape[2]
            width_t = planes.shape[3]
            height_a = np.array([height_t])
            width_a = np.array([width_t])

            print(height_t, width_t)

            target_len_a = np.array([target_width * target_height])
            print("target_len=", target_len_a)

            # --- run----------------------------
            feed_dict = {x_input: x_in, x_resize_height: height_a, x_resize_width: width_a, x_target_len: target_len_a}
            img_r = sess.run(max_r, feed_dict)

            print("--- result, img_r.shape=", img_r.shape)
            # print("img_r=", img_r)
            # for i in range(21):
            #     print(img_r[i])
            target_len = target_height * target_width
            print("end part:", img_r[target_len - 2], img_r[target_len - 1], img_r[target_len], img_r[target_len + 1])

            # img_r = img_r.eval()

            # get target_len
            target_len = target_height * target_width
            print("target_len=", target_len)
            img_r = img_r[: target_len]
            print("target, img_r.shape=", img_r.shape)

            # reshape to 4D for output as img
            img_r = np.reshape(img_r, (1, target_height, target_width, 1))
            print("4D, img_r.shape=", img_r.shape)

            # print("img_r=", img_r)

            im[:, :, 0] = np.clip(img_r.reshape(img_r.shape[1], img_r.shape[2]), 0, 1) * 255

            misc.toimage(im, mode="YCbCr").convert("RGB").save(ouput_img_path)
            sys.stderr.write("Done\n")
            print("outfile=", outfile)


recognize(planes, nInputPlane, "frozen.pb", outfile)
