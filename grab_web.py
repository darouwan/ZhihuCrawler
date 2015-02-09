import re
import urllib.request
import urllib

import bs4


__author__ = 'Junfeng'

headers = {'Use-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
startUrl = "http://www.zhihu.com/people/darouwan-chen"
req = urllib.request.Request(startUrl, headers=headers)
data = urllib.request.urlopen(req).read()
content = bs4.BeautifulSoup(data)
profile_complete = []
profile_ready = [startUrl]
# print(content)

def discoverProfile(profile_url):
    # headers = {'Use-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    #profile_url = "http://www.zhihu.com/people/darouwan-chen"
    profile_req = urllib.request.Request(profile_url, headers=headers)
    profile_data = urllib.request.urlopen(profile_req).read()
    profile_content = bs4.BeautifulSoup(profile_data)
    profiles = profile_content.find_all('div', 'zm-profile-header-main')
    for profile in profiles:
        names = profile.find_all('span', 'name')
        if len(names) > 0:
            name = names[0].contents[0]

        maleGenders = profile.find_all('i', 'icon icon-profile-male')
        if len(maleGenders) > 0:
            print(name, ' is male')
        else:
            femaleGenders = profile.find_all('i', 'icon icon-profile-female')
            if len(femaleGenders) > 0:
                print(name, ' is female')


links = content.find_all('a', href=re.compile(r'people'))
for link in links:
    # print(link.get('href'))
    rawUrl = link.get('href')
    if not rawUrl.startswith('http:'):
        rawUrl = 'http://www.zhihu.com' + rawUrl

    if rawUrl.endswith('/about'):
        continue
    if rawUrl.endswith('/asks'):
        continue
    if rawUrl.endswith('/answers'):
        continue
    if rawUrl.endswith('/posts'):
        continue
    if rawUrl.endswith('/collections'):
        continue
    if rawUrl.endswith('/logs'):
        continue
    if rawUrl.endswith('/followees'):
        continue
    if rawUrl.endswith('/followers'):
        continue
    if rawUrl.endswith('/columns/followed'):
        continue
    if rawUrl.endswith('/topics'):
        continue

    # print(rawUrl)
    if (rawUrl not in profile_complete) & (rawUrl not in profile_ready):
        profile_ready.append(rawUrl)

while len(profile_ready) > 0:
    for startUrl in profile_ready:
        discoverProfile(startUrl)
        print(startUrl)
        profile_complete.append(startUrl)
        profile_ready.remove(startUrl)