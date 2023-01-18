# -*- coding: utf-8 -*-

# Import global packages
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon, LineString, Point
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull
from datetime import datetime

# Note, EPS_DISTANCE needs to be smaller than the gap between any two polygons we want to keep and large enough to cluster polygons that we want to discard together
# EPS_DISTANCE = 281 is the highest value that keeps all tracks in THUL-01

class filterer():
    def __init__(self, tracks, eps_distance):
        if not isinstance(tracks, pd.DataFrame):
            self.tracks = pd.read_csv(tracks, sep=",", header = 0)
        else:
            self.tracks = tracks
        
        self.eps_distance = eps_distance
        
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
            #print(p)
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
            df = pd.concat([df, gpd.GeoDataFrame.from_records([{'points': p, 'objectID': str(oid), 'geometry': Point(p[0])}])])
        for oid in self.lines:
            l = self.lines[oid]
            df = pd.concat([df, gpd.GeoDataFrame.from_records([{'points': l, 'objectID': str(oid), 'geometry': LineString(l)}])])
            
        for oid in self.polyHulls:
            points = self.polyHulls[oid]
            df = pd.concat([df, gpd.GeoDataFrame.from_records([{'points': points, 'objectID': str(oid), 'geometry': Polygon(points)}])])
        
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
    
    def dist(self,a,b):
        d = np.linalg.norm(a-b)
        return d
    
    def ave(self, lst):
        return sum(lst) / len(lst)
    
    def run(self):
        self.separate() # Separate the tracks into points, lines, and polygons
        self.convex_hull(self.polygons) # Calcuate the convex hull of the polygons. This will also add colinear points to lines dictionary
        df, coords = self.geometries() # Get the geometry dataframe containing the track polygons and the centroid coordinates of which to perform the DBSCAN clustering
        
        x = df.loc[df['objectID'] == '0']        

        y = self.tracks
        y = y.loc[y['objectID'] == 0]

        ids = list(df['objectID'])
        passed = []
        
        for i,r in df.iterrows():
            oid = r['objectID']
            oidcx = r['x']
            oidcy = r['y']
            
            oidp = np.array([oidcx, oidcy])
            distances = []
            for o,p in df.iterrows():
                
                if oid != p['objectID']:
                    pcx = p['x']
                    pcy = p['y']
                    pp = np.array([pcx, pcy])
                    
                    d = self.dist(oidp, pp)
                    distances.append(d)
                    
            #print("Distances = ", distances)
            if any(i < self.eps_distance for i in distances):
                continue
            else:
                passed.append(oid)
        
        #print("Passed distance ", passed)

        l = passed

        dfSub = df[df['objectID'].isin(l)] # Subset the  df on the list so that it only includes only the isolated tracks (clusters containing a single track)
        

        keepTracks = map(int, dfSub['objectID'].tolist()) # List of objectIDs we want to keep (map used to convert from str object to integer)
        tracksSub = self.tracks[self.tracks['objectID'].isin(keepTracks)] # Subset the tracks that passed the filtering. We'll return this dataframe from the filtering

        # ### PLOTTING ###
        # fig, (ax0, ax1, ax2) = plt.subplots(ncols=3, sharex=True, sharey=True, figsize=(18, 6))   
        
        # left  = 0.125  # the left side of the subplots of the figure
        # right = 0.9    # the right side of the subplots of the figure
        # bottom = 0.1   # the bottom of the subplots of the figure
        # top = 0.9      # the top of the subplots of the figure
        # wspace = 0.02   # the amount of width reserved for blank space between subplots
        # hspace = 0.2   # the amount of height reserved for white space between subplots
        # fig.subplots_adjust(left = left, bottom=bottom, right=right, top=top, wspace = wspace , hspace=hspace)
        
        # ax1.axes.get_yaxis().set_visible(False)
        # ax2.axes.get_yaxis().set_visible(False)
        # ax0.axes.get_yaxis().set_visible(False)
      
        # ax1.axes.get_xaxis().set_visible(False)
        # ax2.axes.get_xaxis().set_visible(False)  
        # ax0.axes.get_xaxis().set_visible(False)

        # ax0.set_aspect(1)
        # ax1.set_aspect('auto')
        # ax2.set_aspect('auto')

        # scatter = ax0.scatter(self.tracks['x_c'], self.tracks['y_c'], c = self.tracks['objectID'], s = 0.2)
        # ax0 = scatter.axes
        # ax0.invert_yaxis()

        # df.plot(ax=ax1, column = 'objectID', marker = ".", markersize = 0.2)
        # dfSub.plot(ax=ax2, column = 'objectID', marker = ".", markersize=0.2)
        
        # currentTime = datetime.now() # Use this if you need to time-stamp result file
        # currentTime=('%02d-%02d-%02d'%(currentTime.hour,currentTime.minute,currentTime.second))  
        # figName = f'BeforeAndAfterFiltering_eps_{self.eps_distance}_{currentTime}.png'
        # fig.savefig(figName, dpi=600)
        # print("Figure saved at ", figName)
        # ####
        
        return tracksSub

### END OF SCRIPT ###