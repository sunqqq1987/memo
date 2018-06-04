# -*-coding:utf-8-*-


import os
import sys
import time
import datetime
import re

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

MY_NAME = "xx"
MY_PWD = "xx"


def study_now(browser, local_base_path):
    print("-----开始学习章节")

    tmp_idx = 0

    while 1:
        # --------1------------
        # 捕获各种中断情况:
        # 1）提示，继续学习
        # 2）中途停顿，弹出是否继续学习
        # 3）当前章不是最后一章

        browser.switch_to.frame(0)

        cur_page_src = browser.page_source
        soup = BeautifulSoup(cur_page_src, "html.parser")
        # <div id="newMash" class="mask" style="display: none;">
        #  <div id="newTips" class="tips"><p>检测到您上次未学完，是否继续学习！</p><div>
        #  是否进入下一章节继续学习！
        #    <a href="javascript:void(0);">继续学习</a>
        #    <a href="javascript:void(0);">重新学习</a>
        newMash = soup.find("div", attrs={"id": "newMash", "class": "mask", "style": True})
        if newMash is not None:
            styl = newMash["style"]
            if styl != "display: none;":

                tip = soup.find("div", attrs={"id": "newTips", "class": "tips"})
                if tip is not None:
                    all_text = tip.get_text()
                    time_str = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")

                    if re.search("是否进入下一章节继续学习", all_text) is not None:
                        print("进入下一章节继续学习, %s", time_str)
                        time.sleep(3)
                        break
                    else:
                        print("tip shows, 继续学习, %s", time_str)
                        t2 = browser.find_element_by_id("newTips")
                        link = t2.find_element_by_link_text("继续学习")
                        # print(link)
                        link.click()

        # --------2------------
        # 捕获课程都学习完时弹出的评价窗口

        browser.switch_to.default_content()

        # # save page source code
        # file_path = local_base_path + "studying_" + str(tmp_idx) + ".txt"
        # print("page_source=" + file_path)
        # fp = open(file_path, 'w', encoding='UTF-8')
        # fp.write(browser.page_source)
        # fp.close()

        cur_page_src = browser.page_source
        soup = BeautifulSoup(cur_page_src, "html.parser")
        # <div class="layui-layer-content">
        #     <a class="layui-layer-close"><img src="http://static.yun.chinahrt.com/images/lms/zbpj_05.jpg"></a>
        # <span class="layui-layer-setwin">
        #   <a class="layui-layer-ico layui-layer-close layui-layer-close2" href="javascript:;"></a></span>
        layui_content = soup.find("div", attrs={"class": "layui-layer-content"})
        layui_setwin = soup.find("span", attrs={"class": "layui-layer-setwin"})

        if layui_content is not None and layui_setwin is not None:
            layer_close = layui_content.find("a", attrs={"class": "layui-layer-close"})
            if layer_close is not None:
                # setwin = browser.find_element_by_class_name("layui-layer-setwin") # failed
                clos = browser.find_element_by_class_name("layui-layer-close")
                clos.click()
                time_str = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
                print("课程结束, %s", time_str)
                time.sleep(3)

                # # 回退，先回到章节界面
                # browser.back()
                # time.sleep(5)
                break

        tmp_idx = tmp_idx + 1
        if tmp_idx > 2:
            tmp_idx = 0

        time.sleep(10)


def chinahrt_auto_study():
    # --------launch browser
    # for firefox
    # need download geckodriver from https://github.com/mozilla/geckodriver/releases
    # cus_profile_dir= r"D:\tool\firefox\ssl-p3"
    # browser= webdriver.Firefox(cus_profile_dir)

    # cus_profile_dir = r"C:\Users\Administrator\AppData\Roaming\Mozilla\Firefox\Profiles\39nt23v3.defaul31838133"
    # browser = webdriver.Firefox(cus_profile_dir)
    # # browser = webdriver.Firefox()

    # 创建Firefox浏览器的一个Options实例对象
    # profile = webdriver.FirefoxProfile(r"D:\tool\firefox\p3")
    profile = webdriver.FirefoxProfile()
    # 启用flash插件
    profile.set_preference('plugin.state.flash', 2)
    # 启动带有自定义设置的Firefox浏览器
    browser = webdriver.Firefox(profile)

    # chrome
    # chromedriver = "C:\chromedriver\chromedriver.exe"
    # os.environ["webdriver.chrome.driver"] = chromedriver
    # # option = webdriver.ChromeOptions()
    # # default user profile
    # # option.add_argument('--user-data-dir=C:\Users\Admin\AppData\Local\Google\Chrome\User Data')
    #
    # prefs = {"profile.default_content_setting_values.plugins": 1,
    #          "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
    #          "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,
    #          "credentials_enable_service": False,
    #          "profile.password_manager_enabled": False}
    # browser = webdriver.Chrome(chromedriver, prefs=prefs)

    local_base_path = os.getcwd() + "\\"
    print("local_base_path=" + local_base_path)

    # BASE_URL = 'http://hbzj.chinahrt.com/'
    BASE_URL = 'http://yun.chinahrt.com'

    browser.get(BASE_URL)
    time.sleep(6)

    # # save page source code
    # file_path = local_base_path + "main.txt"
    # print("page_source=" + file_path)
    # fp = open(file_path, 'w', encoding='UTF-8')
    # fp.write(browser.page_source)
    # fp.close()

    # browser.maximize_window()  #将浏览器最大化显示

    # 模拟click 'javascript:;'
    # cur_page_src = browser.page_source
    # soup = BeautifulSoup(cur_page_src, "html.parser")
    #
    # # <span class ="layui-layer-setwin">
    # #    <a class="layui-layer-ico layui-layer-close layui-layer-close1" href="javascript:;"></a>
    # popup_icon = soup.find("a", attrs={"class": "layui-layer-ico layui-layer-close layui-layer-close1"})
    # if popup_icon is None:
    #     print("no popup_icon!")
    #     exit()
    # else:
    #     print(popup_icon)
    #
    # setwin = browser.find_element_by_class_name("layui-layer-setwin")
    # # find_element_by_css_selector("span>input")
    # # print(setwin)
    # setwin.click()
    # print("close popup_icon done.")
    # time.sleep(10)

    # # save page source code
    # file_path = local_base_path + "main_login.txt"
    # print("page_source=" + file_path)
    # fp = open(file_path, 'w', encoding='UTF-8')
    # fp.write(browser.page_source)
    # fp.close()

    # <input placeholder="请输入您的用户名" name="UserName" id="UserName" type="text">
    # <input placeholder="请输入您的密码" name="Password" id="Password" type="password">
    # < input class ="lg-btn" value="登录" id="logbtn" type="button" >
    WebDriverWait(browser, 30).until(lambda x: x.find_element_by_id("UserName").is_displayed())
    browser.find_element_by_id("UserName").send_keys(MY_NAME)
    WebDriverWait(browser, 30).until(lambda x: x.find_element_by_id("Password").is_displayed())
    browser.find_element_by_id("Password").send_keys(MY_PWD)

    is_done = input("input checksum done?:\n")
    print(is_done)
    if is_done != "1":
        print("checksum not done.")
        exit()

    WebDriverWait(browser, 30).until(lambda x: x.find_element_by_id("logbtn").is_displayed())
    browser.find_element_by_id("logbtn").click()
    time.sleep(6)
    print("send account done.")

    WebDriverWait(browser, 30).until(lambda x: x.find_element_by_link_text("学习中").is_displayed())
    browser.find_element_by_link_text("学习中").click()
    time.sleep(5)
    print("click 学习中 done.")

    # # ----------test------------
    # browser.get('http://yun.chinahrt.com/studentCoursePage/chapterDetail/a02d16de-0cb8-4947-95dd-5c9f020ac18e')
    # time.sleep(7)
    # study_now(browser, local_base_path)
    #
    # browser.get('http://yun.chinahrt.com/studentCoursePage/chapterDetail/bcdd0a99-732b-487b-a64c-21391faaa89e')
    # time.sleep(7)
    # study_now(browser, local_base_path)
    #
    # exit()

    # # save page source code
    # file_path = local_base_path + "学习中.txt"
    # print("page_source=" + file_path)
    # fp = open(file_path, 'w', encoding='UTF-8')
    # fp.write(browser.page_source)
    # fp.close()

    # 年度培训计划列表---------
    # <div class="fr finish-txt">
    #   <h2 onclick="selectCourse('0dc.');"><a href="javascript:;">..人员公需科目继续教育培训计划</a></h2>
    #   <div class="finish-bar"><a href="#" onclick="selectCourse('bf22c-aaf8-5127dd420f29');"> 去学习</a></div>
    cur_page_src = browser.page_source
    soup = BeautifulSoup(cur_page_src, "html.parser")

    train_list = soup.select('div > h2')
    finish_bars = soup.findAll("div", attrs={"class": "finish-bar"})
    # finish_bars = browser.find_elements_by_class_name("finish-bar")
    idx = 0
    train_base_url = "http://yun.chinahrt.com/studentTrainStudyingPage/SelectCoursePage?planId="
    for ea in finish_bars:
        print("--------------------------------")
        # click failed.
        # print(ea)
        # ea.click()
        a = ea.find("a", attrs={"onclick": True})
        on_text = a["onclick"]
        print(on_text)

        be_search1 = '('
        n1 = on_text.index(be_search1)
        be_search2 = ')'
        n2 = on_text.index(be_search2)
        t_id = on_text[n1 + 2:n2 - 1]

        # print(t_id)
        train_url = train_base_url + t_id
        print("-train_url=%s" % train_url)
        browser.get(train_url)
        time.sleep(7)

        train_title = train_list[idx].get_text()
        print("-train[%d]=%s" % (idx, train_title))

        # # save page source code
        # file_path = local_base_path + "train" + str(idx) + "_课程list.txt"
        # print("page_source=" + file_path)
        # fp = open(file_path, 'w', encoding='UTF-8')
        # fp.write(browser.page_source)
        # fp.close()

        # 获取page list
        # <span class="totalPageNum">2</span>
        cur_page_src = browser.page_source
        soup = BeautifulSoup(cur_page_src, "html.parser")
        total_pages = soup.find("span", attrs={"class": "totalPageNum"})
        total_pages = total_pages.get_text()
        total_pages = int(total_pages)
        print("-共" + str(total_pages) + "页")

        p_count = 1
        while p_count <= total_pages:
            print("+++++++++++++++++++++++++++++++++++")
            # 先在指定page上点击------------
            page_text = str(p_count)
            print("--进入第" + page_text + "页...")
            if p_count > 1:
                # <span class="pageBtnWrap">
                #    <span class="disabled">首页</span><span class="disabled">上一页</span><span class="curr">1</span>
                #    <a href="javascript:;;" onclick="return kkpager._clickHandler(2)" title="第2页">2</a>
                #    <a href="javascript:;;" onclick="return kkpager._clickHandler(2)" title="下一页">下一页</a>
                #    <a href="javascript:;;" onclick="return kkpager._clickHandler(2)" title="尾页">尾页</a>
                # </span>
                pp = browser.find_element_by_class_name("pageBtnWrap")
                pp.find_element_by_link_text(page_text).click()
                time.sleep(7)
                print("--click:" + page_text)

            # 获取当前页上的课程列表------------
            # <div class="study-con pxk">
            #   <h3 class="text-tit"><a style="cursor:pointer;" href="/studentCoursePage/co..4">当代科学技术新知识读本</a></h3>
            #   <div class="percentage-light easyPieChart" data-percent="23"
            #   <div class="pro-bar">
            #     <ul>
            #        <li>
            #          <a href="/studentCoursePage/cour-afb0-f2fb03dba0d4">学习课程</a>
            cur_page_src = browser.page_source
            soup = BeautifulSoup(cur_page_src, "html.parser")

            percents = soup.findAll("div", attrs={"data-percent": True})
            titles = soup.findAll("h3", attrs={"class": "text-tit"})
            course_list = soup.findAll("div", attrs={"class": "pro-bar"})

            # is_enter_course = 0
            idx_c = 0
            for ea_c in course_list:
                percent = percents[idx_c].get_text()
                title = titles[idx_c].get_text()
                # print(percent)
                print("--课程=%s, 进度=%s" % (title, percent))

                if percent != "100%":
                    # is_enter_course = 1  # 进入过具体的课程

                    a_list = ea_c.select('ul > li > a')
                    r_url = ""
                    for ea_a in a_list:
                        a_text = ea_a.get_text()
                        if a_text == "学习课程":
                            r_url = ea_a["href"]
                            break

                    course_base_url = "http://yun.chinahrt.com"
                    course_url = course_base_url + r_url
                    print("course_url=%s" % course_url)
                    browser.get(course_url)
                    time.sleep(7)
                    print("---开始学习课程")

                    # # save page source code
                    # file_path = local_base_path + "课程" + str(idx_c) + "章节list.txt"
                    # print("page_source=" + file_path)
                    # fp = open(file_path, 'w', encoding='UTF-8')
                    # fp.write(browser.page_source)
                    # fp.close()

                    # 章节列表----------------
                    cur_page_src = browser.page_source
                    soup = BeautifulSoup(cur_page_src, "html.parser")

                    p_base_url = "http://yun.chinahrt.com"

                    # <div class="coulist cb">
                    #  <ul>
                    #    <li>
                    coulist = soup.find("div", attrs={"class": "coulist cb"})
                    li_list = coulist.select("ul > li")
                    idx_p = 0
                    for ea_li in li_list:
                        # print(ea_li)
                        # <span class="stu-l">未学习(00:00:00)</span>
                        # <a href="/studentCoursePage/chapterDetail/bab1ac36...e9b347602a">第四章 ...(00:44:57)</a>
                        status = ea_li.find("span", attrs={"class": "stu-l"}).get_text()
                        a = ea_li.find("a")
                        chap_text = a.get_text()
                        print("----%s，章节：%s" % (status, chap_text))
                        if re.search("已学完", status) is None:
                            p_url = p_base_url + a["href"]
                            print("p_url=%s" % p_url)
                            browser.get(p_url)  # 打开章节学习
                            time.sleep(7)

                            study_now(browser, local_base_path)

                        idx_p = idx_p + 1

                idx_c = idx_c + 1

                print("---回到课程list！")
                browser.get(train_url)
                time.sleep(7)

            # next page
            p_count = p_count + 1
            # print("p_count=" + str(p_count))

        # next train
        idx = idx + 1

    # exit()

    # quit current session
    browser.close()


if __name__ == "__main__":
    chinahrt_auto_study()
    print("done.")
