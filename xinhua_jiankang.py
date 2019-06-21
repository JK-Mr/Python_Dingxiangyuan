"""
@author: Jiang Ke
@license: Apache Licence 
@contact: jiangke9413@qq.com
@site: 
@software: PyCharm
@file: xinhua_jiankang.py
@time: 2019/6/21 10:42
"""

from bs4 import BeautifulSoup
import requests
import random
import time
import uuid
import json
import redis

site = input("网站地址:")

file_path = 'F:/xinhua/'
htmlf = open(str(site), 'r', encoding="ISO-8859-1")

pool14 = redis.ConnectionPool(host='47.104.101.207', port=6379, decode_responses=True, db=14, password='Pa88####')
# pool11 = redis.ConnectionPool(host='47.104.101.207', port=6379, decode_responses=True, db=14, password='Pa88####')
# rds11 = redis.Redis(connection_pool=pool11)
rds14 = redis.Redis(connection_pool=pool14)


# json文件的格式
def build_json(pub_time, uid, title, url_link, source, main_content):
    resources = {}
    resources['pub_time'] = pub_time
    resources['uuid'] = uid
    resources['title'] = title
    resources['url'] = url_link
    resources['web_source'] = "新华网"
    resources['source'] = source
    resources['en_type'] = "news"
    resources['article_content'] = main_content
    resources['keywords'] = []
    resources['type'] = "新闻资讯"
    resources['pub_person'] = "新华网"

    write_file(resources, uid)

    rds14.sadd('xinhua:news_ok_urls', url_link)
    rds14.set('xinhua:' + uid, 'ok')

    return resources


# 写成json文件
def write_file(resources, fileName):
    with open(file_path + fileName + '.json', 'w', encoding='UTF-8') as f:
        f.write(json.dumps(resources, ensure_ascii=False))
        f.close()


# 请求
def get_html_resp(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    encoding = response.encoding
    if encoding is None:
        return response.content
    data = response.content.decode(encoding, 'ignore').encode('ISO-8859-1')
    response.close()
    return data


# 生成uuid
def get_uuid(string):
    string = str(string.encode('utf-8'))
    uid = str(uuid.uuid3(uuid.NAMESPACE_URL, string))
    return uid


# 生成随机暂停秒数
def generate_second():
    return random.randint(15, 30)


# 去掉回车
def replace_rntb(txt):
    return txt.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '').strip()


# 去掉空格 none
def replace_blank(txt):
    return txt.replace('\r', '').replace('\n', '').replace('\t', '').replace('\u3000', '').strip()


# 根据html内容解析为soup（utf-8编码）
def get_soup(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    if soup is None:
        soup = get_soup(html_content)
        print('soup type is NoneType')
    return soup


# 获取所需内容
def get_url_links(html):
    url_links = []
    content = html.select('ul[id="showData0"]')[0].select('li')
    for i in content:
        try:
            paper_url = i.select('h3')[0].select('a')[0]['href']
            url_links.append(paper_url)
        except:
            continue
    return url_links


def parseHtml(url, html):
    try:
        # 时间
        year = html.select('div[class="h-info"]')[0].select('span[class="h-time"]')[0].text.split('-')[0]
        month = html.select('div[class="h-info"]')[0].select('span[class="h-time"]')[0].text.split('-')[1]
        day = html.select('div[class="h-info"]')[0].select('span[class="h-time"]')[0].text.split('-')[2].split(' ')[0]
        pub_time = year + '-' + month + '-' + day
        # uuid
        uid = get_uuid(url)
        # 标题
        title = replace_rntb(html.select('div[class="h-news"]')[0].select('div[class="h-title"]')[0].text)
        # 来源
        source = replace_blank(html.select('em[id="source"]')[0].text.strip())
        # 主要内容
        article_content = replace_blank(replace_rntb(html.select('div[id="p-detail"]')[0].text))
        json = build_json(replace_rntb(pub_time), uid, title, url, source, replace_blank(article_content))
        print(json)
    except:
        print('错误' + url)


if __name__ == "__main__":
    html = get_soup(htmlf.read())
    url = get_url_links(html)
    for url in url:
        try:
            time.sleep(generate_second())
            print(url)
            html = get_html_resp(str(url))
            parseHtml(url, get_soup(html))
        except:
            continue
    print("OK")
