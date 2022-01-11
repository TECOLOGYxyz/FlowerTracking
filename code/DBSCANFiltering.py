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
from datetime import datetime

# Note, EPS_DISTANCE needs to be smaller than the gap between any two polygons we want to keep and large enough to cluster polygons that we want to discard together
# EPS_DISTANCE = 281 is the highest value that keeps all tracks in THUL-01

#tracks = pd.read_csv(r'U:\BITCue\Projekter\TrackingFlowers\testResults\_parameterTest_NARS-04_3\parameterTest_NARS-04_maxDisap_10_runMean_10_maxDist_500.csv')

class DBSCANsieve():
    def __init__(self, tracks, eps_distance, min_sample_polygons):
        if not isinstance(tracks, pd.DataFrame):
            self.tracks = pd.read_csv(tracks, sep=",", header = 0)
        else:
            self.tracks = tracks
        
        self.eps_distance = eps_distance
        self.min_sample_polygons = min_sample_polygons
        
        self.points = {}
        self.lines = {}
        self.triangles = {}
        self.polygons = {}
        self.polyLengths = {}
        self.polyHulls = {}
        
    def gen(self): # Generator that yields next group in tracks dataframe
        t = self.tracks.groupby('objectID')
        for i,g in t: 
            oid = g['objectID'].iloc[0]
            x_cs = g['x_c'].tolist()
            y_cs = g['y_c'].tolist()
            p = list(map(list, zip(x_cs, y_cs)))
            yield oid, p
    
    
    def separate(self): # Take next group in tracks dataframe from the generator and split into correct dictionary according to number of points the track contains
        for oid, p in self.gen(): 
            if len(p) == 1: # Get single points
                self.points[oid] = p
                
            if len(p) == 2: # Get lines
                self.lines[oid] = p
                
            if len(p) == 3: # Get triangles
                self.triangles[oid] = p

            if len(p) > 3: # Get polygons
                self.polygons[oid] = p
                
        for p in self.polygons: # Create a dictionary of number of points in each polygon (currently not used)
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
        
        return df, coords # Return the created dataframe as well as the centroid coordinates of which to perform the DBSCAN clustering

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
        self.convex_hull(self.polygons) # Calcuate the convex hull of the polygons. This will also add colinear points to lines dictionary
        
        df, coords = self.geometries() # Get the geometry dataframe containing the track polygons and the centroid coordinates of which to perform the DBSCAN clustering

        dbscan = DBSCAN(eps=self.eps_distance, min_samples=self.min_sample_polygons) # Run the DBSCAN clustering
        clusters = dbscan.fit(coords)

        labels = pd.Series(clusters.labels_).rename('clusterID') # Grab the clustering labels and concatenate to df
        df = pd.concat([df, labels], axis=1)

        grouped_df = df.groupby("clusterID") # Group by the clusterID and count the number of tracks within each cluster
        grouped_df = grouped_df.agg({"objectID": "nunique"}).reset_index()
        sub = grouped_df.loc[grouped_df['objectID'] == 1] # Make a list of clusterIDs that contain only one track
        l = sub['clusterID'].tolist()

        dfSub = df[df['clusterID'].isin(l)] # Subset the  df on the list so that it only includes only the isolated tracks (clusters containing a single track)
        

        keepTracks = map(int, dfSub['objectID'].tolist()) # List of objectIDs we want to keep (map used to convert from str object to integer)
        tracksSub = self.tracks[self.tracks['objectID'].isin(keepTracks)] # Subset the tracks that passed the filtering. We'll return this dataframe from the filtering

        ### PLOTTING ###
        fig, (ax0, ax1, ax2) = plt.subplots(ncols=3, sharex=True, sharey=True, figsize=(18, 6))   
        
        left  = 0.125  # the left side of the subplots of the figure
        right = 0.9    # the right side of the subplots of the figure
        bottom = 0.1   # the bottom of the subplots of the figure
        top = 0.9      # the top of the subplots of the figure
        wspace = 0.02   # the amount of width reserved for blank space between subplots
        hspace = 0.2   # the amount of height reserved for white space between subplots
        fig.subplots_adjust(left = left, bottom=bottom, right=right, top=top, wspace = wspace , hspace=hspace)
        
        ax1.axes.get_yaxis().set_visible(False)
        ax2.axes.get_yaxis().set_visible(False)
        ax0.axes.get_yaxis().set_visible(False)
      
        ax1.axes.get_xaxis().set_visible(False)
        ax2.axes.get_xaxis().set_visible(False)  
        ax0.axes.get_xaxis().set_visible(False)

        # ax0.set_aspect(1)
        # ax1.set_aspect('auto')
        # ax2.set_aspect('auto')

        # ax0.set_aspect(6080, 3420)
        # ax1.set_aspect(6080, 3420)
        # ax2.set_aspect(6080, 3420)

        scatter = ax0.scatter(self.tracks['x_c'], self.tracks['y_c'], c = self.tracks['objectID'], s = 0.2)
        ax0 = scatter.axes
        ax0.invert_yaxis()

        df.plot(ax=ax1, column = 'clusterID', marker = ".", markersize = 0.2)
        dfSub.plot(ax=ax2, column = 'clusterID', marker = ".", markersize=0.2)
        
        currentTime = datetime.now() # Use this if you need to time-stamp result file
        currentTime=('%02d-%02d-%02d'%(currentTime.hour,currentTime.minute,currentTime.second))
        fig.savefig(f'../testResults/{currentTime}_BeforeAndAfterFiltering_eps_{self.eps_distance}.png', dpi=600)
        ### ####
        
        return tracksSub



