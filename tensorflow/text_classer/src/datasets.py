#!/usr/bin/python
# -*-coding:utf-8-*-

import numpy
import tensorflow as tf
import util

# 输入特征向量的维度
INPUT_DIM = 2500

# 输出类型的维度
OUTPUT_DIM = 5

class dataset(object):
    """
        data set info readed in disk file
    """

    def __init__(self, text, label, dtype=tf.float32):
        """
            init
        """
        # 注意以下类型都是numpy array
        # shape[0]是行数，即样本数
        self._num_examples = text.shape[0]
        self._text = text
        self._label = label
        self._index_in_epoch = 0
        self._epochs_completed = 0

    @property
    def num(self):
        return self._num_examples

    @property
    def text(self):
        return self._text

    @property
    def label(self):
        return self._label

    def next_batch(self, batch_size):
        """
            get next batch
        """

        start = self._index_in_epoch
        self._index_in_epoch += batch_size
        if self._index_in_epoch > self._num_examples:
            # complete epochs
            self._epochs_completed += 1

            # 如果读完了样本，则进行一次随机
            perm = numpy.arange(self._num_examples)
            numpy.random.shuffle(perm)
            self._text = self._text[perm]
            self._label = self._label[perm]

            start = 0
            self._index_in_epoch = batch_size
            assert batch_size <= self._num_examples

        end = self._index_in_epoch
        return self._text[start:end], self._label[start:end]


class datasets(object):
    """
        read datasets from {train.txt test.txt cv.txt}
    """

    def __init__(self):
        """

        """
        self.test = None
        self.train = None
        self.cv = None

        pass

    def read_train_data(self, data_dir, one_hot=False, dtype=tf.float32):
        """
            read datasets from train.txt and train_labels.txt
            cause all datasets is too large, read data separately
            to save mem and speed up code.
            save as numpy array such as train_texts and train_lable
        """

        # read training set, text to train.text, label to train.label
        # 注意：它们是numpy 数组
        train_text, train_label = self.read_from_disk(data_dir, "train", one_hot)

        # # shape[0]是行数
        # validation_size = 1
        # # validation_size = int(train_text.shape[0] / 8)
        # print("validation size is %d " % validation_size)
        #
        # cv_text = train_text[:validation_size, :]
        # cv_label = train_label[:validation_size, :]
        #
        # train_text = train_text[validation_size:, :]
        # train_label = train_label[validation_size:, :]

        print(train_text.shape)
        # print(train_text)
        print(train_label.shape)
        # print(train_label)

        self.train = dataset(train_text, train_label)
        # self.cv = dataset(cv_text, cv_label)

        return

    def read_test_data(self, data_dir, one_hot=False, dtype=tf.float32):
        """
            read datasets from test.txt and test_labels.txt
            cause all datasets is too large, read data separately
            to save mem and speed up code.
            save as numpy array such as test_texts and test_lable
        """

        test_text, test_label = self.read_from_disk(data_dir, "test", one_hot)
        self.test = dataset(test_text, test_label)
        return

    def read_from_disk(self, data_dir, data_type, one_hot=False):
        """
            read certain data from disk, data are been generated using
            data_prepare.py
        """
        print("read %s data from disk." % data_type)

        data_path = data_dir + "/" + data_type + ".txt"
        label_path = data_dir + "/" + data_type + "_labels.txt"

        with open(data_path) as f1, open(label_path) as f2:

            # get examples num using shell
            text_line_num = util.get_lines_of_file(data_path)
            label_line_num = util.get_lines_of_file(label_path)

            print("%s examples num=%d, labels num=%d" % (data_type, text_line_num, label_line_num))
            assert label_line_num == text_line_num, "label num and text num must be equal"

            text = numpy.zeros((text_line_num, INPUT_DIM))
            text_count = 0
            for line in f1:
                # print(line)
                # word list form str to int
                words = list(map(int, line.split()))
                # print("words" + str(words))

                text[text_count, :] = words
                text_count += 1

            labels = numpy.zeros((label_line_num, 1), dtype=numpy.uint8)
            label_count = 0
            for line in f2:
                label = map(int, line.split())
                labels[label_count, :] = list(label)
                label_count += 1

            labels[labels == OUTPUT_DIM] = 0
            if one_hot:
                labels = self.to_one_hot(labels)

            print("text.shape=" + str(text.shape))
            print("labels.shape=" + str(labels.shape))

            return text, labels

    def to_one_hot(self, labels, class_num=OUTPUT_DIM):
        """
            dense labels to one_hot vectors
        """
        label_num = labels.shape[0]
        offset = numpy.arange(label_num) * class_num
        labels_one_hot = numpy.zeros((label_num, class_num), dtype=numpy.uint8)
        labels_one_hot.flat[offset + labels.ravel()] = 1
        # print(labels_one_hot)
        return labels_one_hot


# if __name__ == '__main__':
#     d = datasets()
#     d.read_from_disk(".", "train", True)
#     d.read_from_disk(".", "test", True)
#     # d.read_data_sets(".", True)
#     # print d.train.next_batch(1)[1]
