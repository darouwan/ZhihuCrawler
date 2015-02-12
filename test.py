import time

import grab_web
import db

__author__ = 'Junfeng'

prepare_list = ['http://www.zhihu.com/people/Yakinrossa', 'http://www.zhihu.com/people/darouwan-chen']
candidates_list = db.get_all_candidates()
base_url = 'http://www.zhihu.com/people/'
while True:
    prepare_list.clear()
    for candidate in candidates_list:
        prepare_list.append(base_url + candidate[0])

    for url in prepare_list:
        grab_web.discoverProfile(url)
    time.sleep(20 * 60)