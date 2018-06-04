#!/usr/bin/python
# -*-coding:utf-8-*-

import numpy
import jieba
import os
import shutil
import math
import sys
import re

P_PATH = os.path.abspath(__file__)  # 获取当前程序的绝对路径
P_BASE_DIR = os.path.dirname(os.path.dirname(P_PATH))  # 获取当前程序的父目录的绝对路径
print("P_BASE_DIR=%s" % P_BASE_DIR)
sys.path.append(P_BASE_DIR + "\\src")  # 将BASE_DIR添加到系统环境变量中

import util


class textinfo():
    """
        file info of certain class, created for tf-idf.
        max_word_num: max number of words in the class file
        file_num: the number of files in the class
        word_map: key is word, and value is list which size is 2
                list[0] save wordcount, and list[1] saves tf-idf
    """

    def __init__(self):

        # save file num of the class
        self.file_num = 0  # 某类文本的文件总数

        # word map key is word, and value is list which size is 2
        # list[0] save wordcount in this class texts, list[1] is tf-idf
        # word_map 保存了该类文本的所有不重复的词汇的计数、以及f-idf
        self.word_map = {}
        self.max_word_num = 0  # 保存该类文档中出现次数最多的次的次数

    def update(self, words):
        """
            update class info in this function
            words: the new word list added
        """

        self.file_num += 1

        for w in words:
            if w not in self.word_map:
                self.word_map[w] = [0, 0]
            self.word_map[w][0] += 1  # 词的计数+1
            if self.word_map[w][0] > self.max_word_num:
                self.max_word_num = self.word_map[w][0]
        return

    def tf_idf(self, w, number_in_set, text_num):
        """
            compute word`s tf_idf
        """

        # tf是词频，= 某个词在某类文章中的出现次数/ 该类文章中出现次数最多的词的出现次数
        tf = 1.0 * self.word_map[w][0] / self.max_word_num

        # idf是逆文档频率，= log(语料库中的文档总数/ (包含该词的文档数+1))
        idf = math.log(1.0 * text_num / (number_in_set + 1))
        # print "tf is %f , idf is %f " %  (tf, idf)
        self.word_map[w][1] = tf * idf
        return

    def get_mainwords(self, n=500):
        """
            get n words from word_map, which sorted by tf-idf
            sort word_map first, return n words list,
            should called after tf_idf function
        """

        # sort word_map by tf-idf, sorted list is list of tuple ("key", list)
        sorted_list = sorted(self.word_map.items(), key=lambda d: d[1][1], reverse=True)

        print("len of sorted_list= %d" % len(sorted_list))

        assert len(sorted_list) >= n, "main words num n must > all words num in text."

        words_list = []
        for i in range(0, n):
            words_list.append(sorted_list[i][0])

        return words_list


class data_processor():
    """
        data preparation class,
        1. text split using jieba
        2. delete same and stop words.
        2. generate dict.
        3. generate data(test and train) vector.
    """

    def __init__(self):

        # 文本分类名和label值
        self.class_label_dict = {"科技": "1", "娱乐": "2", "体育": "3", "财经": "4", "汽车": "5"}

        # 停用词文件
        self.stop_words_file = r"..\dict\stop_words_ch.txt"

        # 从训练数据中获取的每类中的最高频的前500词，共：类数*500
        self.words_dict_file = r"..\src\train_words_dict.txt"

    def get_unique_id(self, file_path):
        """
            get file unique id format as {class_id}_type_{text_id}.txt.
            file_path is the full path of file
              e.g ./training_set/科技/text1343.txt
            where "training" is type, id of "科技" is file class, and "text1343" is text id.
            modify this function to adapt your data dir format
        """

        dir_list = file_path.split('\\')
        # print(dir_list)

        type_id = dir_list[1].split("_")[0]
        class_name = dir_list[2]
        class_id = self.class_label_dict[class_name]  # 1~5
        text_id = dir_list[3].split(".")[0]

        return class_id + "_" + type_id + "_" + text_id

    # 分词：将data_dir目录的所有文件分词，最后都保存到data_type.txt中
    def split_words(self, data_dir, data_type_file):
        """
            split word for all files under data_dir
            save data as <class_{data_type}_id> <words> in ./{data_type}.txt,
            where data_type is train, test or cv.
            output: {data_type}.txt includes all map of  file unique id and file words.
        """

        if os.path.exists(data_type_file):
            os.remove(data_type_file)

        list_dirs = os.walk(data_dir)
        for root, _, files in list_dirs:
            print(root)
            # get all files under data_dir
            for fp in files:
                file_path = os.path.join(root, fp)
                # print("file_path=" + file_path)

                # 获取文件的唯一ID
                file_id = self.get_unique_id(file_path)

                # split words for f, save in file ./data_type.txt
                with open(file_path, encoding='UTF-8') as f1, open(data_type_file, "a+", encoding='UTF-8') as f2:
                    all_lines = f1.readlines()
                    # print(all_lines)

                    data = ""
                    # del url part in text file
                    for line in all_lines:
                        if re.match(r'https://', line) is None and re.match(r'http://', line) is None:
                            data = data + line + "\n"

                    # print("data=" + data)
                    # exit()

                    # 调用分词库jieba
                    jieba.load_userdict('../dict/user_dict.txt')
                    seg_list = jieba.cut(data, cut_all=False)

                    # 输出分词后的当前文件内容为一行，格式为:<class_{data_type}_id> < words >
                    f2.write(file_id + " " + " ".join(seg_list).replace("\n", " ") + "\n")

        print("split word for %s file end." % data_type_file)
        return

    # 删除停用词：将file_path中包含stop_words_file里的停用词删除
    def del_stopwords(self, file_path):
        """
            rm stop word for {file_path}, stop words save in {stop_words_file} file.
            file_path: file path of file generated by function split_words.
                        each lines of file is format as <file_unique_id> <file_words>.
            stop_words_file: file containing stop words, and every stop words in one line.
            output: file_path which have been removed stop words and overwrite original file.
        """

        # read stop word dict and save in stop_dict
        stop_dict = {}
        with open(self.stop_words_file, encoding='UTF-8') as d:
            for word in d:
                stop_dict[word.strip("\n")] = 1

        # remove tmp file if exists
        if os.path.exists(file_path + ".tmp"):
            os.remove(file_path + ".tmp")

        print("now remove stop words in %s." % file_path)
        # read source file and rm stop word for each line.
        with open(file_path, encoding='UTF-8') as f1, open(file_path + ".tmp", "a+", encoding='UTF-8')as f2:
            for line in f1:
                tmp_list = []  # save words not in stop dict
                words = line.split()
                for word in words[1:]:
                    if word not in stop_dict:
                        tmp_list.append(word)
                words_without_stop = " ".join(tmp_list)
                f2.write(words[0] + " " + words_without_stop + "\n")

        # overwrite origin file with file been removed stop words
        shutil.move(file_path + ".tmp", file_path)
        print("stop words in %s has been removed." % file_path)
        return

    # 生成词典：根据file_path，生成代表所有类型的文本的词典
    def gen_words_dict(self, file_path, words_dict_file):
        """
            generate key words dict for text using tf_idf algorithm.
            file_path: file have been removed stop words, each lines
                       of file is format as <file_unique_id> <file_words>.
            output: words_dict.txt, each line in this file is a word
        """

        # save textinfo by class id
        class_dict = {}
        # all train text num
        text_num = 0
        # save map of word and number of files includes the word
        word_in_files = {}
        with open(file_path, encoding='UTF-8') as f:
            for line in f:
                text_num += 1
                words = line.split()
                # words[0] is {class_id}_type_id
                class_id = words[0].split("_")[0]
                if class_id not in class_dict:
                    class_dict[class_id] = textinfo()  #

                class_dict[class_id].update(words[1:])

                # update word_in_files
                flags = {}
                for w in words[1:]:
                    if w not in word_in_files:
                        word_in_files[w] = 0
                    if w not in flags:
                        flags[w] = False

                    if flags[w] is False:
                        word_in_files[w] += 1
                        flags[w] = True
            print("save textinfo according to class id is over.")

        if os.path.exists(self.words_dict_file):
            os.remove(self.words_dict_file)

        total_file_num = 0
        for k, text_info in class_dict.items():
            total_file_num = total_file_num + text_info.file_num

            print("class %s has %d files" % (k, text_info.file_num))
            # get tf_idf in words of class k
            for w in text_info.word_map:
                text_info.tf_idf(w, word_in_files[w], text_num)

            # 将词频最高的前500个词输出到词典。如果一共10类的话，最后生成有5000个词的词典
            with open(self.words_dict_file, "a+", encoding='UTF-8') as f:
                main_words = text_info.get_mainwords()
                print("class %s main words num: %d" % (k, len(main_words)))

                f.write("\n".join(main_words) + "\n")

        print("total_file_num= %d" % total_file_num)
        print("gen word dict to: %s." % self.words_dict_file)
        return

    # 生成词袋： 利用生成的词典，将以行为单位将去停用词后的每个文本文件转换为5000向量
    # 同时生成data_type_labels.txt来保存每个文件的真实标签值
    def gen_wordbag(self, file_path, data_type):
        """
            generate wordbag by using words_dict_file.txt.
            output: {data_type_bag.txt}, lines in the file is
                <file_unique_id> <words_vector>. each position of
                words_vector is match the words_dict_file.txt. the value
                of words_vector is number of words appearing in file.

        """

        # read words_dict_file.txt
        dict_list = []
        with open(self.words_dict_file, encoding='UTF-8') as d:
            for line in d:
                dict_list.append(line.strip("\n"))

        # print("len(dict_list)=%s" % len(dict_list))

        base_path = os.path.abspath(os.path.dirname(file_path))
        label_file_path = base_path + "//" + data_type + "_labels.txt"
        # remove tmp file if exists
        if os.path.exists(file_path + ".tmp"):
            os.remove(file_path + ".tmp")
        if os.path.exists(label_file_path):
            os.remove(label_file_path)

        class_ids = []
        # gen vector format of data_set, overwrite origin {file_path}
        with open(file_path, encoding='UTF-8') as f1, open(file_path + ".tmp", "a+", encoding='UTF-8') as f2:
            for line in f1:
                # tmp vector of one text
                word_vector = []
                for i in range(0, len(dict_list)):
                    word_vector.append(0)

                words = line.split()
                # words[0] is {class_id}_type_id
                class_id = words[0].split("_")[0]
                class_ids.append(class_id)

                # 如果当前文件的当前行的当前单词 在data_type的词典中，那么在该文本的5000维向量中对应该词的位置，计数+1
                for w in words[1:]:
                    if w in dict_list:
                        word_vector[dict_list.index(w)] += 1

                # 并将该文本向量以追加方式写入一行到data_type.tmp文件.
                # 最终生成的data_type.tmp文件: 行数为文本数，列为5000。
                f2.write(" ".join(map(str, word_vector)) + "\n")

                # print("len(word_vector)=%s" % len(word_vector))
                # print(word_vector)

        # 生成data_type_label.txt文件：行数是文本数，1列，列值是文件的分类（1~10）
        with open(label_file_path, "a+", encoding='UTF-8') as lb:
            lb.write("\n".join(class_ids) + "\n")

        if os.path.exists(file_path + ".splt"):
            os.remove(file_path + ".splt")
        shutil.move(file_path, file_path + ".splt")
        shutil.move(file_path + ".tmp", file_path)

        print("gen word bag to: %s." % file_path)
        return

    def shuffle_data(self, data_dir, data_type):

        data_path = data_dir + "//" + data_type + ".txt"
        label_path = data_dir + "//" + data_type + "_labels.txt"

        # 保存随机后的数据
        r_label_list = []
        r_text_list = []

        with open(data_path, encoding='UTF-8') as f1, open(label_path, encoding='UTF-8') as f2:
            text_line_num = util.get_lines_of_file(data_path)
            label_line_num = util.get_lines_of_file(label_path)

            print("%s examples num=%d, labels num=%d" % (data_type, text_line_num, label_line_num))
            assert label_line_num == text_line_num, "label num and text num must be equal"

            label_list = []
            text_list = []

            for line in f1:
                text_list.append(line)

            for line in f2:
                label_list.append(line)

            arr_r = numpy.arange(text_line_num)
            numpy.random.shuffle(arr_r)

            for i in arr_r:
                r_label_list.append(label_list[i])
                r_text_list.append(text_list[i])

        # 重命名
        bsf_data_path = data_path + ".bsf"
        if os.path.exists(bsf_data_path):
            os.remove(bsf_data_path)
        shutil.move(data_path, bsf_data_path)

        bsf_label_path = label_path + ".bsf"
        if os.path.exists(bsf_label_path):
            os.remove(bsf_label_path)
        shutil.move(label_path, bsf_label_path)

        # 写入随机后的数据
        with open(data_path, "a+", encoding='UTF-8') as f1, open(label_path, "a+",
                                                                 encoding='UTF-8') as f2:
            for ea in r_text_list:
                f1.write(ea)

            for ea in r_label_list:
                f2.write(ea)

        print("shuffle %s data done" % data_type)


if __name__ == '__main__':
    """
        remove the annotations below to generate origin data
        for training and test, if you already has dic
        data_pre.gen_words_dict("train.txt") will not needed
        all commends should been called one time. 
        datasets are in ../
    """
    data_pre = data_processor()

    # path need using '\' on windows
    data_pre.split_words(r"..\training_set", r"..\src\train.txt")
    data_pre.del_stopwords(r"..\src\train.txt")
    # 生成词典
    data_pre.gen_words_dict(r"..\src\train.txt", r"..\dict\words_dict.txt")
    data_pre.gen_wordbag(r"..\src\train.txt", "train")
    # 数据随机
    data_pre.shuffle_data(r"..\src", "train")

    # exit()
    print("=========================")

    data_pre.split_words(r"..\testing_set", r"..\src\test.txt")
    data_pre.del_stopwords(r"..\src\test.txt")
    data_pre.gen_wordbag(r"..\src\test.txt", "test")
    # 数据随机
    data_pre.shuffle_data(r"..\src", "test")
