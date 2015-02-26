import time

import grab_web
import db

__author__ = 'Junfeng'

if __name__ == '__main__':
    candidates_list = []
    base_url = 'http://www.zhihu.com/people/'
    while True:
        candidates_list.clear()
        candidates_list = db.get_all_candidates()
        for candidate in candidates_list:
            grab_web.discoverProfile(base_url + candidate, candidate)
        time.sleep(12 * 60 * 60)