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
df = pd.read_csv(r"../data\annotations\2020_04_30_NorwayAnnotations_NARS-13_IndividualAnnotations_FRCNN_Metrics.csv")


#print(thul01)

df['x_c'] = (df['x_min'] + df['x_max']) / 2
df['y_c'] = (df['y_min'] + df['y_max']) / 2


#print(thul01)


a = np.array([3.4,4])
b = np.array([6,9])

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

meand = []
for i, g in df_grouped:
    #print(g)
    g_points = []
    dlist = []
    for i,l in g.iterrows():
        g_points.append(np.array([l['x_c'], l['y_c']]))
        
    for p1 in g_points:
        for p2 in g_points:
            d = dist(p1, p2)
            dlist.append(d)
    meand.append(sum(dlist))
print(ave(meand))

# THUL-01:
# NYAA-04: 897228.1250040481
# NARS-13: 403952.7876561521
# NARS-04:
# NARS-17: 

    

meand = []
for i, g in df_grouped:
    #print(g)
    g_points = []
    dlist = []
    for i,l in g.iterrows():
        g_points.append(np.array([l['x_c'], l['y_c']]))
        
    for p1 in g_points:
        for p2 in g_points:
            d = dist(p1, p2)
            dlist.append(d)
    meand.append(ave(dlist))
print(ave(meand))

# THUL-01:
# NYAA-04: 105.16666014360499
# NARS-13: 108.85171087792607
# NARS-04:
# NARS-17: 





# Find the largest distance between two points in a track. This will help us set max_distance in the tracking algorithm.


# Find the largest number of frames a track was lost and then regained. This will help us set max_disappeared in the tracking algorithm.


# 


# 