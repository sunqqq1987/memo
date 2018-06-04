import tensorflow as tf
import numpy as np

# Follow 2 lines fix some warnings shows.
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def tf_env_info():
    # 测试tensorflow环境是否正常
    print('TensorFlow version: {0}'.format(tf.__version))

    hello = tf.constant('Hello, TensorFlow!')
    sess = tf.Session()
    print(sess.run(hello))


def test_tbd_histogram():
    k = tf.placeholder(tf.float32)

    # 正太分布的直方图
    # Make a normal distribution, with a shifting mean
    mean_moving_normal = tf.random_normal(shape=[1000], mean=(5 * k), stddev=1)
    # Record that distribution into a histogram summary
    tf.summary.histogram("normal/moving_mean", mean_moving_normal)

    # Setup a session and summary writer
    sess = tf.Session()
    writer = tf.summary.FileWriter("./tmp/histogram_example")

    summaries = tf.summary.merge_all()

    # Setup a loop and write the summaries to disk
    N = 400
    for step in range(N):
        k_val = step / float(N)  # 均值
        summ = sess.run(summaries, feed_dict={k: k_val})

        # print("{},{}".format(k_val, summ))

        writer.add_summary(summ, global_step=step)


def test_conv2d():
    # conv2d()的输出是：feature map 形如 [batch, height, width, out_channels]

    # case 1
    # 考虑一种最简单的情况，现在有一张3×3
    # 单通道的图像（对应的shape：[1，3，3，1]），用一个1×1
    # 的卷积核（对应的shape：[1，1，1，1]）去做卷积，最后会得到一张3×3
    # 的feature map: [1, 3, 3, 1]

    input = tf.Variable(tf.random_normal([1, 3, 3, 1]))
    filter = tf.Variable(tf.random_normal([1, 1, 1, 1]))
    op1 = tf.nn.conv2d(input, filter, strides=[1, 1, 1, 1], padding='VALID')

    # case 2
    # 增加图片的通道数，使用一张3×3
    # 五通道的图像（对应的shape：[1，3，3，5]），用一个1×1
    # 的卷积核（对应的shape：[1，1，1，1]）去做卷积，仍然是一张3×3
    # 的feature map: [1, 3, 3, 1]，这就相当于每一个像素点，卷积核都与该像素点的每一个通道做点积

    input = tf.Variable(tf.random_normal([1, 3, 3, 5]))
    filter = tf.Variable(tf.random_normal([1, 1, 5, 1]))
    op2 = tf.nn.conv2d(input, filter, strides=[1, 1, 1, 1], padding='VALID')

    # case 3
    # 把卷积核扩大，现在用3×3
    # 的卷积核做卷积，最后的输出是一个值，相当于情况2的feature
    # map所有像素点的值求和: feature map: [1, 1, 1, 1]

    input = tf.Variable(tf.random_normal([1, 3, 3, 5]))
    filter = tf.Variable(tf.random_normal([3, 3, 5, 1]))
    op3 = tf.nn.conv2d(input, filter, strides=[1, 1, 1, 1], padding='VALID')

    # case 4
    # 使用更大的图片将情况2的图片扩大到5×5，仍然是3×3
    # 的卷积核，令步长为1，输出3×3
    # 的feature map: [1, 3, 3, 1]

    input = tf.Variable(tf.random_normal([1, 5, 5, 5]))
    filter = tf.Variable(tf.random_normal([3, 3, 5, 1]))
    op4 = tf.nn.conv2d(input, filter, strides=[1, 1, 1, 1], padding='VALID')

    # case 5
    # 上面我们一直令参数padding的值为‘VALID’，当其为‘SAME’时，表示卷积核可以停留在图像边缘，如下，输出5×5
    # 的feature map: [1, 5, 5, 1]

    input = tf.Variable(tf.random_normal([1, 5, 5, 5]))
    filter = tf.Variable(tf.random_normal([3, 3, 5, 1]))
    op5 = tf.nn.conv2d(input, filter, strides=[1, 1, 1, 1], padding='SAME')

    # case 6
    # 如果卷积核有多个, 此时输出7张5×5的feature map: [1, 5, 5, 7]

    input = tf.Variable(tf.random_normal([1, 5, 5, 5]))
    filter = tf.Variable(tf.random_normal([3, 3, 5, 7]))
    op6 = tf.nn.conv2d(input, filter, strides=[1, 1, 1, 1], padding='SAME')

    # case 7
    # 步长不为1的情况，文档里说了对于图片，因为只有两维，通常strides取[1，stride，stride，1]
    # 此时，输出7张3×3的feature map: [1, 3, 3, 7]

    input = tf.Variable(tf.random_normal([1, 5, 5, 5]))
    filter = tf.Variable(tf.random_normal([3, 3, 5, 7]))
    op7 = tf.nn.conv2d(input, filter, strides=[1, 2, 2, 1], padding='SAME')

    # case 8
    # 如果batch值不为1，同时输入2张图
    # 每张图，都有7张3×3的feature map，输出的shape就是[2，3，3，7]

    input = tf.Variable(tf.random_normal([2, 5, 5, 5]))
    filter = tf.Variable(tf.random_normal([3, 3, 5, 7]))
    op8 = tf.nn.conv2d(input, filter, strides=[1, 2, 2, 1], padding='SAME')

    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        print("\ncase 1")
        print(sess.run(op1))
        print("\ncase 2")
        print(sess.run(op2))
        print("\ncase 3")
        print(sess.run(op3))
        print("\ncase 4")
        print(sess.run(op4))
        print("\ncase 5")
        print(sess.run(op5))
        print("\ncase 6")
        print(sess.run(op6))
        print("\ncase 7")
        print(sess.run(op7))
        print("\ncase 8")
        print(sess.run(op8))


def do_inference(x):
    print("inference")
    for i in range(5):
        x = tf.maximum(x, 0.1 * x)
    return x


if __name__ == '__main__':
    # test_conv2d()

    planes = [[[1, 2, 3],
               [4, 5, 6]]]

    # planes = [np.pad(im[:, :, 0], len(model_list[0]) + len(model_list[1]), "edge") / 255.0]
    planes = np.array(planes)
    print(planes.shape)
    planes = planes.reshape(1, planes.shape[1], planes.shape[2], 1)
    print(planes.shape)
    planes = np.transpose(planes, (0, 3, 1, 2))
    print(planes.shape)

    wx = tf.placeholder(tf.float32)
    wy = tf.placeholder(tf.float32)
    planes_t = tf.placeholder(tf.float32, shape=[1, 1, None, None], name="planes_input")

    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        print("begin init")
        sess.run(init)

        x = planes_t
        x = do_inference(x)

        # feed_dict = {
        #     x: planes_t
        # }
        # x= sess.run(
        #     [train_op],
        #     feed_dict)
