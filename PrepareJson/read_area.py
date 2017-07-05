#encoding=utf-8

import json
import csv

with open('province_counts.json', 'r') as f:
    dic = json.load(f)
for key in dic.keys():
    print key, dic[key]
with open('province_counts.csv', 'wb') as csvfile:
    csvwritter = csv.writer(csvfile)
    for key in dic:
        csvwritter.writerow([key.encode('utf-8'), dic[key]])
    
##with open('area_counts.json', 'r') as f:
##    dic = json.load(f)
##
##dic = sorted(dic.iteritems(), key = lambda x: x[1], reverse = True)
##for key in dic:
##    print key[0], key[1]
##with open('area_counts.csv', 'wb') as csvfile:
##    csvwritter = csv.writer(csvfile)
##    for key in dic:
##        csvwritter.writerow([key[0].encode('utf-8'), key[1]])
