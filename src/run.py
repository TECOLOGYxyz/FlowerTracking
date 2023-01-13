# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 12:50:10 2021

@author: au309263
"""

import pandas as pd
from track import tracker
#from filtering import sieve
#from DBSCANFiltering import DBSCANsieve
from distanceFiltering import distanceSieve
from evaluate import evaluator
#import os
import time
import os
from scipy.spatial import distance as dist
import os
import re
import numpy as np
br = '\n'


############### EXAMPLE RUNS ###############

#
##
### First let's run the tracking algorithm on some simulated data:
##
#

# sims = pd.read_csv(r"./data/simulation/maxgapExample.csv") # Read the simulated data
# sims['filename'] = "simulation_run" # Add a filename column to the dataframe
# sims['x_min'] = sims["x_c"] - 1 # Add top left, bottom right bounding box coordinates (to simulate format of detection)
# sims['x_max'] = sims["x_c"] + 1
# sims['y_min'] = sims["y_c"] - 1
# sims['y_max'] = sims["y_c"] + 1

# # # We are ready to run tracking on the file
# t = tracker(max_gap = 0, max_distance = 0,  running_mean_threshold = 1, results_filename = r"U:\BITCue\Projekter\TrackingFlowers/maxgapExample_tracked_delete.csv", detections = sims, verbose = True) # Instantiate the class instance and pass in the threshold for max_disappeared and the list of frames.
# t.track() # Run the tracking algorithm.

### Now we can run the evalutor on the tracked vs ground truth dataframes to get tracking accuracy scores
# gt = pd.read_csv(r"U:\BITCue\Projekter\TrackingFlowers\data\simulation\maxgapExample.csv")
# dt = pd.read_csv(r"U:\BITCue\Projekter\TrackingFlowers/maxgapExample_tracked_delete.csv")

# results_filename = "U:\BITCue\Projekter\TrackingFlowers\delete_evaluate.csv"

# e = evaluator(dt, gt, results_filename, verbose = True)
# e.run()





#
##
### Now let's track some real flowers
##
#


# Read detection/annotation file
gt = pd.read_csv(r"U:\BITCue\Projekter\TrackingFlowers\data\annotations\2020_05_17_NorwayAnnotations_NARS-04_IndividualAnnotations_FRCNN_Metrics.csv")
# # In this case, frame numbers are hidden in the filename. We'll extract them and  give them their own column.
gt['frame'] = gt.filename.str.extract('(\d{6})').astype(int)

# Bounding boxes are given as coordinates for top left, bottom right corner. We need center x and y.
gt['x_c'] = (gt['x_min'] + gt['x_max']) / 2
gt['y_c'] = (gt['y_min'] + gt['y_max']) / 2


# # We are ready to run tracking on the file
# t = tracker(10, 0, 1, r"U:\BITCue\Projekter\TrackingFlowers\2020_05_17_NorwayAnnotations_NARS-04_IndividualAnnotations_FRCNN_Metrics_2.csv", gt, True) # Instantiate the class instance and pass in the threshold for max_disappeared and the list of frames.
# t.track() # Run the tracking algorithm.


### Now we can run the evalutor on the tracked vs ground truth dataframes to get tracking accuracy scores
#gt = pd.read_csv(r"U:\BITCue\Projekter\TrackingFlowers\data\annotations\2020_05_15_NorwayAnnotations_THUL-01_IndividualAnnotations_FRCNN_Metrics.csv")
dt = pd.read_csv(r"U:\BITCue\Projekter\TrackingFlowers\parameterTest_NARS-04_maxDisap_10_runMean_1_maxDist_0.csv")
gt['object'] = gt['id_gt']

gt['object'] = gt.apply(lambda x: int(''.join(filter(str.isdigit, x['object']))), axis=1)

results_filename = "U:\BITCue\Projekter\TrackingFlowers\delete_evaluate_3.csv"

e = evaluator(dt, gt, results_filename, verbose = True)
e.run()
