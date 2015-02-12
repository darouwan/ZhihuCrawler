import time

import grab_web
import db

__author__ = 'Junfeng'

candidates_list = db.get_all_candidates()
base_url = 'http://www.zhihu.com/people/'
while True:
    candidates_list.clear()
    candidates_list = db.get_all_candidates()
    for candidate in candidates_list:
        grab_web.discoverProfile(base_url + candidate[0])
    time.sleep(20 * 60)