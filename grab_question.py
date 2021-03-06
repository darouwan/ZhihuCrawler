import gzip
import urllib
import urllib.request

import bs4


# -*- coding: utf-8 -*-
__author__ = 'Junfeng'
headers = {'Use-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
           'Accept-Encoding': 'gzip'}


def discover_question(question_url='http://www.zhihu.com/question/30073693'):
    # question_url = 'http://www.zhihu.com/question/30073693'  # test url
    question_req = urllib.request.Request(question_url, headers=headers)
    question_data = urllib.request.urlopen(question_req).read()
    question_content = bs4.BeautifulSoup(gzip.decompress(question_data))
    print(question_content)
    question_num_contents = question_content.find(id='zh-question-answer-num').contents
    if question_num_contents:
        print(question_num_contents[0][:-3].rstrip())


if __name__ == '__main__':
    discover_question()