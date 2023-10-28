# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 10:14:16 2022

@author: nkgarrit
"""

import json
import pycocotools.mask as mask
import cv2 as cv2

f = open("testout.json")

data = json.load(f)

ids = [6155,8531,1331,1332,8093,7148,7149,4296,8069,8070,8071,8072,8073,8053,5408,7155,7156,7157,7158,7159,7160,7161,7162,7163,7164,7165,7166,7167,7168,7169]

for i in data['annotations']:
    #print(i['segmentation'])
    if i['id'] in ids:
        continue
    else:
        j = i['segmentation']
        m = [list(j)]
        i['segmentation'] = m
    
# print(data)

with open('dbllist.json', 'w') as fp:
    json.dump(data, fp)
