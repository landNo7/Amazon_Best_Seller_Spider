# -*- coding: UTF-8 -*-
import os

path = 'E:\\college\\冯如杯\\冯如杯对抗攻击\\i\
magedownload\\Tencent\\Data\\Home&Kitchen'


def delete_gap_dir(dir):
    if os.path.isdir(dir):
        for d in os.listdir(dir):
            delete_gap_dir(os.path.join(dir, d))
        if not os.listdir(dir):
            os.rmdir(dir)
            print('remove: ' + dir)


delete_gap_dir(path)
