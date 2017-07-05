import csv
import json

with open('words.json','r') as f:
    words=json.load(f)['data']

for each in words:

    print each['content'],each['hot']

with open('word.csv','wb') as f:
    csvwriter = csv.writer(f)
    for each in words:

        csvwriter.writerow([each['content'].encode('utf-8'),each['hot']])
