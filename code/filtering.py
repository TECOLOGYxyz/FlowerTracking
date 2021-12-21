# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 20:14:12 2021

@author: au309263
"""
from shapely.geometry import Polygon, LineString
import pandas as pd # Replace with cudf if performance is too slow?
from collections import OrderedDict
import numpy as np
from scipy.spatial import distance as dist
from scipy.spatial import ConvexHull
#from scipy.ndimage.filters import uniform_filter1d
import matplotlib.pyplot as plt
import time
import itertools


br = "\n"



"""
TO-DO

- Remmove single points
- Establish straight line between two-point tracks
- Establish triangle between three-point tracks
- Establish polygon from vertices of the convex hull of n-point tracks (n > 3)
- Check if any lines overlap and remove both if they do
- Check if any remaining lines overlap with any polygons, remove both line and polygon if so
- Check if any polygons overlap and remove both if they do
- Output filtered track file

"""

#### FUNCTIONS ####

class sieve():
    def __init__(self, tracks):
        self.tracks = tracks
        
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

    
        
        #print(f'Points:{br}{points}')
        #print(f'Lines:{br}{lines}')
        #print(f'Triangles:{br}{triangles}')
        #print(f'Polygons:{br}{polygons}')
        #print(f'PolyLengths:{br}{polyLengths}')
        
        
        #return self.points, self.lines, self.triangles, self.polygons, self.polyLengths

    def remove_from_list(self, list_to_remove_from, indexes_to_remove):
        
            for i in sorted(set(indexes_to_remove), reverse=True):
                del list_to_remove_from[i]
            return list_to_remove_from
    
    def get_change(self, previous, current):
        try:
            percentage = abs(previous - current)/max(previous, current) * 100
        except ZeroDivisionError:
            percentage = float('inf')
        return percentage    
    
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
                
        

    # def cart_product(listOfPolygons):
    #     print("Calculating cartesian products of polygons")
    #     cartProduct = []
    #     #print("List of polygons: ",br, listOfPolygons)
    #     listOfPolygons = [i.tolist() for i in listOfPolygons]
    #     #print("List of polygons after converstion: ",br, listOfPolygons)
    #     for i in listOfPolygons:
    #         #print("i", i)
    #         for j in listOfPolygons:
    #             if not i == j and [j,i] not in cartProduct:
    #             #if (i == j).all():# and [j,i] not in cartProduct:
    #                 #print("jello")
    #                 cartProduct.append([i,j])
        
    #     return cartProduct

    def filter_points():
        pass
    
    def filter_lines_on_lines(self, list_of_lines):
        
        lines_to_remove = []
        
        class Point:
        	def __init__(self,x,y):
        		self.x = x
        		self.y = y
        
        def ccw(A,B,C): # Look for intersection between lines
        	return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)
        
        def intersect(A,B,C,D):
        	return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

        for i in list_of_lines:
            pointsA = list_of_lines[i]
            a = Point(pointsA[0][0], pointsA[0][1])
            b = Point(pointsA[1][0], pointsA[1][1])
            
            for j in list_of_lines:
                pointsB = list_of_lines[j]
                if not pointsA == pointsB:
                    #print("j",j)
                    c = Point(pointsB[0][0], pointsB[0][1])
                    d = Point(pointsB[1][0], pointsB[1][1])
                
                    if intersect(a,b,c,d):
                        lines_to_remove.append(i)
                        lines_to_remove.append(j)
                        continue
        
        #print(f'Removing {len(set(lines_to_remove))} overlapping lines')
        self.remove_from_list(list_of_lines, set(lines_to_remove))
        return list_of_lines # Return the lines that didn't overlap


    def filter_lines_on_polygons(self, list_of_lines, list_of_polygons):
        lines_to_remove = []
        
        for l in list_of_lines:
            line = list_of_lines[l] 
            line = LineString(line)
           
            for t in list_of_polygons:
                points = list_of_polygons[t]
                #print("Points", points)
                polygon = Polygon(points)
               
                if line.intersects(polygon):
                    lines_to_remove.append(l)
                    #continue
        print(f'Removing {len(set(lines_to_remove))} lines overlapping with triangles')
        self.remove_from_list(list_of_lines, set(lines_to_remove))
        return list_of_lines
           
    
    def filter_triangles_on_triangles(self, list_of_triangles):
        triangles_to_remove = []
        
        for t in list_of_triangles:
            #print("t", t)
            pointsA = list_of_triangles[t]
            #print("Points A", pointsA)
            triangleA = Polygon(pointsA)
            
            for r in list_of_triangles:
                pointsB = list_of_triangles[r]
                if not pointsA == pointsB:
                    #print("r", r)
                    triangleB = Polygon(pointsB)
                   
                    if triangleA.intersects(triangleB):
                        triangles_to_remove.append(t)
                        triangles_to_remove.append(r)
         
        
        print(f'Removing {len(set(triangles_to_remove))} overlapping triangles')
        list_of_triangles = self.remove_from_list(list_of_triangles, set(triangles_to_remove))
        return list_of_triangles


    def filter_triangles_on_polygons(self, list_of_triangles, list_of_polygons):
        triangles_to_remove = []
        
        for t in list_of_triangles:
            #print("t", t)
            pointsA = list_of_triangles[t]
            #print(f'Triangle points {pointsA}')
            triangle = Polygon(pointsA)
            
            for r in list_of_polygons:
                pointsB = list_of_polygons[r]
                polygon = Polygon(pointsB)
                   
                if triangle.intersects(polygon):
                    triangles_to_remove.append(t)

        #print(list_of_triangles)            
        #print(triangles_to_remove)
        print(f'Removing {len(set(triangles_to_remove))} triangles overlapping with polygons')
        list_of_triangles = self.remove_from_list(list_of_triangles, triangles_to_remove)
        return list_of_triangles


    def filter_polygons_on_polygons(self, list_of_polygons, polygon_lengths):
        polygons_to_remove = []
        print(f'Polygon lengths: {br}{polygon_lengths}')

        def filter_two_polygons(two_polygons):
            if polygon_lengths[two_polygons[0]] == polygon_lengths[two_polygons[1]]: # If polygons contain the same number of points, remove both
                polygons_to_remove.extend(two_polygons)
                
            else:
                if self.get_change(polygon_lengths[two_polygons[0]], polygon_lengths[two_polygons[1]]) < 40: # If difference is less than 10%, remove both
                    print(f'Difference is less than 20% ({self.get_change(polygon_lengths[two_polygons[0]], polygon_lengths[two_polygons[1]])}). Removing {two_polygons[0]} {polygon_lengths[two_polygons[0]]} points  and {two_polygons[1]} {polygon_lengths[two_polygons[1]]} points')
                    polygons_to_remove.extend(two_polygons)
                else:                                
                    if polygon_lengths[two_polygons[0]] > polygon_lengths[two_polygons[1]]: # If difference is more than 20%, remove the smallest
                        print(f'{polygon_lengths[two_polygons[0]]} for {two_polygons[0]} more than {polygon_lengths[two_polygons[1]]} for {two_polygons[1]}. Removing smallest ({two_polygons[1]}) ({self.get_change(polygon_lengths[two_polygons[0]],polygon_lengths[two_polygons[1]])})')
                        polygons_to_remove.append(two_polygons[1])
                    else:
                        print(f'{polygon_lengths[two_polygons[1]]} for {polygon_lengths[two_polygons[1]]} more than {polygon_lengths[two_polygons[0]]} for {polygon_lengths[two_polygons[0]]}. Removing smallest ({two_polygons[0]} ({self.get_change(polygon_lengths[two_polygons[1]], polygon_lengths[two_polygons[0]])})')
                        polygons_to_remove.append(two_polygons[0])


        
        for t in list_of_polygons:
            overlaps = {}
            print(f'Polygons to remove {br}{polygons_to_remove}')
            if t not in polygons_to_remove:
                #print("t: ", t)
                pointsA = list_of_polygons[t]
                polyA = Polygon(pointsA)
                overlaps[t] = pointsA
                
                for j in list_of_polygons:
                    if j not in polygons_to_remove:
                        #print("j: ", j)
                        pointsB = list_of_polygons[j]
                        if not pointsA==pointsB:
                            polyB = Polygon(pointsB)
                            
                            if polyA.intersects(polyB):
                                overlaps[j] = pointsB
                
                
                polygonKeys = sorted(overlaps, key=lambda k: polygon_lengths[k], reverse=True)                
                
                if len(overlaps) > 1:
                    print("There are overlapping polygons")
                    
                    
                    print(polygonKeys)
                    print(len(polygonKeys))
                    
                    if len(polygonKeys) > 2:
                        print("Length more than two")
                        polygons_to_remove.extend(polygonKeys[1:])
                        
                        
                        print(f'Remove these: {polygonKeys[2:]}')
                        print(f'Keep these: {polygonKeys[:2]}')
                        
                        polygonKeys = polygonKeys[:2]
                        filter_two_polygons(polygonKeys)
                    if len(polygonKeys) == 2:
                        print("Length is two.", polygonKeys)
                        filter_two_polygons(polygonKeys)
                else:
                    overlaps = {}
                    
        print(f'Removing {len(set(polygons_to_remove))} polygons ovelapping with polygons')
        list_of_polygons = self.remove_from_list(list_of_polygons, set(polygons_to_remove))    
        return list_of_polygons
                        

    def run(self):
        self.separate()
        self.convex_hull(self.polygons) # Get the hull vertices for the polygons. This also adds polygons with colinear points to the lines dictionary

        flines = self.filter_lines_on_lines(self.lines) # Remove overlapping lines
        flines = self.filter_lines_on_polygons(flines, self.triangles) # Remove lines overlapping with triangles
        flines = self.filter_lines_on_polygons(flines, self.polyHulls) # Remove lines overlapping with polygons
        
        ftriangles = self.filter_triangles_on_triangles(self.triangles) # Remove overlapping triangles
        ftriangles = self.filter_triangles_on_polygons(ftriangles, self.polyHulls) # Remove triangles overlapping with polygons hulls
        
        allPolyHulls = self.polyHulls
        
        fpolygons = self.filter_polygons_on_polygons(self.polyHulls, self.polyLengths) # Filter polygons overlapping with polygons
        
        # ### Return the objectIDs that have made their way through the filter
        tracks_to_keep = []
        
        # if flines.keys():
        #     for o in flines.keys():
        #         tracks_to_keep.append(o)
        
        if ftriangles.keys():
            for o in ftriangles.keys():
                tracks_to_keep.append(o)
        
        if fpolygons.keys():
            for o in fpolygons.keys():
                tracks_to_keep.append(o)
        
        print(f'Tracks to keep: {br}{tracks_to_keep}')
        print("All poly hulls: ", allPolyHulls)
        return tracks_to_keep, self.polyHulls, allPolyHulls