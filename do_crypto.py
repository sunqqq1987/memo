#!/usr/bin/env python
# -*- coding: utf-8 -*-

# attention: need python3

import time
import os
import sys
# import chardet

import base64
from Crypto.Cipher import AES
from Crypto import Random

import re

from hashlib import md5, sha1
import shutil

BACKUP_FOLDER= 'BACKUP_FOLDER'
SKIP_PATH_KEYWORDS = ['\.git', BACKUP_FOLDER, 'igr_']

def getMd5(filename): #计算md5
    mdfive = md5()
    with open(filename, 'rb') as f:
        mdfive.update(f.read())
    return mdfive.hexdigest()

def getSha1(filename): #计算sha1
    sha1Obj = sha1()
    with open(filename, 'rb') as f:
        sha1Obj.update(f.read())
    return sha1Obj.hexdigest()

def get_key():

    key=""
    loop = 1
    while loop==1:
        # for python3
        key1 = input("Please input key:")
        key2 = input("Please input key again:")
        if key1 == key2:
            key=key1
            print("ok. key=" + key)
            loop = 0
        else:
            print("error! not same key")

    #check if it's len ==16
    len1 = len(key)
    if len1<16:
        a_char="1"
        i=len1+1
        while i<=16:
            key=key+a_char
            i=i+1
    else:
        key=key[0:16]
    
    print(key)

    return key

def decode_string(text):
    # print(chardet.detect(name)) # 找出文件名编码,文件名包含有中文,貌似不准确

    # only for python2
    # # 支持中文文件名
    # # windows下文件编码为GB2312，linux下为utf-8
    # try:
    #     decode_str = text.decode("GB2312")
    #     print ("use GB2312:" + decode_str)
    # except UnicodeDecodeError:
    #     print ("use utf-8")
    #     decode_str = text.decode("utf-8")
    # return decode_str

    return text


def encrypt_CBC(data, password):
    bs = AES.block_size # 16

    #pad = lambda s: s.decode("utf8","ignore") + (bs - len(s) % bs) * chr(bs - len(s) % bs)
    pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
    iv = Random.new().read(bs)
    cipher = AES.new(password, AES.MODE_CBC, iv)
    data = cipher.encrypt(pad(data))
    data = iv + data
    return data

def decrypt_CBC(data, password):
    bs = AES.block_size

    if len(data) <= bs:
        return data
    #unpad = lambda s: s[0:-ord(s[-1])]
    unpad = lambda s: s[0:-s[-1]]
    iv = data[:bs]
    cipher = AES.new(password, AES.MODE_CBC, iv)
    data = unpad(cipher.decrypt(data[bs:]))
    return data


def pad_to_16(text):
    #在尾部添加pad_num个pad_num
    pad_num = 16 - len(text) % 16
    i = 0
    while i < pad_num:
        #text += str(pad_num).encode()
        text += bytes([pad_num])
        i = i+1
    return text

def encrypt(data, password):
    aes = AES.new(password, AES.MODE_ECB)
    encrypt_aes = aes.encrypt(pad_to_16(data))
    encrypted_text = base64.encodebytes(encrypt_aes)
    return encrypted_text

def decrypt(data, password):
    unpad = lambda s: s[0:-s[-1]]
    aes = AES.new(password, AES.MODE_ECB)
    base64_decrypted = base64.decodebytes(data)
    decrypted_text = aes.decrypt(base64_decrypted)
    decrypted_text = unpad(decrypted_text)
    return decrypted_text

def check_is_skip(text):
    patternStr = ""
    i = 0
    for kw in SKIP_PATH_KEYWORDS:
        if i == 0:
            patternStr = patternStr + kw
        else:
            patternStr = patternStr + "|" + kw
        i = i + 1
    regexp = re.compile(patternStr, re.IGNORECASE | re.DOTALL)

    if regexp.search(text) != None:
        return 1
    else:
        return 0


def do_encrypt(FOLDER, out_folder):
    # must be 16 bytes long ，初始化密钥
    key=get_key()
    
    filename_list = []
    filepath_list = []
    for root, dirs, files in os.walk(FOLDER):
        for name in files:
            # print name

            # 支持中文文件名
            name = decode_string(name)

            filename_list.append(name)
            filepath_list.append(os.path.join(root, name))

    i = 0
    for filepath in filepath_list:
        # skip special file and folder
        is_skip = check_is_skip(filepath)

        if is_skip == 0:

            #check if changed or not
            bak_fld = FOLDER+"/"+BACKUP_FOLDER
            filepath_bk = filepath.replace(FOLDER, bak_fld)
            if os.path.exists(filepath) == True and os.path.exists(filepath_bk) == True and \
            getSha1(filepath) == getSha1(filepath_bk):
                #print('---skip unchanged: ' + filepath)
                pass
            else:
                # 注意：不能发现de或en的文件被删除的情况
                print('encrypt: ' + filepath)

                filepath_org = filepath

                test_string = filepath
                len1 = len(test_string)
                beSearch1 = '.'
                filepath_en=""
                try:
                    n1 = test_string.rindex(beSearch1)
                    postfix = filepath[n1 + 1:len1]
                    filepath_en = filepath[0:n1] + "_" + postfix + '.en'
                except:
                    n1 = len1
                    filepath_en = filepath[0:n1] + "_" + '.en'

                # 使用en路径
                p, f = os.path.split(filepath_en);
                p = p.replace(FOLDER, out_folder)
                if os.path.exists(p) == False:
                    os.makedirs(p)  # 先创建输出路径

                filepath_en = filepath_en.replace(FOLDER, out_folder)
                print("-----to: " + filepath_en)
                if os.path.exists(filepath_en):
                    os.remove(filepath_en)

                fp_en = open(filepath_en, 'wb')

                # filesize = os.path.getsize(filepath)

                fp_org = open(filepath_org, 'rb')
                msg = fp_org.read()
                en_msg = encrypt(msg, key)  #--------------
                # en_msg = base64.b64encode(en_msg)
                fp_org.close()

                fp_en.write(en_msg)
                fp_en.close()

                time.sleep(0.2)

        i = i + 1


def do_decrypt(FOLDER, out_folder):

    # must be 16 bytes long ，初始化密钥
    key=get_key()

    # 2. decrypt all the textfile
    filename_list = []
    filepath_list = []
    for root, dirs, files in os.walk(FOLDER):
        for name in files:
            # print name

            # 支持中文文件名
            name = decode_string(name)

            filename_list.append(name)
            filepath_list.append(os.path.join(root, name))

    i = 0
    for filepath in filepath_list:
        # only decrypt encrypted file
        if os.path.splitext(filepath)[1] == '.en':
            print('decrypt: ' + filepath)
            # continue

            filepath_en = filepath

            # decrypt
            test_string = filepath
            # len1 = len(test_string)
            beSearch1 = '_'
            n1 = test_string.rindex(beSearch1)
            beSearch1 = '.en'
            n2 = test_string.rindex(beSearch1)
            postfix = filepath[n1 + 1:n2]

            # len_postfix = len(".en")
            if postfix == "":
                filepath_de = filepath[0: n1]
            else:
                filepath_de = filepath[0: n1] + '.' + postfix
            

            # 使用de路径
            p, f = os.path.split(filepath_de);
            p1 = p.replace(FOLDER, out_folder)
            if os.path.exists(p1) == False:
                os.makedirs(p1)  # 先创建输出路径

            filepath_de = filepath_de.replace(FOLDER, out_folder)
            print("-----to: " + filepath_de)
            if os.path.exists(filepath_de):
                os.remove(filepath_de)

            fp_de = open(filepath_de, 'wb')

            # filesize = os.path.getsize(filepath)

            fp_en = open(filepath_en, 'rb')
            msg = fp_en.read()
            # msg = base64.b64decode(msg)
            de_msg = decrypt(msg, key)  #--------------
            fp_en.close()

            fp_de.write(de_msg)
            fp_de.close()

            time.sleep(0.2)

        i = i + 1

    # 拷贝一份到bakup folder
    bak_fld = out_folder+"/"+BACKUP_FOLDER
    if os.path.exists(bak_fld) == True:
        shutil.rmtree(bak_fld)  # 存在先删除
    shutil.copytree(out_folder, bak_fld)
    print ("\n copy folder:" + out_folder + " To backup folder:" +  bak_fld + ", done")
    

if __name__ == '__main__':

    if len(sys.argv) != 4:
        print("Argument is not right")
        exit()

    action = sys.argv[1]
    de_folder = sys.argv[2]
    en_folder = sys.argv[3]

    if os.path.exists(en_folder) == False:
        print("Error: en_folder: " + en_folder + " not exist")
        exit()

    if en_folder == de_folder:
        print("Error: en/de folder: " + en_folder + " should not same")
        exit()

    # 递归创建de目录， 如果不存在
    if os.path.exists(de_folder) == False:
        os.makedirs(de_folder)

    if action == "en":
        do_encrypt(de_folder, en_folder)
        print('do_encrypt, done')

    if action == "de":
        do_decrypt(en_folder, de_folder)
        print('do_decrypt, done')

    
