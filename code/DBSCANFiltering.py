# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 13:28:48 2021

@author: au309263
"""

import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from filtering import sieve

# Note, EPS_DISTANCE = 20 is a magic number and it needs to be
# * smaller than the gap between any two islands
# * large enough to cluster polygons in one island in same cluster
EPS_DISTANCE = 4
MIN_SAMPLE_POLYGONS = 1


#tracks = pd.read_csv(r'U:\BITCue\Projekter\TrackingFlowers\testResults\_parameterTest_NARS-13_3\parameterTest_NARS-13_maxDisap_10_runMean_10_maxDist_300.csv')
tracks = pd.read_csv(r'U:\BITCue\Projekter\TrackingFlowers\data\annotations\2020_05_15_NorwayAnnotations_THUL-01_IndividualAnnotations_FRCNN_Metrics.csv')
### FILTER ###

# s = sieve(tracks)

# d,p = s.run()

# print(p)

# tracks_filtered = tracks[tracks['objectID'].isin(d)]
# tracks_filtered.to_csv(r'U:\BITCue\Projekter\TrackingFlowers\testResults/filtered20_NYAA-04_maxDisap_10_runMean_10_maxDist_300.csv')

polys = []


tracks['x_c'] = (tracks['x_min'] + tracks['x_max']) / 2
tracks['y_c'] = (tracks['y_min'] + tracks['y_max']) / 2
 
grouped = tracks.groupby(['id_gt'])   


for i,g in grouped:
    xs = g['x_c'].tolist()
    ys = g['x_c'].tolist()
    k = list(zip(xs,ys))
    polys.append(Polygon(k))
    
# for t in p:
#     pointsA = p[t]
#     polyA = Polygon(pointsA)
#     polys.append(polyA)    

print(polys)
# p1=Polygon([(1,1), (1,3), (3,4), (4,2), (3,1)])
# p2=Polygon([(3,3),(2,5),(5,6),(5,4)])
# p3=Polygon([(6,8),(8,10),(10,8),(9,6)])
# p4=Polygon([(5,2),(7,4),(8,2), (7,1)])
# # p4=Polygon([(40,40),(50,40),(50,30),(40,30)])
# # p5=Polygon([(40,40),(50,40),(50,50),(40,50)])
# # p6=Polygon([(40,40),(40,50),(30,50)])
# dfg = gpd.GeoDataFrame(geometry=[p1, p2, p3, p4])
dfg = gpd.GeoDataFrame(geometry=polys)
print(dfg)


# preparation for dbscan
dfg['x'] = dfg['geometry'].centroid.x
dfg['y'] = dfg['geometry'].centroid.y
coords = dfg[["x", "y"]].to_numpy()


# dbscan
dbscan = DBSCAN(eps=EPS_DISTANCE, min_samples=MIN_SAMPLE_POLYGONS)
clusters = dbscan.fit(coords)

# add labels back to dataframe
labels = pd.Series(clusters.labels_).rename('IslandID')
dfg = pd.concat([dfg, labels], axis=1)

dfg.plot('IslandID')


# plt.scatter(tracks['x_c'], tracks['y_c'], c = tracks['objectID'], s = 5)
# plt.show()