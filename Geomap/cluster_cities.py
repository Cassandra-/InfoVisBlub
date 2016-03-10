import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets.samples_generator import make_blobs
import json
import os
import ast
import sys

if os.path.exists('cities_2.json'):
    with open('cities_2.json', 'r') as infile:
        read_data = infile.read()
        read_data = ast.literal_eval(read_data)
    infile.close()

# filter schools outside the Netherlands
keys_to_remove = []
with open('cities_2.json', 'w') as outfile:
    outfile.write('{')
    try:
        for city in read_data:
            if read_data[city][0] > 50.5 and read_data[city][0] < 54.0:
                if read_data[city][1] > 3.0 and read_data[city][1] < 7.5:
                    outfile.write("\"" + city + '\":[' + str(read_data[city][0]) + ',' + str(read_data[city][1]) + '],')
                    continue

            keys_to_remove.append(city)

    finally:
        outfile.write('}')
        outfile.close()

for key in keys_to_remove:
    del read_data[key]

X = read_data.values()
X = np.array([np.array(xi) for xi in X])

k = 100
k_means = KMeans(n_clusters=k)
k_means.fit(X)

cluster_centers = k_means.cluster_centers_

with open('cities_2_clusters.json', 'w') as outfile:
    outfile.write('{')
    cnt = 0
    for center in cluster_centers:
        outfile.write("\"" + str(cnt) + '\":[' + str(center[0]) + ',' + str(center[1]) + '],')
        cnt += 1
    outfile.write('}')
    outfile.close()
