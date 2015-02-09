import shutil
import urllib.request
import urllib
import bs4,os
import requests
__author__ = 'Junfeng'


headers = {'Use-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
url = "http://www.zhihu.com/people/darouwan-chen"
req = urllib.request.Request(url, headers=headers)
data = urllib.request.urlopen(req).read()
content = bs4.BeautifulSoup(data)
print(content)

link=content.findAll('a')

print(link)