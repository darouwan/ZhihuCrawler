import re
import urllib.request
import urllib

import bs4


__author__ = 'Junfeng'

headers = {'Use-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
startUrl = "http://www.zhihu.com/people/darouwan-chen"

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
    discoverNewLinks(profile_content)


def discoverNewLinks(profile_content):
    links = profile_content.find_all('a', href=re.compile(r'people'))
    for link in links:
        # print(link.get('href'))
        rawurl = link.get('href')
        if not rawurl.startswith('http:'):
            rawurl = 'http://www.zhihu.com' + rawurl

        if rawurl.endswith('/about'):
            continue
        if rawurl.endswith('/asks'):
            continue
        if rawurl.endswith('/answers'):
            continue
        if rawurl.endswith('/posts'):
            continue
        if rawurl.endswith('/collections'):
            continue
        if rawurl.endswith('/logs'):
            continue
        if rawurl.endswith('/followees'):
            continue
        if rawurl.endswith('/followers'):
            continue
        if rawurl.endswith('/columns/followed'):
            continue
        if rawurl.endswith('/topics'):
            continue

        # print(rawUrl)
        if (rawurl not in profile_complete) & (rawurl not in profile_ready):
            profile_ready.append(rawurl)


while len(profile_ready) > 0:
    for startUrl in profile_ready:
        discoverProfile(startUrl)
        print(startUrl)
        profile_complete.append(startUrl)
        profile_ready.remove(startUrl)