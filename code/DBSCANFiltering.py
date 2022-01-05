# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 13:28:48 2021

@author: au309263
"""

import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon, LineString, Point
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from filtering import sieve
import numpy as np
from scipy.spatial import ConvexHull


# Note, EPS_DISTANCE = 20 is a magic number and it needs to be
# * smaller than the gap between any two islands
# * large enough to cluster polygons in one island in same cluster
#EPS_DISTANCE = 300 #281 #281
#MIN_SAMPLE_POLYGONS = 1




#tracks = pd.read_csv(r'U:\BITCue\Projekter\TrackingFlowers\testResults\_parameterTest_THUL-01_3\parameterTest_THUL-01_maxDisap_0_runMean_0_maxDist_0.csv')
tracks = pd.read_csv(r'U:\BITCue\Projekter\TrackingFlowers\testResults\_parameterTest_NARS-04_3\parameterTest_NARS-04_maxDisap_10_runMean_10_maxDist_100.csv')
#gt = pd.read_csv(r'U:\BITCue\Projekter\TrackingFlowers\data\annotations\2020_05_17_NorwayAnnotations_NARS-04_IndividualAnnotations_FRCNN_Metrics.csv')



class DBSCANsieve():
    def __init__(self, tracks, eps_distance, min_sample_polygons):
        self.tracks = tracks
        
        self.eps_distance = eps_distance
        self.min_sample_polygons = min_sample_polygons
        
        
        self.points = {}
        self.lines = {}
        self.triangles = {}
        self.polygons = {}
        self.polyLengths = {}
        self.polyHulls = {}
        
        
    def gen(self):
        t = self.tracks.groupby('objectID')
        for i,g in t: # Generator that yields next group in tracks dataframe
            oid = g['objectID'].iloc[0]
            x_cs = g['x_c'].tolist()
            y_cs = g['y_c'].tolist()
            p = list(map(list, zip(x_cs, y_cs)))
            yield oid, p
    
    
    def separate(self):

        for oid, p in self.gen(): # Take next group in tracks dataframe and split into correct dictionary according to number of points the track contains
            if len(p) == 1: # Get single points
                self.points[oid] = p
                
            if len(p) == 2: # Get lines
                self.lines[oid] = p
                
            if len(p) == 3: # Get triangles
                self.triangles[oid] = p

            if len(p) > 3: # Get polygons
                self.polygons[oid] = p
                
        for p in self.polygons:
            self.polyLengths[p] = len(self.polygons[p])
            
            
    def geometries(self): # Create a geodataframe containing the track geometries
        
        df = gpd.GeoDataFrame()
        
        for oid in self.points:
            p = self.points[oid]
            df = df.append({'points': p, 'objectID': str(oid), 'geometry': Point(p[0])}, ignore_index=True)
        
        for oid in self.lines:
            l = self.lines[oid]
            df = df.append({'points': l, 'objectID': str(oid), 'geometry': LineString(l)}, ignore_index=True)
            
            
        for oid in self.polyHulls:
            points = self.polyHulls[oid]
            df = df.append({'points': points, 'objectID': str(oid), 'geometry': Polygon(points)}, ignore_index=True)
        
        
        df['x'] = df['geometry'].centroid.x
        df['y'] = df['geometry'].centroid.y
        
        coords = df[["x", "y"]].to_numpy()
        
        return df, coords
    


    def convex_hull(self, polygons): # Calculate the convex hull of points
            for k in polygons:
                points = np.array(polygons[k])
                hulls = []
                
                try:
                    hull = ConvexHull(points)
                    hulls.append(points[hull.vertices])
                
                    self.polyHulls[k] = hulls[0].tolist()
                    
                    
                except Exception as e:
                    if e.args[0][:6] == 'QH6154': # Catch error that points are colinear.
                        print(f'Adding object {k} with points {polygons[k]} to lines')    
                        self.lines[k] = polygons[k] # Add the points to the line dictionary
    

    
    def run(self):
        self.separate() # Separate the tracks into points, lines, and polygons
        self.convex_hull(self.polygons)
        
        df, coords = self.geometries()


        dbscan = DBSCAN(eps=self.eps_distance, min_samples=self.min_sample_polygons) # Run the DBSCAN clustering
        clusters = dbscan.fit(coords)

        labels = pd.Series(clusters.labels_).rename('clusterID') # Grab the clustering labels and concatenate to df
        df = pd.concat([df, labels], axis=1)

        grouped_df = df.groupby("clusterID") # Group by the clusterID and count the number of tracks within each cluster
        grouped_df = grouped_df.agg({"objectID": "nunique"}).reset_index()
        sub = grouped_df.loc[grouped_df['objectID'] == 1] # Make a list of clusterIDs that contain only one track
        l = sub['clusterID'].tolist()

        dfSub = df[df['clusterID'].isin(l)] # Subset the  df on the list so that it only includes only the isolated tracks (clusters containing a single track)
        


        
        fig, (ax1, ax2) = plt.subplots(ncols=2, sharex=True, sharey=True) # Plot some stuff        
        
        #fig.tight_layout
        
        
        left  = 0.125  # the left side of the subplots of the figure
        right = 0.9    # the right side of the subplots of the figure
        bottom = 0.1   # the bottom of the subplots of the figure
        top = 0.9      # the top of the subplots of the figure
        wspace = 0.02   # the amount of width reserved for blank space between subplots
        hspace = 0.2   # the amount of height reserved for white space between subplots
        fig.subplots_adjust(left = left, bottom=bottom, right=right, top=top, wspace = wspace , hspace=hspace)
        
        ax1.axes.get_yaxis().set_visible(False)
        ax2.axes.get_yaxis().set_visible(False)
      
              
        ax1.axes.get_xaxis().set_visible(False)
        ax2.axes.get_xaxis().set_visible(False)  
      
        df.plot(ax=ax1, column = 'clusterID', marker = ".", markersize = 0.2).invert_yaxis()
        dfSub.plot(ax=ax2, column = 'clusterID', marker = ".", markersize=0.2)
        
        
        fig.savefig(f'../testResults/BeforeAndAfterFiltering_eps_{self.eps_distance}.png', dpi=300)

    
        return 0

        
d = DBSCANsieve(tracks, eps_distance = 200, min_sample_polygons = 1)
d.run()





# p1=LineString([(40,40),(55,50)])
# l = list(p1.centroid.coords)
# #l = p1.centroid
# print(l[0][0])

# k = pd.DataFrame()

# k['x'] = [1,4] #l[0][0]
# k['y'] = [2,3] #l[0][1]

        
# coords = k[["x", "y"]].to_numpy()

# dbscan = DBSCAN(eps=100, min_samples=1)
# clusters = dbscan.fit(coords)


# p1=LineString([(40,40),(40,50),(30,50)])
# p2=LineString([(40,40),(40,50),(30,50)])

# dfg = gpd.GeoDataFrame(geometry=[p1, p2])

# dfg['x'] = dfg['geometry'].centroid.x
# dfg['y'] = dfg['geometry'].centroid.y
# coords = dfg[["x", "y"]].to_numpy()
# print(coords)
# # # # # dbscan
# dbscan = DBSCAN(eps=100, min_samples=1)
# clusters = dbscan.fit(coords)


#dfg.plot('IslandID')
# polys = []


# for i in polyHulls:
#     points = polyHulls[i]
#     print("Point: ", '\n', points)
#     pg = Polygon(points)
#     polys.append(pg)
    
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
# dfg = gpd.GeoDataFrame(geometry=polys)
# # print(dfg)


# # # # preparation for dbscan
# dfg['x'] = dfg['geometry'].centroid.x
# dfg['y'] = dfg['geometry'].centroid.y
# coords = dfg[["x", "y"]].to_numpy()


# # # # dbscan
# dbscan = DBSCAN(eps=EPS_DISTANCE, min_samples=MIN_SAMPLE_POLYGONS)
# clusters = dbscan.fit(coords)

# # # # add labels back to dataframe
# labels = pd.Series(clusters.labels_).rename('IslandID')
# dfg = pd.concat([dfg, labels], axis=1)
# dfg = pd.concat([dfg, tracks['objectID']], axis=1)

# dfg.plot('IslandID')

# print(dfg.columns)

# grouped_df = dfg.groupby("IslandID")
# grouped_df = grouped_df.agg({"objectID": "nunique"})
# grouped_df = grouped_df.reset_index()
# print(grouped_df)
# sub = grouped_df.loc[grouped_df['objectID'] == 1]
# l = sub['IslandID'].tolist()

# print(sub)
# #print(l)

# dfgSub = dfg[dfg['IslandID'].isin(l)]
# dfgSub.plot('IslandID')



# gt['x_c'] = (gt['x_min'] + gt['x_max']) / 2
# gt['y_c'] = (gt['y_min'] + gt['y_max']) / 2

# ids = list(set(gt['id_gt'].tolist()))
# #print(ids)

# idMap = {}
# idList = []


# for i,f in enumerate(ids):
#     idMap[f] = i

# for i,r in gt.iterrows():
#     id_gt = r['id_gt']
#     idList.append(idMap[id_gt])
    
# #print(idList)
# gt['colour'] = idList


# plt.scatter(gt['x_c'], gt['y_c'], c = gt['colour'], s = 1)
# plt.show()





# tracks = pd.read_csv(r'U:\BITCue\Projekter\TrackingFlowers\data\annotations\2020_05_15_NorwayAnnotations_THUL-01_IndividualAnnotations_FRCNN_Metrics.csv')
# tracks.rename(columns={"id_gt": "objectID"}, inplace = True)
# tracks['x_c'] = (tracks['x_min'] + tracks['x_max']) / 2
# tracks['y_c'] = (tracks['y_min'] + tracks['y_max']) / 2



