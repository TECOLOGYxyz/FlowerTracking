# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 12:50:10 2021

@author: au309263
"""

import pandas as pd
from track import tracker
import time

# ===================== Run tracking on several combinations of parameters ====

### SETTINGS ###

prefix_results_filename = "parameterTest_NARS-13"

list_max_disappeared = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160] # Maximum number of frames a track can be lost before new points will be forces into a new track.
list_running_mean_threshold = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160] # Maximum number of frames for calculating the running mean of the position of an object If there are less than this number of frames currently in the track, a mean over what is in the track will be used..
list_max_distance = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000] # If set to 0, this parameter will be ignored. If not zero, points that have a distance to tracked objects higher than this parameter will be forced into new tracks.

# list_max_disappeared = [100] # Maximum number of frames a track can be lost before new points will be forces into a new track.
# list_running_mean_threshold = [5] # Maximum number of frames for calculating the running mean of the position of an object If there are less than this number of frames currently in the track, a mean over what is in the track will be used..
# list_max_distance = [400] # If set to 0, this parameter will be ignored. If not zero, points that have a distance to tracked objects higher than this parameter will be forced into new tracks.


list_of_parameters = [(x,y,z) for x in list_max_disappeared for y in list_running_mean_threshold for z in list_max_distance] # A list of all combinations of the above parameters.

#### PATH TO DETECTIONS ####
#detections = pd.read_csv(r'../Dummy_fortracking2.csv')

detections = pd.read_csv(r"U:\BITCue\Projekter\TrackingFlowers\data\annotations\2020_04_30_NorwayAnnotations_NARS-13_IndividualAnnotations_FRCNN_Metrics.csv")
detections['frame'] = detections['filename'].str.extract('(\d{6})')
detections['x_c'] = (detections['x_min'] + detections['x_max']) / 2
detections['y_c'] = (detections['y_min'] + detections['y_max']) / 2
detections['frame'] = detections['frame'].astype('int')

frames = list(set(detections['frame'].tolist()))
frames = sorted([int(i) for i in frames])

verbose = False # Set to True if you want tracking process printed to screen and False if not


### RUN ###

for i in list_of_parameters:
    starttime = time.time()
    resultsFilename = f'../testResults/_parameterTest_NARS-13_3/{prefix_results_filename}_maxDisap_{i[0]}_runMean_{i[1]}_maxDist_{i[2]}.csv'    
    
    t = tracker(i[0], i[2], i[1], resultsFilename, frames, detections, verbose)
    
    for f in frames:
        t.track(f)
    endtime = time.time()
    print(f'Tracking done. That took {round(endtime-starttime, 3)} seconds. That is {round((endtime-starttime)/len(frames), 3)} seconds per frame.')
    t.write_tracks_file()
    tracks = pd.read_csv(resultsFilename)
    print(f'maxDis: {i[0]}, runMean: {i[1]} - Number of tracks found: {len(tracks.objectID.unique())}')

# =============================================================================