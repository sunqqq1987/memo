#!/usr/bin/python
# -*-coding:utf-8-*-


def get_lines_of_file(file_path):
    count = 0
    with open(file_path, "r", encoding='utf-8') as fp:
        while 1:
            buffer = fp.read(8 * 1024 * 1024)
            if not buffer:
                break
            count += buffer.count('\n')

    return count
