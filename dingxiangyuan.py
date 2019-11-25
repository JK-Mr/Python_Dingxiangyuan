"""
@author: Jiang Ke
@license: Apache Licence 
@contact: jiangke9413@qq.com
@site: 
@software: PyCharm
@file: dingxiangyuan.py
@time: 2019/11/25 17:19
"""

import requests
from bs4 import BeautifulSoup


# 请求页面
def get_html_resp(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    return response


# 根据html内容解析为soup（utf-8编码）
def get_soup(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    if soup is None:
        soup = get_soup(html_content)
    return soup


# 获取所需内容
def get_url_links(html_content):
    url_links = []
    content = html_content.select('div[class="x_wrap1 fl"]')[0]
    for a in content:
        print(a.select('a'))
        # try:
        #     paper_url = a.select('a')[0]['href']
        #     url_links.append(paper_url)
        # except:
        #     continue



if __name__ == "__main__":
    html = get_html_resp(str('http://heart.dxy.cn/tag/news/p-1'))
    get_url_links(get_soup(html.text))
