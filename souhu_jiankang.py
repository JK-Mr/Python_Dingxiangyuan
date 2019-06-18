# -*- coding: utf-8 -*-

"""
@author: Jiang Ke
@license: Apache Licence 
@contact: jiangke9413@qq.com
@site: 
@software: PyCharm
@file: souhu_jiankang.py
@time: 2019/6/18 15:50
"""

from bs4 import BeautifulSoup
import requests
import json

bulk_path = 'F:\\all_bulks\\'

# 请求
def get(url):
    # 请求头,模拟浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    # 返回信息
    response = requests.get(url, headers=headers)
    return response


# 获取所需内容
def html_content(html_content):
    json_load = json.loads(str(html_content))
    pcArticleVOS = json_load['data']['pcArticleVOS']
    for a in pcArticleVOS:
        print(str(a['link']))
        with open(a['link'] + '.json', 'w') as f:
            f.write(json.dumps(ensure_ascii=False).decode('utf8'))
            f.close()


if __name__ == "__main__":
    html = get(str('https://v2.sohu.com/author-page-api/author-articles/pc/104952?pNo=') + str(1))
    html_content(html.text)
    print("OK")
