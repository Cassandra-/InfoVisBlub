import sys
import json
from collections import defaultdict

def get_centroid(clusters, city):
    for cluster, cities in clusters.items():
        if city in cities:
            return cluster

with open(sys.argv[1], 'r') as f:
    flow = json.load(f, encoding='latin1')

with open(sys.argv[2], 'r') as f:
    clusters = json.load(f, encoding='latin1')

out = defaultdict(lambda: {})
for frm, destinations in flow.items():
    frm_centroid = get_centroid(clusters, frm)

    for to, count in destinations.items():
        to_centroid = get_centroid(clusters, to)
        if to_centroid in out[frm_centroid]:
            out[frm_centroid][to_centroid] += count
        else:
            out[frm_centroid][to_centroid] = count

with open('flow.json', 'w') as f:
    print(json.dumps(out, f, encoding='latin1', indent=1))
