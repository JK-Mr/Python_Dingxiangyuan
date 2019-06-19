# -*- coding: utf-8 -*-

"""
@author: Jiang Ke
@license: Apache Licence 
@contact: jiangke9413@qq.com
@site: 
@software: PyCharm
@file: xinlang_yiyao.py
@time: 2019/6/19 16:55
"""

from bs4 import BeautifulSoup
import requests
import json
import random
import redis
import uuid
import time


# file_path = 'F:\xinlang_yiyao/'


# json文件的格式
def build_json(pub_time, uid, title, url_link, main_content, keywords):
    resources = {}
    resources['pub_time'] = pub_time
    resources['uuid'] = uid
    resources['title'] = title
    resources['url'] = url_link
    resources['web_source'] = "搜狐健康"
    resources['source'] = "搜狐健康"
    resources['en_type'] = "news"
    resources['article_content'] = main_content
    resources['keywords'] = keywords
    resources['type'] = "新闻资讯"
    resources['pub_person'] = "搜狐健康"

    # write_file(resources, uid)

    return resources


# 生成uuid
def get_uuid(string):
    string = str(string.encode('utf-8'))
    uid = str(uuid.uuid3(uuid.NAMESPACE_URL, string))
    return uid


# 写成json文件
# def write_file(resources, fileName):
#     with open(file_path + fileName + '.json', 'w', encoding='UTF-8') as f:
#         f.write(json.dumps(resources, ensure_ascii=False))
#         f.close()


# 去掉回车
def replace_rntb(txt):
    return txt.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '').strip()


# 去掉空格 none
def replace_blank(txt):
    return txt.replace(' ', '').replace('None', '')


# 生成随机暂停秒数
def generate_second():
    return random.randint(15, 30)


# 请求
def get_html_resp(url):
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    response = requests.get(url=url,headers=headers,verify=False)
    return response


# 获取所需内容
def get_url_links(html):
    print(html)


# 根据html内容解析为soup（utf-8编码）
def get_soup(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    if soup is None:
        soup = get_soup(html_content)
        print('soup type is NoneType')
    return soup


# 获取
def parseHtml(url_link, html):
    # 时间
    year = html.select('div[class="article-info"]')[0].select('span')[0].text.split('-')[0]
    month = html.select('div[class="article-info"]')[0].select('span')[0].text.split('-')[1]
    day = html.select('div[class="article-info"]')[0].select('span')[0].text.split('-')[2].split(' ')[0]
    pub_time = year + '-' + month + '-' + day
    # uuid
    uid = get_uuid(url_link)
    # 标题
    title = replace_rntb(html.select('div[class="text-title"]')[0].select('h1')[0].text)
    # 主要内容
    article_content = replace_rntb(html.select('article[class="article"]')[0].text)
    main_content = replace_blank(article_content + '【关键词】' + html.select('meta[name="keywords"]')[0].attrs['content'])
    # 关键词
    keywords = html.select('meta[name="keywords"]')[0].attrs['content'].split(',')

    build_json(pub_time, uid, title, url_link, main_content, keywords)


if __name__ == "__main__":
    html = get_html_resp(str('https://med.sina.com/article_list_-1_1_' + str(1) + '_3509.html'))
    # get_url_links(html.text)

    print("OK")
