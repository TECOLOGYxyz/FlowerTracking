# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 15:08:22 2021

@author:
    Hjalte M. R. Mann
    TECOLOGY.xyz

In this script we'll do some analyses of the ground truth individual annotations.
We'll use the results for setting the parameters of our tracking algorithm.

"""

import pandas as pd
import numpy as np

# Input ground truth annotations
df = pd.read_csv(r"../data\annotations\2021_12_13_NorwayAnnotations_NYAA-04_IndividualAnnotations_FRCNN_Metrics.csv")


#print(thul01)

df['x_c'] = (df['x_min'] + df['x_max']) / 2
df['y_c'] = (df['y_min'] + df['y_max']) / 2



def dist(a,b):
    d = np.linalg.norm(a-b)
    return d

def ave(lst):
    return sum(lst) / len(lst)



df_grouped = df.groupby(['id_gt'])

largestDist = 0

# for i, g in df_grouped:
#     #print(g)
#     g_points = []
#     for i,l in g.iterrows():
#         g_points.append(np.array([l['x_c'], l['y_c']]))
        
#     for p1 in g_points:
#         for p2 in g_points:
#             d = dist(p1, p2)
#             if d > largestDist:
#                 print(f'{d} is larger than {largestDist}. Storing {d}')
#                 print(f'Distance calculated between {p1} and {p2}')
#                 largestDist = d
            
            
# print(f'Largest dist found: {largestDist}')

# THUL-01: 449.00334074481003
# NYAA-04: 632.9178461696273
# NARS-13: 782.0206199327483 QC
# NARS-04: 557.953851138246
# NARS-17: 615.5536126122565


# Largest distance between mean of track and each point
largestDist = 0

# for i, g in df_grouped:
#     #print(g)
#     x_cs = []
#     y_cs = []
#     g_points = []
#     for i,l in g.iterrows():
#         x_cs.append(l['x_c'])
#         y_cs.append(l['y_c'])
#         g_points.append(np.array([l['x_c'], l['y_c']]))

#     mx = ave(x_cs)
#     my = ave(y_cs)
    
#     m = np.array([mx, my]) # Mean of x and mean of y
#     for p1 in g_points:
#         d = dist(p1, m)
#         if d > largestDist:
#             print(f'{d} is larger than {largestDist}. Storing {d}')
#             print(f'Distance calculated between {p1} and {m}')
#             largestDist = d
            
            
# print(f'Largest dist found: {largestDist}')


# THUL-01: 278.2451605832456
# NYAA-04: 448.8589106287767
# NARS-13: 456.82260896011803
# NARS-04: 
# NARS-17: 376.3443382217583
    



# Mean distance per flower

# meand = []
# for i, g in df_grouped:
#     #print(g)
#     g_points = []
#     dlist = []
#     for i,l in g.iterrows():
#         g_points.append(np.array([l['x_c'], l['y_c']]))
        
#     for p1 in g_points:
#         for p2 in g_points:
#             d = dist(p1, p2)
#             dlist.append(d)
#     meand.append(sum(dlist))
# print(ave(meand))

# THUL-01:
# NYAA-04: 897228.1250040481
# NARS-13: 403952.7876561521
# NARS-04:
# NARS-17: 

    

# meand = []
# for i, g in df_grouped:
#     #print(g)
#     g_points = []
#     dlist = []
#     for i,l in g.iterrows():
#         g_points.append(np.array([l['x_c'], l['y_c']]))
        
#         print("GROUP ", i, '\n')
#         for p1 in g_points:
#             for p2 in g_points:
#                 if (p1!=p2).all():
#                     d = dist(p1, p2)
#                     dlist.append(d)
#                     print("Distance: ", d)
                    

# # A measure of how much the flowers move: Average distance to the centroid for each flower
# flower_distances = []
# for i, g in df_grouped:
#     #print(g)
#     x_cs = []
#     y_cs = []
#     g_points = [] # Points in the group
#     fd = []
    
#     for i,l in g.iterrows():
#         x_cs.append(l['x_c'])
#         y_cs.append(l['y_c'])
#         g_points.append(np.array([l['x_c'], l['y_c']]))

#     mx = ave(x_cs)
#     my = ave(y_cs)
    
#     m = np.array([mx, my]) # Centroid
    
#     for p in g_points:
#         d = dist(p, m)
#         fd.append(d)
#     flower_distances.append(ave(fd))
        
# print(flower_distances)
# print("Number of flowers: ", len(flower_distances))
# print(ave(flower_distances))
# print("SD: ", np.std(flower_distances))

# MEAN +- SD
# THUL-01: 61.94251146461619 +- 13.457573357296228
# NYAA-04: 74.80506999824438 +- 21.887652913458854
# NARS-13: 79.64964754955484 +- 36.09646690733737
# NARS-04: 81.95968592449228 +- 29.9865844156764
# NARS-17: 62.17535359604089 +- 45.948225562148046



# Average number of points in each flower
# points = []
# for i, g in df_grouped:
#     print(g)
#     points.append(g.shape[0])

# print("Points per flower: ", points)
# print("Average points per flower: ", ave(points))
# print("SD: ", np.std(points))


# MEAN +- SD
# THUL-01: 116.5 +- 40.94203219186854
# NYAA-04: 83.9047619047619 +- 33.91292036673417
# NARS-13: 57.49411764705882 +- 18.943646167087426
# NARS-04: 53.875 +- 15.649980031936144
# NARS-17: 57.53846153846154 +- 18.59121125948158






# # A measure of how much the flowers move: Average distance to the centroid for each flower for each dimension

sdxl = []
sdyl = []

for i, g in df_grouped:
    print(g)
    x_cs = []
    y_cs = []
    g_points = [] # Points in the group
    fd = []
    
    for i,l in g.iterrows():
        x_cs.append(l['x_c'])
        y_cs.append(l['y_c'])
        g_points.append(np.array([l['x_c'], l['y_c']]))

    mx = ave(x_cs)
    my = ave(y_cs)
    
    sdx = np.std(x_cs)
    sdy = np.std(y_cs)
    
    sdxl.append(sdx)
    sdyl.append(sdy)
    
    
    print("Mean x: ", mx)
    print("Mean y: ", my)

    print("SD x: ", sdx)
    print("SD y: ", sdy)

    print("VAR x: ", np.var(x_cs))
    print("VAR y: ", np.var(y_cs))
    
  
print("=====")
print("Average sdx: ", ave(sdxl))
print("Average sdy: ", ave(sdyl))

# print(flower_distances)
# print("Number of flowers: ", len(flower_distances))
# print(ave(flower_distances))
# print("SD: ", np.std(flower_distances))

# SD X,Y
# THUL-01: 34.29536984447268, 68.17660400741654
# NYAA-04: 56.61978993045123, 70.86374658894299
# NARS-13: 73.4109421621663, 53.59317990558027
# NARS-04: 73.8633237415749, 58.43851116215664
# NARS-17: 57.85321367764776, 33.177647881529325


# Find the largest distance between two points in a track. This will help us set max_distance in the tracking algorithm.


# Find the largest number of frames a track was lost and then regained. This will help us set max_disappeared in the tracking algorithm.


# 


# 