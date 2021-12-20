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
        
        
    def gen(self):
        t = self.tracks.groupby('objectID')
        for i,g in t: # Generator that yields next group in tracks dataframe
            oid = g['objectID'].iloc[0]
            x_cs = g['x_c'].tolist()
            y_cs = g['y_c'].tolist()
            p = list(map(list, zip(x_cs, y_cs)))
            yield oid, p
    
    
    def separate(self):
        
        points = {}
        lines = {}
        triangles = {}
        polygons = {}
        polyLengths = {}
        
        for oid, p in self.gen(): # Take next group in tracks dataframe and split into correct dictionary according to number of points the track contains
            if len(p) == 1: # Get single points
                points[oid] = p
                
            if len(p) == 2: # Get lines
                lines[oid] = p
                
            if len(p) == 3: # Get triangles
                triangles[oid] = p

            if len(p) > 3: # Get polygons
                polygons[oid] = p
                
        for p in polygons:
            polyLengths[p] = len(polygons[p])

    
        
        #print(f'Points:{br}{points}')
        #print(f'Lines:{br}{lines}')
        #print(f'Triangles:{br}{triangles}')
        #print(f'Polygons:{br}{polygons}')
        #print(f'PolyLengths:{br}{polyLengths}')
        
        
        return points, lines, triangles, polygons, polyLengths

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
    
    def convex_hull(self, points): # Calculate the convex hull of points
        #print("Calculating convex hulls")
        #points = np.array([[1, 2],[1, 4],[4, 1], [2,2.5], [3.5,3.5]])
        hulls = []
        p = points
        #print(p)
        p = np.array(p)
        #print("Points: ", p)
        hull = ConvexHull(p)
        #print("Hull vertices: ", p[hull.vertices])
        hulls.append(p[hull.vertices])
            
        return hulls[0].tolist()

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
        
        def ccw(A,B,C):
        	return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)
        
        def intersect(A,B,C,D):
        	return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

        for i in list_of_lines:
            #print("i", i)
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
        
        print(f'Removing {len(set(lines_to_remove))} overlapping lines')
        self.remove_from_list(list_of_lines, set(lines_to_remove))
        return list_of_lines # Return the lines that didn't overlap


    def filter_lines_on_polygons(self, list_of_lines, list_of_polygons):
        lines_to_remove = []
        
        for l in list_of_lines:
            line = list_of_lines[l] 
            line = LineString(line)
           
            for t in list_of_polygons:
                points = list_of_polygons[t]
                triangle = Polygon(points)
               
                if line.intersects(triangle):
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
        
        for t in list_of_polygons:
            #print("t", t)
            pointsA = list_of_polygons[t]
            polygonA = Polygon(pointsA)
            
            for p in list_of_polygons: # Replace with itertools.product
                pointsB = list_of_polygons[p]
                if not pointsA==pointsB:
                    #print("r", p)
                    
                    polygonB = Polygon(pointsB)
                    
                    if polygonA.intersects(polygonB):
                        if polygon_lengths[t] == polygon_lengths[p]: # If polygons contain the same number of points, remove both
                            polygons_to_remove.append(t)
                            polygons_to_remove.append(p)
                        else:
                            if self.get_change(polygon_lengths[t], polygon_lengths[p]) < 30: # If difference is less than 10%, remove both
                                print(f'Difference is less than 20% ({self.get_change(polygon_lengths[t], polygon_lengths[p])}). Removing {t} and {p}')
                                polygons_to_remove.append(t)
                                polygons_to_remove.append(p)
                            else:                                
                                if polygon_lengths[t] > polygon_lengths[p]: # If difference is more than 20%, remove the smallest
                                    print(f'{polygon_lengths[t]} for {t} more than {polygon_lengths[p]} for {t}. Removing smallest ({p})')
                                    polygons_to_remove.append(p)
                                else:
                                    print(f'{polygon_lengths[p]} for {p} more than {polygon_lengths[t]} for {t}. Removing smallest ({t})')
                                    polygons_to_remove.append(t)
                                    
        print(f'Removing {len(set(polygons_to_remove))} polygons ovelapping with polygons')
        list_of_polygons = self.remove_from_list(list_of_polygons, set(polygons_to_remove))    
        return list_of_polygons


    def run(self):
        #self.separate(tracks)
        points, lines, triangles, polygons, polyLengths = self.separate()

        flines = self.filter_lines_on_lines(lines) # Remove overlapping lines
        flines = self.filter_lines_on_polygons(flines, triangles) # Remove lines overlapping with triangles
        
        ftriangles = self.filter_triangles_on_triangles(triangles) # Remove overlapping triangles
        
        ### Create convex hulls for each polygon and return vertices
        
        polyHulls = {}
        for p in polygons:
            #print("Polygon: ", br, polygons[p])
            h = self.convex_hull(polygons[p])
            #print("Hull: ", br, h)
            polyHulls[p] = h
            
        ###
        
        ftriangles = self.filter_triangles_on_polygons(ftriangles, polyHulls) # Remove triangles overlapping with polygons hulls
        flines = self.filter_lines_on_polygons(flines, polyHulls) # Remove lines overlapping with polygon hulls
        fpolygons = self.filter_polygons_on_polygons(polyHulls, polyLengths) # Filter polygons overlapping with polygons
        
        ### Return the objectIDs that have made their way through the filter
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
        
        return tracks_to_keep, polyHulls
        
    
        
        





# fig, ax2 = plt.subplots(figsize=(15,10))
# ax2.set_xlim(0, 6080)
# ax2.set_ylim(0, 3420)

# for h in hulls:
#     print(h)
#     t = hulls[h]
#     print(t)
    #h = np.array(h)
    #ax2.scatter(h[::1,0], h[::1,1], zorder = -1, s = 40)
    #ax2.fill(h[::1,0], h[::1,1], zorder = -1)




# # Remove single points:
    
    

# Check for overlapping lines
## Remove both

# Check for lines overlapping with triangles
## Remove line

# Check for lines overlapping with polygons (convex hulls)
## Remove line


# Check for triangles overlapping triangles
## Remove both

# Check for triangles overlapping polygons (convex hulls)
## Remove triangles

# Check for polygons overlapping polygons
## If difference < 5%
### remove smallest
## If difference > 5%
### Remove both


#What is left?




#print(polygons, br)

#hulls = convex_hull(polygons)


# for h in hulls:
#     #print(h)
#     ax1.scatter(h[::1,0], h[::1,1], zorder = -1, s = 2)
#     ax1.fill(h[::1,0], h[::1,1], zorder = -1)
    
    

#c = cart_product(hulls)

#print(h, br)
#print(c, br)


#t = [[Polygon(np.array(p1)).intersects(Polygon(np.array(p2)))] for (p1,p2) in c]
#print(t)



# fig, res = plt.subplots(nrows = 1, ncols = 2, figsize = (12.2, 3.4))

# res[0].set_xlim([0, 6080])
# res[0].set_ylim([0, 3420])

# res[1].set_xlim([0, 6080])
# res[1].set_ylim([0, 3420])


# for h in hulls:
#     res[0].scatter(h[::1,0], h[::1,1], zorder = 1, s = 2)
#     res[0].fill(h[::1,0], h[::1,1], zorder = -1)
    

# for p in polygons:
#     print(p)
#     x = [i[0] for i in p]
#     y = [i[1] for i in p]
    
#     res[1].scatter(x, y, s = 1, zorder = 1)




# #tracks.objectID.astype('category')
# tracks['objectID'] = tracks['objectID'].astype('category')
# print(tracks['objectID'].dtypes)
# print(tracks['objectID'])
# colors = {'0':'red', '1':'blue', '2':'green', '3':'black', '4':'brown', '5':'yellow'}

#print(tracks)
#tracks.plot.scatter(x = 'x_c', y = 'y_c', c=tracks['objectID'].apply(lambda x: colors[str(x)]))


# #plt.plot(points[:,0], points[:,1], 'o')
# #for simplex in hull.simplices:
# #    plt.plot(points[simplex, 0], points[simplex, 1], 'k-')

# #print(points)
# #print(hull.simplices)


# # plt.plot(points[hull.vertices,0], points[hull.vertices,1], 'r--', lw=2)
# # plt.plot(points[hull.vertices[0],0], points[hull.vertices[0],1], 'ro')

# # plt.plot(points2[hull2.vertices,0], points2[hull2.vertices,1], 'r--', lw=2)
# # plt.plot(points2[hull2.vertices[0],0], points2[hull2.vertices[0],1], 'ro')


# # plt.show()

# #(hull.vertices)

# # x = []
# # y = []
# # x2 = []
# # y2 = []


# # for v in hull.vertices:
# #     #print(points[v][0])
# #     x.append(points[v][0])
# #     y.append(points[v][1])
  
    
# # for v in hull2.vertices:
# #     #print(points[v][0])
# #     x2.append(points2[v][0])
# #     y2.append(points2[v][1])
  

# #p1 = Polygon(points)
# #p2 = Polygon(points2)

# #print(p1.intersects(p2))

# plt.figure(figsize=(20, 20))
# plt.axis('equal')

# plt.scatter(points[::1,0], points[::1,1], s = 90)
# plt.fill(x,y)


# plt.scatter(points2[::1,0], points2[::1,1], s = 90)
# plt.fill(x2,y2)

# plt.show()

# #print(points2[::1,0])



# p1 = [[[1,2], [2,1], [3,4], [3,2]],[[3,1], [2,4], [3,5]],[[7,4], [5,4], [8,9], [7.5,7.5]],[[5,6], [7,5], [11,7]]]
# #p1 = [[['a'], ['b']], [['c'], ['d']], [['e'], ['f']]]
# #p2 = [[[7,4], [5,4], [8,9]],[[5,6], [7,5], [11,7]]]

# #t = [[p1, p2] for (p1,p2) in product(p1, p2)]

# #print(t)
# #print(np.array(t[0][0]))
# #print(Polygon(np.array(t[0][0])).intersects(Polygon(np.array(t[0][1]))))

# #print([[p1] for p1 in product(p1, repeat = 2)])

# #t = [[Polygon(np.array(p1)).intersects(Polygon(np.array(p2)))] for (p1,p2) in product(p1, p1)]
# #print(t)





                
# #print(cart_product(p1))




# fig = plt.figure()

# ax1 = fig.add_subplot(211)





# #print(br,convex_hull(p1))



# ax2 = fig.add_subplot(212)

# h = convex_hull(p1)

# for p in p1:
#     #print(p)
#     x = [i[0] for i in p]
#     y = [i[1] for i in p]
    
#     ax2.scatter(x, y, s = 50, zorder = 1)

# for c in h:
#     ax2.fill(c[::1,0], c[::1,1], zorder = -1)

# cart_product(h)

# #t = [[Polygon(np.array(p1)).intersects(Polygon(np.array(p2)))] for (p1,p2) in cart_product(h)]


# plt.show()



