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
df = pd.read_csv(r"data\annotations\2020_05_23_NorwayAnnotations_NYAA-04_IndividualAnnotations_FRCNN_Metrics.csv")

#print(thul01)

df['x_c'] = (df['x_min'] + df['x_max']) / 2
df['y_c'] = (df['y_min'] + df['y_max']) / 2


#print(thul01)


a = np.array([3.4,4])
b = np.array([6,9])

def dist(a,b):
    d = np.linalg.norm(a-b)
    return d

#print(dist)

df_grouped = df.groupby(['id_gt'])

largestDist = 0

for i, g in df_grouped:
    #print(g)
    g_points = []
    for i,l in g.iterrows():
        g_points.append(np.array([l['x_c'], l['y_c']]))
        
    for p1 in g_points:
        for p2 in g_points:
            d = dist(p1, p2)
            if d > largestDist:
                print(f'{d} is larger than {largestDist}. Storing {d}')
                print(f'Distance calculated between {p1} and {p2}')
                largestDist = d
            
            
print(f'Largest dist found: {largestDist}')

# THUL-01: 449.00334074481003
# NYAA-04: 2307.41034495384
# NARS-13: 782.0206199327483
# NARS-04: 557.953851138246

    

# Find the largest distance between two points in a track. This will help us set max_distance in the tracking algorithm.


# Find the largest number of frames a track was lost and then regained. This will help us set max_disappeared in the tracking algorithm.


# 


# 