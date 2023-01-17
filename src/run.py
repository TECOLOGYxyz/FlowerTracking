# -*- coding: utf-8 -*-

# Import local packages
from track import tracker
from filter import filterer
from evaluate import evaluator

# Import global packages
import pandas as pd

br = '\n'


############### EXAMPLE RUNS ###############

#
##
### First let's run the tracking algorithm on some simulated data:
##
#

sims = pd.read_csv(r"./data/simulation/maxgapExample.csv") # Read the simulated data
sims['filename'] = "simulation_run" # Add a filename column to the dataframe
sims['x_min'] = sims["x_c"] - 1 # Add top left, bottom right bounding box coordinates (to simulate format of detection)
sims['x_max'] = sims["x_c"] + 1
sims['y_min'] = sims["y_c"] - 1
sims['y_max'] = sims["y_c"] + 1

# # We are ready to run tracking on the file
t = tracker(max_gap = 0, max_distance = 0,  running_mean_threshold = 1, results_filename = r"maxgapExample_tracked.csv", detections = sims, verbose = True) # Instantiate the class instance and pass in the threshold for max_disappeared and the list of frames.
t.track() # Run the tracking algorithm.

## Now we can run the evalutor on the tracked vs ground truth dataframes to get tracking accuracy scores
gt = pd.read_csv(r"./data\simulation\maxgapExample.csv")
gt['id_gt_int'] = gt['object'] # The evaluator needs a column named "id_gt" with integer objects IDs for the ground truth. For the simulated data, we can just use the original object ids.

dt = pd.read_csv(r"maxgapExample_tracked.csv")
dt.rename({'objectID': 'id_tr'}, axis=1, inplace=True) # The evaluator needs a column named "id_gt" with integer objects IDs for the ground truth. For the simulated data, we can just use the original object IDs.

results_filename = "maxgapExample_tracked_evaluated.csv"
e = evaluator(dt, gt, results_filename, verbose = True)
e.run()


#
##
### Now let's track some real flowers
##
#

# Read detection/annotation file
gt = pd.read_csv(r".\data\annotations\2020_05_17_NorwayAnnotations_NARS-04_IndividualAnnotations_FRCNN_Metrics.csv")

# In this case, frame numbers are hidden in the filename. We'll extract them, convert them to a continous sequence and  give them their own column.
f = list(set(gt['filename'].tolist())) # Make a list of image filenames
f.sort(key=lambda x: int(''.join(filter(str.isdigit, x)))) # Sort the filenames based on extracted digits in the filename
d = {k: v+1 for v, k in enumerate(f)} # Make a dictionary with index
gt['frame'] = gt['filename'].map(d)

# Bounding boxes are given as coordinates for top left, bottom right corner. We need center x and y.
gt['x_c'] = (gt['x_min'] + gt['x_max']) / 2
gt['y_c'] = (gt['y_min'] + gt['y_max']) / 2

# # We are ready to run tracking on the file
t = tracker(10, 500, 10, r"NARS-04_10_500_10_tracked.csv", gt, True) # Instantiate the class instance and pass in the threshold for max_disappeared and the list of frames.
t.track() # Run the tracking algorithm.

## Now we can run the evalutor on the tracked vs ground truth dataframes to get tracking accuracy scores
dt = pd.read_csv( r"NARS-04_10_500_10_tracked.csv")
dt.rename({'objectID': 'id_tr'}, axis=1, inplace=True)

gt['id_gt_int'] = gt.apply(lambda x: int(''.join(filter(str.isdigit, x['id_gt']))), axis=1)

results_filename = "NARS-04_10_500_10_tracked_evaluated.csv"

e = evaluator(dt, gt, results_filename, verbose = True)
e.run()


#
##
### We can also run the evaluator directly on csv files
##
#

gt = pd.read_csv(r".\data\annotations\2020_05_17_NorwayAnnotations_NARS-04_IndividualAnnotations_FRCNN_Metrics.csv")
dt = pd.read_csv( r"NARS-04_10_500_10_tracked.csv")

f = list(set(gt['filename'].tolist())) # Make a list of image filenames
f.sort(key=lambda x: int(''.join(filter(str.isdigit, x)))) # Sort the filenames based on extracted digits in the filename
d = {k: v+1 for v, k in enumerate(f)} # Make a dictionary with index

gt['x_c'] = (gt['x_min'] + gt['x_max'])/2
gt['y_c'] = (gt['y_min'] + gt['y_max'])/2
gt['frame'] = gt['filename'].map(d) # Create a frame column by mapping filename to dictionary
gt['id_gt_int'] = gt.apply(lambda x: int(''.join(filter(str.isdigit, x['id_gt']))), axis=1)

dt.rename({'objectID': 'id_tr'}, axis=1, inplace=True)
dt['frame'] = dt['filename'].map(d) # Create a frame column by mapping filename to dictionary 

results_filename = "NARS-04_10_500_10_tracked_evaluated_fromFile.csv"

e = evaluator(dt, gt, results_filename, verbose = True)
e.run()


#
##
### Let's try the filtering algorithm
##
#

dt = r'NARS-04_10_500_10_tracked.csv'

gt = pd.read_csv(r".\data\annotations\2020_05_17_NorwayAnnotations_NARS-04_IndividualAnnotations_FRCNN_Metrics.csv")
gt['id_gt_int'] = gt.apply(lambda x: int(''.join(filter(str.isdigit, x['id_gt']))), axis=1)

# Run filtering
d = filterer(dt, eps_distance = 350)
filteredTracks = d.run()
#filteredTracks.to_csv(r'NARS-04_10_500_10_tracked_filtered.csv') # Save the filtered tracks to csv

# Evaluate the filtered tracks
filteredTracks.rename({'objectID': 'id_tr'}, axis=1, inplace=True)
gtSub = gt.merge(filteredTracks, on=['filename','x_min', 'x_max', 'y_min', 'y_max'], how='inner', indicator=True) # We need to evaluate filtered tracks based on ground truth that only contains the filtered data 
#gtSub.to_csv(r'NARS-04_GT_filtered.csv') # Save subsetted ground truth to csv

e = evaluator(filteredTracks, gtSub, "hello.csv", verbose = True)
res = e.run()

l = len(filteredTracks['id_tr'].unique())
print(f'{res[1]} mismatches with {l} tracks kept')


### END OF SCRIPT ###