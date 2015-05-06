import gzip
import re
import traceback
from urllib.error import HTTPError
import urllib.request
import urllib

from django.utils import timezone
import bs4

import db

"""
                       ::
                      :;J7, :,                        ::;7:
                      ,ivYi, ,                       ;LLLFS:
                      :iv7Yi                       :7ri;j5PL
                     ,:ivYLvr                    ,ivrrirrY2X,
                     :;r@Wwz.7r:                :ivu@kexianli.
                    :iL7::,:::iiirii:ii;::::,,irvF7rvvLujL7ur
                   ri::,:,::i:iiiiiii:i:irrv177JX7rYXqZEkvv17
                ;i:, , ::::iirrririi:i:::iiir2XXvii;L8OGJr71i
              :,, ,,:   ,::ir@mingyi.irii:i:::j1jri7ZBOS7ivv,
                 ,::,    ::rv77iiiriii:iii:i::,rvLq@huhao.Li
             ,,      ,, ,:ir7ir::,:::i;ir:::i:i::rSGGYri712:
           :::  ,v7r:: ::rrv77:, ,, ,:i7rrii:::::, ir7ri7Lri
          ,     2OBBOi,iiir;r::        ,irriiii::,, ,iv7Luur:
        ,,     i78MBBi,:,:::,:,  :7FSL: ,iriii:::i::,,:rLqXv::
        :      iuMMP: :,:::,:ii;2GY7OBB0viiii:i:iii:i:::iJqL;::
       ,     ::::i   ,,,,, ::LuBBu BBBBBErii:i:i:i:i:i:i:r77ii
      ,       :       , ,,:::rruBZ1MBBqi, :,,,:::,::::::iiriri:
     ,               ,,,,::::i:  @arqiao.       ,:,, ,:::ii;i7:
    :,       rjujLYLi   ,,:::::,:::::::::,,   ,:i,:,,,,,::i:iii
    ::      BBBBBBBBB0,    ,,::: , ,:::::: ,      ,,,, ,,:::::::
    i,  ,  ,8BMMBBBBBBi     ,,:,,     ,,, , ,   , , , :,::ii::i::
    :      iZMOMOMBBM2::::::::::,,,,     ,,,,,,:,,,::::i:irr:i:::,
    i   ,,:;u0MBMOG1L:::i::::::  ,,,::,   ,,, ::::::i:i:iirii:i:i:
    :    ,iuUuuXUkFu7i:iii:i:::, :,:,: ::::::::i:i:::::iirr7iiri::
    :     :rk@Yizero.i:::::, ,:ii:::::::i:::::i::,::::iirrriiiri::,
     :      5BMBBBBBBSr:,::rv2kuii:::iii::,:i:,, , ,,:,:i@petermu.,
          , :r50EZ8MBBBBGOBBBZP7::::i::,:::::,: :,:,::i;rrririiii::
              :jujYY7LS0ujJL7r::,::i::,::::::::::::::iirirrrrrrr:ii:
           ,:  :@kevensun.:,:,,,::::i:i:::::,,::::::iir;ii;7v77;ii;i,
           ,,,     ,,:,::::::i:iiiii:i::::,, ::::iiiir@xingjief.r;7:i,
        , , ,,,:,,::::::::iiiiiiiiii:,:,:::::::::iiir;ri7vL77rrirri::
         :,, , ::::::::i:::i:::i:i::,,,,,:,::i:i:::iir;@Secbone.ii:::


"""

__author__ = 'Junfeng'

headers = {'Use-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
           'Accept-Encoding': 'gzip'}
startUrl = "http://www.zhihu.com/people/darouwan-chen"
ISOTIMEFORMAT = '%Y-%m-%d %X'
profile_complete = []
profile_ready = [startUrl]
# print(content)


def discoverProfile(profile_url, candidate):
    print(profile_url)
    # headers = {'Use-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    # profile_url = "http://www.zhihu.com/people/darouwan-chen"

    try:
        profile_req = urllib.request.Request(profile_url, headers=headers)
        profile_data = urllib.request.urlopen(profile_req).read()
        profile_content = bs4.BeautifulSoup(gzip.decompress(profile_data))

        profiles = profile_content.find_all('div', 'zm-profile-header-main')
        name = ''
        for profile in profiles:
            names = profile.find_all('span', 'name')
            gender = ''
            if len(names) > 0:
                name = names[0].contents[0]

            male_genders = profile.find_all('i', 'icon icon-profile-male')
            if len(male_genders) > 0:
                gender = 'male'
            else:
                female_genders = profile.find_all('i', 'icon icon-profile-female')
                if len(female_genders) > 0:
                    gender = 'female'

        discover_new_links(profile_content)
        count = get_followers_count(profile_content)
        upvotes = get_upvotes(profile_content)
        thanks = get_thanks(profile_content)
        # current_time = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
        # timezone.activate('Asia/Shanghai')
        current_time = timezone.now()
        if name != '':
            print(name, '\t is \t', gender, '\t followers:\t', count, '\tupvotes:', upvotes, '\tthanks:', thanks,
                  '\ttime:',
                  current_time)
            # db.insert_user_data((name, gender, count, upvotes, thanks, current_time))
            db.insert_user_data_django(name, gender, count, upvotes, thanks, current_time, candidate)
    except HTTPError:
        # print('HTTP error')
        traceback.print_exc()
        # HTTPError.with_traceback()



def get_upvotes(profile):
    profile_header_user_agree = profile.find_all('span', 'zm-profile-header-user-agree')
    upvotes = 0
    if len(profile_header_user_agree) > 0:
        upvotes = profile_header_user_agree[0].find_all('strong')[0].contents[0]
        upvotes = int(upvotes)
    return upvotes


def get_thanks(profile):
    profile_header_user_thanks = profile.find_all('span', 'zm-profile-header-user-thanks')
    thanks = 0
    if len(profile_header_user_thanks) > 0:
        thanks = profile_header_user_thanks[0].find_all('strong')[0].contents[0]
        thanks = int(thanks)
    return thanks


def discover_new_links(profile_content):
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
        if (rawurl not in profile_complete) and (rawurl not in profile_ready):
            profile_ready.append(rawurl)


def get_followers_count(profile_content):
    # print(profile_content)
    count = 0
    followers_sections = profile_content.find_all('a', 'item', href=re.compile(r'/followers$'))
    if len(followers_sections) == 0:
        print('followers section  is null')
        return 0
    count = followers_sections[0].find_all('strong')[0].contents[0]

    # print(count)
    return count

# discoverProfile('http://www.zhihu.com/people/yang-dong-54-6')

if __name__ == '__main__':
    discoverProfile('http://www.zhihu.com/people/wei-fei-28-42', 'wei-fei-28-42')


