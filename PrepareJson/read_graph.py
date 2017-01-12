import json
import pprint

with open('graph_index.json','r') as f:
    d=json.load(f)

print 'num of nodes',str(len(d['nodes']))
print 'num of edges',str(len(d['edges']))

