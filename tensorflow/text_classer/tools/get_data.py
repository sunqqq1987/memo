# -*- coding: utf-8 -*-

# import sys

# python3不需要以下2行
# reload(sys)
# sys.setdefaultencoding('utf-8')

# print(sys.getdefaultencoding())

import time
import re
import datetime

import os
from selenium import webdriver
from bs4 import BeautifulSoup

parsed_page_classes = ["科技", "财经", "娱乐", "体育", "财经", "汽车"]

phantomjs_path = r'C:\ProgramData\Anaconda3\envs\tensorflow_env\Scripts\phantomjs-2.1.1\phantomjs.exe'

# 关闭图片加载，开启缓存，忽略https错误
phantomjs_service_args = ['--load-images=no', '--disk-cache=yes', '--ignore-ssl-errors=true']


def get_time_string():
    # 获得当前时间
    now = datetime.datetime.now()
    cur_time_str = now.strftime("%Y-%m-%d_%H_%M_%S")

    return cur_time_str


def correct_title(title):
    # correct title
    tmp = title.strip()
    # 去掉中间的空格
    tmp = tmp.replace(" ", "_")
    # filter invalid chars: \ / : * ？ " < > | for filename
    invalid_chars = ["\\", "/", ":", "*", "\"", "?", "<", ">", "|"]
    for ch in invalid_chars:
        tmp = tmp.replace(ch, "")
    len1 = len(tmp)
    if len1 > 50:
        tmp = tmp[0:50]

    return tmp


def toutiao_spider():
    # need to download phantomjs from http://phantomjs.org/download.html
    browser = webdriver.PhantomJS(executable_path=phantomjs_path, service_args=phantomjs_service_args)

    # 是否允许覆盖已经存在的文件
    IS_overwrite = 0

    local_base_path = os.getcwd() + "\\test_data\\"
    print("local_base_path=" + local_base_path)

    BASE_URL = 'https://www.toutiao.com'

    browser.get(BASE_URL)
    time.sleep(10)

    cur_page_src = browser.page_source

    soup = BeautifulSoup(cur_page_src, "html.parser")

    # map of class name and url
    class_name_url_dict = {}

    # <a href="/" target="_self" ga_event="channel_recommand_click" class="channel-item"><span>科技</span></a>
    channel_items = soup.find_all("a", attrs={"class": "channel-item"})
    for ea in channel_items:
        # print(ea)
        channel = ea.get_text()
        if channel in parsed_page_classes:
            url = BASE_URL + ea["href"]
            if channel not in class_name_url_dict:
                class_name_url_dict[channel] = url
                print(channel + ": " + class_name_url_dict[channel])

    # exit()  # debug

    # news list file
    time_as_title = get_time_string()
    file_path2 = local_base_path + "toutiao_news_list_" + time_as_title + ".txt"
    # print("file_path2=" + file_path2)
    fp2 = open(file_path2, 'w', encoding='UTF-8')

    news_content = ""
    idx_u = 0
    for ea_class_name, ea_class_url in class_name_url_dict.items():
        print("")

        browser.get(ea_class_url)
        time.sleep(5)

        # class_base_path = local_base_path + str(idx_u) + "_" + ea_class_name + "\\"
        class_base_path = local_base_path + ea_class_name + "\\"
        if os.path.exists(class_base_path) is False:
            os.mkdir(class_base_path)  # create

        # scroll to get more enough news
        scroll_count = 1
        while scroll_count <= 3:
            step = 10000 * scroll_count
            js = "var q=document.body.scrollTop=" + str(step)
            browser.execute_script(js)
            time.sleep(5)

            # file_path = class_base_path + "page_shot_" + str(idx_u) + "_" + str(scroll_count) + ".png"
            # browser.get_screenshot_as_file(file_path)

            scroll_count = scroll_count + 1

        # # save page source code
        # file_path = local_base_path + "toutiao_page_source_" + ea_class_name + ".txt"
        # print("page_source=" + file_path)
        # fp = open(file_path, 'w', encoding='UTF-8')
        # fp.write(browser.page_source)
        # fp.close()

        # parse with bs4
        cur_page_src = browser.page_source
        soup = BeautifulSoup(cur_page_src, "html.parser")

        # map of article name and url
        art_title_url_dict = {}

        # news list info
        news_content = news_content + "\n==========================" + ea_class_name + "============================\n"
        news_content = news_content + "\n link_titles: \n"

        # <div class="title-box" ga_event="wenda_title_click">
        #    <a class="link title"
        cnt = 0
        link_titles = soup.find_all("div", attrs={"class": "title-box"})
        for ea in link_titles:
            # print(ea)
            ga_event = ea["ga_event"]

            # skip cases
            is_skip = 0
            # if ga_event == "wenda_title_click":   # 问答
            #     is_skip = 1

            a_item = ea.find("a", attrs={"class": "link title"})
            title = a_item.get_text()

            url = a_item["href"]

            AD_STR = ""
            if re.search("http", url) is not None:
                AD_STR = "[广告]"
                news_content = news_content + AD_STR + title + " " + url + "\n"
            elif is_skip == 0:
                news_content = news_content + title + " " + BASE_URL + url + "\n"
                if title not in art_title_url_dict:
                    art_title_url_dict[title] = BASE_URL + url
                    cnt = cnt + 1
                    print("[" + str(cnt) + "] " + title + ": " + art_title_url_dict[title])

        print("---parsing article---" + ea_class_name)

        # parse each article
        for ea_title, ea_url in art_title_url_dict.items():
            ea_title = ea_title.strip()

            # # debug
            # ea_title = "2018年农村养老金，涨了多少钱？"
            # ea_url = "https://www.toutiao.com/a6534155934317412611/"

            # correct title
            new_title = correct_title(ea_title)
            # print(" new_title=" + new_title)

            file_path = class_base_path + new_title + ".txt"

            if os.path.exists(file_path) is False or IS_overwrite == 1:

                browser.get(ea_url)
                time.sleep(10)
                cur_page_src = browser.page_source
                soup = BeautifulSoup(cur_page_src, "html.parser")

                # 文本的第一行是title, 之后是正文
                content = ea_title + "\n"
                content = content + ea_url + "\n"

                # <div class="article-content">
                article_content_items = soup.find_all("div", attrs={"class": "article-content"})
                for ea in article_content_items:
                    content = content + ea.get_text() + "\n"

                # special case 1: 微信正文
                if len(article_content_items) == 0:
                    # <article tt-ignored-node="1">
                    article_content_items = soup.find_all("article", attrs={"tt-ignored-node": "1"})
                    for ea in article_content_items:
                        content = content + ea.get_text() + "\n"

                    # special case 2： 问答
                    if len(article_content_items) == 0:
                        # <div data-node="answer-item" data-ansid="6452910758614270222" class="answer-item sticky-item">
                        #     <div class="answer-text-full rich-text">
                        article_content_items = soup.find_all("div", attrs={"class": "answer-item sticky-item"})
                        for ea in article_content_items:
                            text_item = ea.find("div", attrs={"class": "answer-text-full rich-text"})
                            content = content + text_item.get_text() + "\n"

                        # special case 3：
                        if len(article_content_items) == 0:
                            # <article>
                            #   <div class="content">
                            article_content_items = soup.select('article > div[class="content"]')
                            for ea in article_content_items:
                                content = content + ea.get_text() + "\n"

                            # special case 4：
                            if len(article_content_items) == 0:
                                # <article>
                                #   <p>
                                article_content_items = soup.select('article > p')
                                for ea in article_content_items:
                                    content = content + ea.get_text() + "\n"

                # save to file
                fp = open(file_path, 'w', encoding='UTF-8')
                fp.write(content)
                fp.close()

                print(ea_title + ": " + ea_url)
                print(" =>" + file_path)

            # exit()  # debug

        idx_u = idx_u + 1

    fp2.write(news_content)
    fp2.close()

    browser.quit()


def yidian_spider():
    # need to download phantomjs from http://phantomjs.org/download.html
    browser = webdriver.PhantomJS(executable_path=phantomjs_path, service_args=phantomjs_service_args)

    # browser = webdriver.PhantomJS(executable_path=phantomjs_path)

    # 是否允许覆盖已经存在的文件
    IS_overwrite = 0

    local_base_path = os.getcwd() + "\\test_data\\"
    print("local_base_path=" + local_base_path)

    BASE_URL = 'http://www.yidianzixun.com'

    # start = datetime.datetime.now()

    browser.get(BASE_URL)
    time.sleep(10)

    # end = datetime.datetime.now()
    # # 计算耗时
    # print('%s s' % (end - start).total_seconds())

    cur_page_src = browser.page_source

    soup = BeautifulSoup(cur_page_src, "html.parser")

    # map of class name and url
    class_name_url_dict = {}

    # <div class="channel-nav">
    #  <div class="list">
    #     <a data-index="12" href="/channel/c5" data-channelid="12852854159" class="item">
    channel_items = soup.find_all("a", attrs={"class": "item", "data-channelid": True})
    for ea in channel_items:
        # print(ea)
        channel = ea.get_text()
        if channel in parsed_page_classes:
            url = BASE_URL + ea["href"]
            if channel not in class_name_url_dict:
                class_name_url_dict[channel] = url
                print(channel + ": " + class_name_url_dict[channel])

    # print(len(channel_items))

    # news list file
    time_as_title = get_time_string()
    file_path2 = local_base_path + "yidian_news_list_" + time_as_title + ".txt"
    # print("file_path2=" + file_path2)
    fp2 = open(file_path2, 'w', encoding='UTF-8')

    news_content = ""
    idx_u = 0
    for ea_class_name, ea_class_url in class_name_url_dict.items():
        print("")

        browser.get(ea_class_url)
        time.sleep(5)

        class_base_path = local_base_path + ea_class_name + "\\"
        if os.path.exists(class_base_path) is False:
            os.mkdir(class_base_path)  # create

        # scroll to get more enough news
        scroll_count = 1
        while scroll_count <= 3:
            step = 10000 * scroll_count
            js = "var q=document.body.scrollTop=" + str(step)
            browser.execute_script(js)
            time.sleep(5)
            # browser.refresh()
            # time.sleep(3)

            # file_path = class_base_path + "page_shot_" + str(idx_u) + "_" + str(scroll_count) + ".png"
            # browser.get_screenshot_as_file(file_path)

            scroll_count = scroll_count + 1

        # save page source code
        file_path = local_base_path + "yidian_page_source_" + ea_class_name + ".txt"
        print("page_source=" + file_path)
        fp = open(file_path, 'w', encoding='UTF-8')
        fp.write(browser.page_source)
        fp.close()

        # parse with bs4
        cur_page_src = browser.page_source
        soup = BeautifulSoup(cur_page_src, "html.parser")

        # map of article name and url
        art_title_url_dict = {}

        # news list info
        news_content = news_content + "\n==========================" + ea_class_name + "============================\n"
        news_content = news_content + "\n link_titles: \n"

        # <div class="channel-news channel-news-0">
        #   <a class="item doc style-small-image style-content-middle" href="/article/0IZYzk8n" target="_blank">
        #      <div class="doc-title">7座以下私家车将取消年检？“捆绑式年检”到底有多坑！</div>
        link_titles = soup.find("div", attrs={"class": "channel-news channel-news-0"})
        if link_titles is None:
            # special case happen sometimes
            link_titles = soup.find("div", attrs={"class": "channel-news"})

        cnt = 0
        link_titles = link_titles.findAll("a")
        for ea in link_titles:
            # print(ea)

            skip = 0
            # skip special case: video, because of no context

            # <div class="video-time">01:13</div>
            if ea.find("div", attrs={"class": "video-time"}) is not None:
                skip = 1

            url = ea["href"]
            title = ea.find("div", attrs={"class": "doc-title"})
            title = title.get_text()

            news_content = news_content + title + " " + BASE_URL + url + "\n"
            if skip == 0 and title not in art_title_url_dict:
                art_title_url_dict[title] = BASE_URL + url
                cnt = cnt + 1
                print("[" + str(cnt) + "] " + title + ": " + art_title_url_dict[title])

        # exit()

        print("---parsing article---" + ea_class_name)

        # parse each article
        for ea_title, ea_url in art_title_url_dict.items():
            ea_title = ea_title.strip()

            # debug
            # ea_url = "http://m2.people.cn/r/MV8xXzI5ODYxMTk5XzQwNjA2XzE1MjA4MDg3NjQ=?tt_group_id=6531828458270491150"

            # correct title
            new_title = correct_title(ea_title)
            # print(" new_title=" + new_title)

            file_path = class_base_path + new_title + ".txt"

            if os.path.exists(file_path) is False or IS_overwrite == 1:

                browser.get(ea_url)
                time.sleep(10)
                cur_page_src = browser.page_source
                soup = BeautifulSoup(cur_page_src, "html.parser")

                # 文本的第一行是title, 之后是正文
                content = ea_title + "\n"
                content = content + ea_url + "\n"

                # <div class="content-bd">
                article_content_items = soup.find_all("div", attrs={"class": "content-bd"})
                for ea in article_content_items:
                    content = content + ea.get_text() + "\n"

                # special case 1：北青网
                if len(article_content_items) == 0:
                    # <article>
                    #   <div>
                    #     <p>
                    article_content_items = soup.select('article > div > p')
                    for ea in article_content_items:
                        content = content + ea.get_text() + "\n"

                    # special case 2：视觉中国综合
                    if len(article_content_items) == 0:
                        # <article class ="yidian-content">
                        #    <figure>
                        article_content_items = soup.select('article > figure')
                        for ea in article_content_items:
                            content = content + ea.get_text() + "\n"

                # save to file
                fp = open(file_path, 'w', encoding='UTF-8')
                fp.write(content)
                fp.close()

                print(ea_title + ": " + ea_url)
                print(" =>" + file_path)

            # exit()  # debug

        # exit()

        idx_u = idx_u + 1

    fp2.write(news_content)
    fp2.close()

    browser.quit()


if __name__ == "__main__":

    # toutiao_spider()
    # exit()

    print("=========================================")

    count = 0
    while count < 3:
        toutiao_spider()
        print("toutiao done.")
        time.sleep(10)

        print("")
        yidian_spider()
        print("yidian done.")
        time.sleep(10)

        count = count + 1