import tensorflow as tf
import numpy as np


class TextCNN(object):
    """
    A CNN for text classification.
    Uses an embedding layer, followed by a convolutional, max-pooling and softmax layer.
    """

    # sequence_length：句子固定长度（不足补全，超过截断）
    # num_classes：类别数
    # vocab_size：词库大小
    # embedding_size：词向量维度，也就是卷积核的宽度
    # filter_sizes：卷积核的尺寸（=高度）数组
    # num_filters：每个尺寸的卷积核数量
    # l2_reg_lambda=0.0：L2正则参数

    def __init__(
            self, sequence_length, num_classes, vocab_size,
            embedding_size, filter_sizes, num_filters, l2_reg_lambda=0.0):
        # 变量input_x存储句子矩阵，宽为sequence_length(词的数量)，长度自适应（=句子数量）
        # input_y存储句子对应的分类结果，宽度为num_classes，长度自适应
        # 变量dropout_keep_prob存储dropout参数，常量l2_loss为L2正则超参数

        # Placeholders for input, output and dropout
        self.input_x = tf.placeholder(tf.int32, [None, sequence_length], name="input_x")
        self.input_y = tf.placeholder(tf.float32, [None, num_classes], name="input_y")  # 真值
        self.dropout_keep_prob = tf.placeholder(tf.float32, name="dropout_keep_prob")

        # Keeping track of l2 regularization loss (optional)
        l2_loss = tf.constant(0.0)

        # self.W可以理解为词向量词典（卷积核），存储vocab_size个大小为embedding_size的词向量，随机初始化为-1~1之间的值；
        # self.embedded_chars是输入input_x对应的词向量表示，[句子数量, sequence_length, embedding_size]
        # self.embedded_chars_expanded是，将词向量表示扩充一个维度：维度变为[句子数量, sequence_length, embedding_size, 1]
        #   方便进行卷积（tf.nn.conv2d的input参数为四维变量）
        # tf.expand_dims(input, axis=None, name=None, dim=None)：在input第axis位置增加一个维度（dim用法等同于axis，官方文档已弃用）

        # Embedding layer
        with tf.device('/cpu:0'), tf.name_scope("embedding"):
            # 定义W并初始化，变量名为W
            self.W = tf.Variable(
                tf.random_uniform([vocab_size, embedding_size], -1.0, 1.0),
                name="W")
            self.embedded_chars = tf.nn.embedding_lookup(self.W, self.input_x)
            self.embedded_chars_expanded = tf.expand_dims(self.embedded_chars, -1)

        # Create a convolution + maxpool layer for each filter size
        pooled_outputs = []
        for i, filter_size in enumerate(filter_sizes):
            with tf.name_scope("conv-maxpool-%s" % filter_size):

                # Convolution Layer

                # filter_shape：卷积核矩阵：包括num_filters(卷积核个数,也叫输出通道数)个大小为filter_size(卷积核的高度)*
                # embedding_size(卷积核的宽度)的卷积核，输入通道数为1
                #  卷积核尺寸中的embedding_size，相当于对输入文字序列从左到右卷，没有上下卷的过程
                # W：卷积核，shape为filter_shape，元素随机生成，正态分布
                # b：偏移量，因为有num_filters个卷积核，故有这么多个偏移量
                # conv：W与self.embedded_chars_expanded的卷积

                filter_shape = [filter_size, embedding_size, 1, num_filters]
                W = tf.Variable(tf.truncated_normal(filter_shape, stddev=0.1), name="W")
                b = tf.Variable(tf.constant(0.1, shape=[num_filters]), name="b")

                # 参考：http://blog.csdn.net/mao_xiao_feng/article/details/78004522
                # 函数tf.nn.conv2d(input, filter, strides, padding, use_cudnn_on_gpu=None, name=None)实现卷积计算
                #  input:  输入的词向量,[句子数(图片数，也称batch), 句子定长(对应图高), 词向量维度(对应图宽), 1(对应图像输入通道数in_channels)]
                #  filter: 卷积核W，[卷积核的高度，卷积核的宽度(词向量维度)，1(图像输入通道数in_channels)，卷积核个数（输出通道数out_channels）]
                #  strides: 图像各维步长,一维向量，长度为4，图像通常为[1, x, x, 1]
                #  padding: 卷积方式，'SAME'为等长卷积, 'VALID'为窄卷积
                #  输出一个feature map：shape是[batch, height, width, out_channels]，表示batch个out_channels张[height, width]

                conv = tf.nn.conv2d(
                    self.embedded_chars_expanded,
                    W,
                    strides=[1, 1, 1, 1],
                    padding="VALID",
                    name="conv")

                # Apply nonlinearity

                # h: 存储WX+b后非线性激活的结果,四维张量[batch, height, width, channels]
                # 可以理解为,正面或者负面评价有一些标志词汇,这些词汇概率被增强，即一旦出现这些词汇,倾向性分类进正或负面评价,
                # 该激励函数可加快学习进度，增加稀疏性,因为让确定的事情更确定,噪声的影响就降到了最低。
                h = tf.nn.relu(tf.nn.bias_add(conv, b), name="relu")

                # pooled：池化后结果, append到pooled_outputs中
                # 函数tf.nn.max_pool(value, ksize, strides, padding, name=None)：对value池化
                # value：待池化的四维张量[batch, height, width, channels]
                # ksize：池化窗口大小，长度（大于）等于4的数组，与value的维度对应，一般为[1,height,width,1]，batch和channels上不池化
                # strides:与卷积步长类似
                # padding：与卷积的padding参数类似
                # 返回值shape仍然是[batch, height, width, channels]这种形式

                # Maxpooling over the outputs
                pooled = tf.nn.max_pool(
                    h,
                    ksize=[1, sequence_length - filter_size + 1, 1, 1],
                    strides=[1, 1, 1, 1],
                    padding='VALID',
                    name="pool")

                # 对每个卷积核重复上述操作，
                # 故pool_outputs中是若干种卷积核的池化后的结果，维度为[len(filter_sizes), batch, height, width, channels=1]
                pooled_outputs.append(pooled)

        # Combine all the pooled features
        # 扁平化数据，以便跟全连接层相连
        # 卷积核的总数
        num_filters_total = num_filters * len(filter_sizes)
        # 将pooled_outputs中所有的[batch, height, width, channels]在第4个维度(width)上合并
        self.h_pool = tf.concat(pooled_outputs, 3)
        # 将h_pool变换为列为卷积核总数的2维矩阵h_pool_flat
        self.h_pool_flat = tf.reshape(self.h_pool, [-1, num_filters_total])

        # Add dropout
        # drop层,防止过拟合,参数为dropout_keep_prob
        # 过拟合的本质是采样失真,噪声权重影响了判断，如果采样足够多,足够充分,噪声的影响可以被量化到趋近事实,也就无从过拟合。
        # 即数据越大,drop和正则化就越不需要。
        with tf.name_scope("dropout"):
            self.h_drop = tf.nn.dropout(self.h_pool_flat, self.dropout_keep_prob)

        # Final (unnormalized) scores and predictions
        # 输出层
        with tf.name_scope("output"):
            # 获取变量W,
            W = tf.get_variable(
                "W",
                shape=[num_filters_total, num_classes],
                initializer=tf.contrib.layers.xavier_initializer())
            b = tf.Variable(tf.constant(0.1, shape=[num_classes]), name="b")
            # 损失函数导入
            l2_loss += tf.nn.l2_loss(W)
            l2_loss += tf.nn.l2_loss(b)
            # 得分=xw+b
            self.scores = tf.nn.xw_plus_b(self.h_drop, W, b, name="scores")
            # 预测结果: 按列方向获取最大的得分值，注意score与b都是一维的行向量
            self.predictions = tf.argmax(self.scores, 1, name="predictions")

        # Calculate mean cross-entropy loss
        with tf.name_scope("loss"):
            # loss: 交叉熵损失函数
            losses = tf.nn.softmax_cross_entropy_with_logits(logits=self.scores, labels=self.input_y)
            self.loss = tf.reduce_mean(losses) + l2_reg_lambda * l2_loss

        # Accuracy
        with tf.name_scope("accuracy"):
            # 准确率: 求和计算算数平均值
            correct_predictions = tf.equal(self.predictions, tf.argmax(self.input_y, 1))
            self.accuracy = tf.reduce_mean(tf.cast(correct_predictions, "float"), name="accuracy")
