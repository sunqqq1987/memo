#!/usr/bin/python
# -*-coding:utf-8-*-
"""
	PCA for datasets
	
"""
import os
import sys
import numpy
from datasets import datasets

K_DIM = 1000
ORIGIN_DIM = 2500


def test():
    num1 = numpy.array([[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]])
    print(num1)
    print(numpy.mean(num1))  # 对所有元素求均值
    print(numpy.mean(num1, 0))  # 压缩行，对各列求均值
    print(numpy.mean(num1, 1))  # 压缩列，对各行求均值


def pca(origin_mat):
    """
    gen matrix using pca
    row of origin_mat is one sample of dataset
    col of origin_mat is one feature
    return matrix  U, s and  V
    """
    # mean,normalization
    avg = numpy.mean(origin_mat, axis=0)  # 压缩行，对各列求均值, 输出是一个行向量
    # covariance matrix
    cov = numpy.cov(origin_mat - avg, rowvar=0)  # 协方差cov
    # Singular Value Decomposition.奇异值分解SVD
    U, s, V = numpy.linalg.svd(cov, full_matrices=True)

    k = 1
    sigma_s = numpy.sum(s)
    # chose smallest k for 99% of variance retained
    for k in range(1, ORIGIN_DIM + 1):
        variance = numpy.sum(s[0:k]) / sigma_s
        print("k = %d, variance is %f" % (k, variance))
        if variance >= 0.99:
            break

    if k == ORIGIN_DIM:
        print("something unexpected , k is same as ORIGIN_DIM")
        exit(1)

    return U[:, 0:k], k


if __name__ == '__main__':
    """
        main, read train.txt, and do pca
        save file to train_pca.txt
    """
    # test
    # test()
    # exit()

    data_sets = datasets()
    train_text, _ = data_sets.read_from_disk(".", "train", one_hot=False)

    U, k = pca(train_text)
    print("U shape: ", U.shape)
    # 注意：这里的K值就是降维后的维度？
    print("k is : ", k)

    text_pca = numpy.dot(train_text, U)
    text_num = text_pca.shape[0]
    print("text_num in pca is ", text_num)

    with open("./train_pca.txt", "a+") as f:
        for i in range(0, text_num):
            f.write(" ".join(map(str, text_pca[i, :])) + "\n")
