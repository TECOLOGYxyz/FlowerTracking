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
import numpy as np
from scipy.spatial import ConvexHull



# Note, EPS_DISTANCE = 20 is a magic number and it needs to be
# * smaller than the gap between any two islands
# * large enough to cluster polygons in one island in same cluster
EPS_DISTANCE = 100
MIN_SAMPLE_POLYGONS = 1


#tracks = pd.read_csv(r'U:\BITCue\Projekter\TrackingFlowers\testResults\_parameterTest_THUL-01_3\parameterTest_THUL-01_maxDisap_0_runMean_0_maxDist_0.csv')
tracks = pd.read_csv(r'U:\BITCue\Projekter\TrackingFlowers\testResults\_parameterTest_NARS-13_3\parameterTest_NARS-13_maxDisap_10_runMean_10_maxDist_400.csv')
gt = pd.read_csv(r'U:\BITCue\Projekter\TrackingFlowers\data\annotations\2020_04_30_NorwayAnnotations_NARS-13_IndividualAnnotations_FRCNN_Metrics.csv')


# tracks = pd.read_csv(r'U:\BITCue\Projekter\TrackingFlowers\data\annotations\2020_05_15_NorwayAnnotations_THUL-01_IndividualAnnotations_FRCNN_Metrics.csv')
# tracks.rename(columns={"id_gt": "objectID"}, inplace = True)
# tracks['x_c'] = (tracks['x_min'] + tracks['x_max']) / 2
# tracks['y_c'] = (tracks['y_min'] + tracks['y_max']) / 2
 


polyHulls = {}

def convex_hull(polygons): # Calculate the convex hull of points
    for k in polygons:
        points = np.array(polygons[k])
        hulls = []
        
        try:
            hull = ConvexHull(points)
            hulls.append(points[hull.vertices])
        
            polyHulls[k] = hulls[0].tolist()
            
            
        except Exception as e:
            if e.args[0][:6] == 'QH6154': # Catch error that points are colinear.
                pass

polyHulls = {}
polygons = {}
    
def gen():
    t = tracks.groupby('objectID')
    for i,g in t: # Generator that yields next group in tracks dataframe
        oid = g['objectID'].iloc[0]
        x_cs = g['x_c'].tolist()
        y_cs = g['y_c'].tolist()
        p = list(map(list, zip(x_cs, y_cs)))
        yield oid, p


def separate():
    for oid, p in gen(): # Take next group in tracks dataframe and split into correct dictionary according to number of points the track contains
        if len(p) > 3: # Get polygons
            polygons[oid] = p
            

separate()
print(polygons)
convex_hull(polygons)


polys = []


for i in polyHulls:
    points = polyHulls[i]
    print("Point: ", '\n', points)
    pg = Polygon(points)
    polys.append(pg)
    
#     # xs = g['x_c'].tolist()
#     # ys = g['x_c'].tolist()
#     # k = list(zip(xs,ys))
#     # polys.append(Polygon(k))

# # for i,g in grouped:
# #     xs = g['x_c'].tolist()
# #     ys = g['x_c'].tolist()
# #     k = list(zip(xs,ys))
# #     polys.append(Polygon(k))
    
# # # for t in p:
# # #     pointsA = p[t]
# # #     polyA = Polygon(pointsA)
# # #     polys.append(polyA)    

# # print(polys)
# # # p1=Polygon([(1,1), (1,3), (3,4), (4,2), (3,1)])
# # # p2=Polygon([(3,3),(2,5),(5,6),(5,4)])
# # # p3=Polygon([(6,8),(8,10),(10,8),(9,6)])
# # # p4=Polygon([(5,2),(7,4),(8,2), (7,1)])
# # # # p4=Polygon([(40,40),(50,40),(50,30),(40,30)])
# # # # p5=Polygon([(40,40),(50,40),(50,50),(40,50)])
# # # # p6=Polygon([(40,40),(40,50),(30,50)])
# # # dfg = gpd.GeoDataFrame(geometry=[p1, p2, p3, p4])
dfg = gpd.GeoDataFrame(geometry=polys)
# print(dfg)


# # # preparation for dbscan
dfg['x'] = dfg['geometry'].centroid.x
dfg['y'] = dfg['geometry'].centroid.y
coords = dfg[["x", "y"]].to_numpy()


# # # dbscan
dbscan = DBSCAN(eps=EPS_DISTANCE, min_samples=MIN_SAMPLE_POLYGONS)
clusters = dbscan.fit(coords)

# # # add labels back to dataframe
labels = pd.Series(clusters.labels_).rename('IslandID')
dfg = pd.concat([dfg, labels], axis=1)
dfg = pd.concat([dfg, tracks['objectID']], axis=1)

dfg.plot('IslandID')

print(dfg.columns)

grouped_df = dfg.groupby("IslandID")
grouped_df = grouped_df.agg({"objectID": "nunique"})
grouped_df = grouped_df.reset_index()
print(grouped_df)
sub = grouped_df.loc[grouped_df['objectID'] == 1]
l = sub['IslandID'].tolist()

print(sub)
#print(l)

dfgSub = dfg[dfg['IslandID'].isin(l)]
dfgSub.plot('IslandID')



gt['x_c'] = (gt['x_min'] + gt['x_max']) / 2
gt['y_c'] = (gt['y_min'] + gt['y_max']) / 2

ids = list(set(gt['id_gt'].tolist()))
#print(ids)

idMap = {}
idList = []


for i,f in enumerate(ids):
    idMap[f] = i

for i,r in gt.iterrows():
    id_gt = r['id_gt']
    idList.append(idMap[id_gt])
    
#print(idList)
gt['colour'] = idList


# plt.scatter(gt['x_c'], gt['y_c'], c = gt['colour'], s = 1)
# plt.show()







