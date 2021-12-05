# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 20:14:12 2021

@author: au309263
"""
from shapely.geometry import Polygon
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
tracks = pd.read_csv(r'testResults/trackResults7.csv')
print(tracks)

#### NORMALIZE X AND Y ####
#tracks['x_c'] = tracks['x_c']/6080
#tracks['y_c'] = tracks['y_c']/3420


#### FUNCTIONS ####
def convex_hull(points): # Calculate the convex hull of points
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


tracksGrouped = tracks.groupby(['objectID'])

polygons = []

for i,group in tracksGrouped:
    if not len(group) <= 3:
        polygon = []
        for i,line in group.iterrows():
            point = [line['x_c'], line['y_c']]
            polygon.append(point)
        polygons.append(polygon)
    
#print(polygons, br)

hulls = convex_hull(polygons)


# for h in hulls:
#     #print(h)
#     ax1.scatter(h[::1,0], h[::1,1], zorder = -1, s = 2)
#     ax1.fill(h[::1,0], h[::1,1], zorder = -1)
    
    

c = cart_product(hulls)

#print(h, br)
#print(c, br)


t = [[Polygon(np.array(p1)).intersects(Polygon(np.array(p2)))] for (p1,p2) in c]
#print(t)



fig, res = plt.subplots(nrows = 1, ncols = 2, figsize = (12.2, 3.4))

res[0].set_xlim([0, 6080])
res[0].set_ylim([0, 3420])

res[1].set_xlim([0, 6080])
res[1].set_ylim([0, 3420])


for h in hulls:
    res[0].scatter(h[::1,0], h[::1,1], zorder = 1, s = 2)
    res[0].fill(h[::1,0], h[::1,1], zorder = -1)
    

for p in polygons:
    print(p)
    x = [i[0] for i in p]
    y = [i[1] for i in p]
    
    res[1].scatter(x, y, s = 1, zorder = 1)




#tracks.objectID.astype('category')
tracks['objectID'] = tracks['objectID'].astype('category')
print(tracks['objectID'].dtypes)
print(tracks['objectID'])
colors = {'0':'red', '1':'blue', '2':'green', '3':'black', '4':'brown', '5':'yellow'}

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



