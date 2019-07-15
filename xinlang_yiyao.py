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

import urllib3

file_path = 'F:/lang_yiyao/'

pool14 = redis.ConnectionPool(host='47.104.101.207', port=6379, decode_responses=True, db=14, password='Pa88####')
# pool11 = redis.ConnectionPool(host='47.104.101.207', port=6379, decode_responses=True, db=14, password='Pa88####')
# rds11 = redis.Redis(connection_pool=pool11)
rds14 = redis.Redis(connection_pool=pool14)


# json文件的格式
def build_json(pub_time, uid, title, url_link, source, main_content, keywords):
    resources = {}
    resources['pub_time'] = pub_time
    resources['uuid'] = uid
    resources['title'] = title
    resources['url'] = url_link
    resources['web_source'] = "新浪医药新闻"
    resources['source'] = source  # 网页获取
    resources['en_type'] = "news"
    resources['article_content'] = main_content
    resources['keywords'] = keywords
    resources['type'] = "新闻资讯"
    resources['pub_person'] = "新浪医药新闻"

    write_file(resources, uid)

    # rds14.sadd('xinlang:news_ok_urls', url_link)
    # rds14.set('xinlang:' + uid, 'ok')

    return resources


# 生成uuid
def get_uuid(string):
    string = str(string.encode('utf-8'))
    uid = str(uuid.uuid3(uuid.NAMESPACE_URL, string))
    return uid


# 写成json文件
def write_file(resources, fileName):
    print(fileName)
    with open(file_path + fileName + '.json', 'w', encoding='UTF-8') as f:
        f.write(json.dumps(resources, ensure_ascii=False))
        f.close()


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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    urllib3.disable_warnings()
    response = requests.get(url=url, headers=headers, verify=False)
    return response


# 获取所需内容
def get_url_links(html):
    url_links = []
    content = html.select('li')
    for i in content:
        try:
            paper_url = i.select('div[class="indextitle-text"]')[0].select('a')[0]['href']
            url_links.append(paper_url)
        except:
            continue
    return url_links


# 根据html内容解析为soup（utf-8编码）
def get_soup(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    if soup is None:
        soup = get_soup(html_content)
        print('soup type is NoneType')
    return soup


# 获取
def parseHtml(url_link, html):
    try:
        # 时间
        date = html.select('div[class="wz-tbbox"]')[0].select('span')[1].text
        resTime = time.strftime('%Y-%m-%d', time.strptime(date.strip(), '%a %b %d %H:%M:%S CST %Y'))
        # uuid
        uid = get_uuid(url_link)
        # 标题
        title = replace_rntb(html.select('div[class="news"]')[0].select('h1[class="news-title"]')[0].text)
        # 关键词
        keywords = html.select('meta[name="keywords"]')[0].attrs['content'].split()
        # 主要内容
        article_content = replace_rntb(html.select('div[class="textbox"]')[0].text)
        main_content = replace_blank(article_content + '【关键词】' + str(keywords))
        # 来源
        source = replace_blank(html.select('span[class="wz-zuthorname"]')[0].select('em')[0].text.strip())

        print(url_link + '有来源数据！')
        json = build_json(resTime, uid, title, url_link, source, main_content, keywords)
    except:
        try:
            date = html.select('div[class="wz-tbbox"]')[0].select('span')[0].text
            resTime = time.strftime('%Y-%m-%d', time.strptime(date.strip(), '%a %b %d %H:%M:%S CST %Y'))
            # uuid
            uid = get_uuid(url_link)
            # 标题
            title = replace_rntb(html.select('div[class="news"]')[0].select('h1[class="news-title"]')[0].text)
            # 关键词
            keywords = html.select('meta[name="keywords"]')[0].attrs['content'].split()
            # 主要内容
            article_content = replace_rntb(html.select('div[class="textbox"]')[0].text)
            main_content = replace_blank(article_content + '【关键词】' + str(keywords))
            # 来源
            source = '新浪医药新闻'

            print(url_link + '无来源数据！')
            json = build_json(resTime, uid, title, url_link, source, main_content, keywords)
        except:

            # 时间
            date = html.select('div[class="wz-tbbox"]')[0].select('span')[1].text
            resTime = time.strftime('%Y-%m-%d', time.strptime(date.strip(), '%a %b %d %H:%M:%S CST %Y'))
            # uuid
            uid = get_uuid(url_link)
            # 标题
            title = replace_rntb(html.select('div[class="news"]')[0].select('h1[class="news-title"]')[0].text)
            # 关键词
            keywords = html.select('meta[name="keywords"]')[0].attrs['content'].split()
            # 主要内容
            article_content = replace_rntb(html.select('div[class="textbox"]')[0].text)
            main_content = replace_blank(article_content + '【关键词】' + str(keywords))
            # 来源
            source = replace_blank(
                html.select('span[class="wz-zuthorname margin-l50"]')[0].select('em')[0].select('a')[0].text.strip())

            print(url_link + '原创数据！')
            json = build_json(resTime, uid, title, url_link, source, main_content, keywords)


if __name__ == "__main__":
    for i in range(1, 3509):
        print('第%d页' % i)
        html = get_html_resp(str('https://med.sina.com/article_list_-1_1_' + str(1) + '_3509.html'))
        url_links = get_url_links(get_soup(html.text))
        if not (url_links is None):
            for url_link in url_links:
                try:
                    time.sleep(generate_second())
                    html = get_html_resp(str(url_link))
                    parseHtml(url_link, get_soup(html.text))
                except:
                    continue
