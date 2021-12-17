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

#### PATH TO TRACKS ####
tracks = pd.read_csv(r'../testResults/_parameterTest_NARS-04_3\parameterTest_NARS-04_maxDisap_0_runMean_0_maxDist_0.csv')
print(tracks)


#### NORMALIZE X AND Y ####
#tracks['x_c'] = tracks['x_c']/6080
#tracks['y_c'] = tracks['y_c']/3420


#### FUNCTIONS ####

class sieve():
    def __init__(self, tracks):
        self.tracks = tracks
        
        
    def gen(self):
        t = tracks.groupby('objectID')

        for i,g in t: # Generator that yields next group in tracks dataframe
            oid = g['objectID'].iloc[0]
            x_cs = g['x_c'].tolist()
            y_cs = g['y_c'].tolist()
            p = list(map(list, zip(x_cs, y_cs)))
            yield oid, p
    
    def separate(self, tracks):
        
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

    
        
        print(f'Points:{br}{points}')
        print(f'Lines:{br}{lines}')
        print(f'Triangles:{br}{triangles}')
        print(f'Polygons:{br}{polygons}')
        print(f'PolyLengths:{br}{polyLengths}')
        
        
        return points, lines, triangles, polygons, polyLengths 
            
        # points = []
        # lines = []
        # triangles = []
        # polygons = []
        # polyID = 0
        # polyLengths = OrderedDict()

        # # Get single points
        
        
        # for i,group in tracksGrouped:
        #     if len(group) == 1: # Get single points
        #         point = []
        #         for i,row in group.iterrows():
        #             p = [row['x_c'], row['y_c']]
        #             point.append(p)
        #         points.append(point)
        #     if len(group) == 2: # Get lines
        #         line = []
        #         for i,row in group.iterrows():
        #             point = [row['x_c'], row['y_c']]
        #             line.append(point)
        #         lines.append(line)
        #     if len(group) == 3: # Get triangles
        #         triangle = []
        #         for i,row in group.iterrows():
        #             point = [row['x_c'], row['y_c']]
        #             triangle.append(point)
        #         triangles.append(triangle)
        #     if len(group) > 3: # Get polygons
        #         polygon = []
        #         polyLengths[polyID] = len(group)
        #         polyID += 1
        #         for i,row in group.iterrows():
        #             point = [row['x_c'], row['y_c']]
        #             polygon.append(point)
        #         polygons.append(polygon)
        

    
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
        print("Calculating convex hulls")
        #points = np.array([[1, 2],[1, 4],[4, 1], [2,2.5], [3.5,3.5]])
        hulls = []
        for p in points:
            #print(p)
            p = np.array(p)
            print("Points: ", p)
            hull = ConvexHull(p)
            #print("Hull vertices: ", p[hull.vertices])
            hulls.append(p[hull.vertices])
            
        return hulls

    def cart_product(listOfPolygons):
        print("Calculating cartesian products of polygons")
        cartProduct = []
        #print("List of polygons: ",br, listOfPolygons)
        listOfPolygons = [i.tolist() for i in listOfPolygons]
        #print("List of polygons after converstion: ",br, listOfPolygons)
        for i in listOfPolygons:
            #print("i", i)
            for j in listOfPolygons:
                if not i == j and [j,i] not in cartProduct:
                #if (i == j).all():# and [j,i] not in cartProduct:
                    #print("jello")
                    cartProduct.append([i,j])
        
        return cartProduct

    def filter_points():
        pass
    
    def filter_lines_on_lines(self, list_of_lines):
        class Point:
        	def __init__(self,x,y):
        		self.x = x
        		self.y = y
        
        def ccw(A,B,C):
        	return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)
        
        def intersect(A,B,C,D):
        	return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

        for i in list_of_lines:
            print("i", i)
            a = Point(i[0][0], i[0][1])
            b = Point(i[1][0], i[1][1])
            
            for j in list_of_lines:
                if not i == j:
                    print("j",j)
                    c = Point(j[0][0], j[0][1])
                    d = Point(j[1][0], j[1][1])
                
                    if intersect(a,b,c,d):
                        list_of_lines.remove(i)
                        list_of_lines.remove(j)
                        continue
        
        return list_of_lines # Return the lines that didn't overlap


    def filter_lines_on_triangles(self, list_of_lines, list_of_triangles):
       
        for l in list_of_lines:
           line = LineString(l)
           
           for t in list_of_triangles:
               triangle = Polygon(t)
               
               if line.intersects(triangle):
                   list_of_lines.remove(l)
                   continue
        return list_of_lines
           
    
    def filter_triangles_on_triangles(self, list_of_triangles):
        
        triangles_to_remove = []
        
        for t in list_of_triangles:
            #print("t", t)
            triangleA = Polygon(t)
            
            for r in list_of_triangles:
                if not t == r:
                    #print("r", r)
                    triangleB = Polygon(r)
                   
                    if triangleA.intersects(triangleB):
                        triangles_to_remove.append(t)
                        triangles_to_remove.append(r)
         
        
        list_of_triangles = self.remove_from_list(list_of_triangles, triangles_to_remove)
        return list_of_triangles


    def filter_triangles_on_polygons(self, list_of_triangles, list_of_polygons):
        
        triangles_to_remove = []
        
        for t in list_of_triangles:
            #print("t", t)
            triangle = Polygon(t)
            
            for r in list_of_polygons:
                    polygon = Polygon(r)
                   
                    if triangle.intersects(polygon):
                        triangles_to_remove.append(t)
                        triangles_to_remove.append(r)
                        #continue
        
        list_of_triangles = self.remove_from_list(list_of_triangles, triangles_to_remove)
        return list_of_triangles


    def filter_polygons_on_polygons(self, list_of_polygons, polygon_lengths):
        
        polygons_to_remove = []
        
        for i, t in enumerate(list_of_polygons):
            print("t", t)
            polygonA = Polygon(t)
            
            for k, p in enumerate(list_of_polygons): # Replace with itertools.product
                if not t == p:
                    print("r", p)
                    polygonB = Polygon(p)
                    
                    if polygonA.intersects(polygonB):
                        if polygon_lengths[i] == polygon_lengths[k]: # If polygons contain the same number of points, remove both
                            polygons_to_remove.append(i)
                            polygons_to_remove.append(k)
                        else:
                            if self.get_change(polygon_lengths[i], polygon_lengths[k]) < 20: # If difference is less than 10%, remove both
                                polygons_to_remove.append(i)
                                polygons_to_remove.append(k)
                            else:                                
                                if polygon_lengths[i] > polygon_lengths[k]: # If difference is more than 20%, remove the smallest
                                    polygons_to_remove.append(k)
                                else:
                                    polygons_to_remove.append(i)
        
        list_of_polygons = self.remove_from_list(list_of_polygons, polygons_to_remove)    
        return list_of_polygons

    def run(self):
        self.separate(self.tracks)
        # points, lines, triangles, polygons, polyID, polyLengths = self.separate(self.tracks)

        # flines = self.filter_lines_on_lines(lines) # Remove overlapping lines
        # flines = self.filter_lines_on_triangles(flines, triangles) # Remove lines overlapping with triangles
        
        # ftriangles = self.filter_triangles_on_triangles(triangles)
        
        # print("Filtered lines: ", flines)
        # print("Filtered triangles: ", ftriangles)
        # #fpolygons = self.
        

s = sieve(tracks)

s.run()




# Remove single points:
    
    

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



