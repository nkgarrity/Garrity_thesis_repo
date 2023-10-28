# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 12:06:20 2022

@author: nkgarrit
"""

import json
import pycocotools.mask as mask
import cv2 as cv2


def polygonFromMask(maskedArr): # https://github.com/hazirbas/coco-json-converter/blob/master/generate_coco_json.py

        contours, _ = cv2.findContours(maskedArr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        segmentation = []
        for contour in contours:
            # Valid polygons have >= 6 coordinates (3 points)
            if contour.size >= 6:
                segmentation.append(contour.flatten().tolist())
        RLEs = mask.frPyObjects(segmentation, maskedArr.shape[0], maskedArr.shape[1])
        RLE = mask.merge(RLEs)
        # RLE = mask.encode(np.asfortranarray(maskedArr))
        area = mask.area(RLE)
        [x, y, w, h] = cv2.boundingRect(maskedArr)

        return segmentation[0] #, [x, y, w, h], area

f = open("C:/Users/nkgar/Desktop/mrcnn_train_data/coco_json_all.json")

data = json.load(f)

for i in data['annotations']:
    #print(i['segmentation'])
    j = i['segmentation']
    if type(j) == list:
        continue
    
    maskedArr = mask.decode(j)
    k = [polygonFromMask(maskedArr)]
    i['segmentation'] = k  
    
    
# f.close()