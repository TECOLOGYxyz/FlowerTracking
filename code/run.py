# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 12:50:10 2021

@author: au309263
"""

import pandas as pd
from track import tracker
from filtering import sieve
from DBSCANFiltering import DBSCANsieve
from evaluate import evaluator
import os
import time


# ===================== Import ground truth data ====

def impdata(camID):
    if camID == "NARS-04":
        gt = r"U:\BITCue\Projekter\TrackingFlowers\data\annotations\2020_05_17_NorwayAnnotations_NARS-04_IndividualAnnotations_FRCNN_Metrics.csv"
    if camID == "NARS-13":
        gt = r"U:\BITCue\Projekter\TrackingFlowers\data\annotations\2020_04_30_NorwayAnnotations_NARS-13_IndividualAnnotations_FRCNN_Metrics.csv"
    if camID == "THUL-01":
        gt = r"U:\BITCue\Projekter\TrackingFlowers\data\annotations\2020_05_15_NorwayAnnotations_THUL-01_IndividualAnnotations_FRCNN_Metrics.csv"
    if camID == "NYAA-04":
        gt = r"U:\BITCue\Projekter\TrackingFlowers\data\annotations\2021_12_13_NorwayAnnotations_NYAA-04_IndividualAnnotations_FRCNN_Metrics.csv"
    if camID == "NARS-17":
        gt = r"U:\BITCue\Projekter\TrackingFlowers\data\annotations\2021_12_30_NorwayAnnotations_NARS-17_IndividualAnnotations_FRCNN_Metrics.csv"
    return gt
        

# ===================== Run tracking on several combinations of parameters ====

# ### SETTINGS ###

# prefix_results_filename = "parameterTest_NARS-17"

# list_max_disappeared = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160] # Maximum number of frames a track can be lost before new points will be forces into a new track.
# list_running_mean_threshold = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160] # Maximum number of frames for calculating the running mean of the position of an object If there are less than this number of frames currently in the track, a mean over what is in the track will be used..
# list_max_distance = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000] # If set to 0, this parameter will be ignored. If not zero, points that have a distance to tracked objects higher than this parameter will be forced into new tracks.

# #list_max_disappeared = [100] # Maximum number of frames a track can be lost before new points will be forces into a new track.
# #list_running_mean_threshold = [5] # Maximum number of frames for calculating the running mean of the position of an object If there are less than this number of frames currently in the track, a mean over what is in the track will be used..
# #list_max_distance = [400] # If set to 0, this parameter will be ignored. If not zero, points that have a distance to tracked objects higher than this parameter will be forced into new tracks.


# list_of_parameters = [(x,y,z) for x in list_max_disappeared for y in list_running_mean_threshold for z in list_max_distance] # A list of all combinations of the above parameters.

# ### PATH TO DETECTIONS ####
# #detections = pd.read_csv(r'../Dummy_fortracking2.csv')

# detections = pd.read_csv(r"U:\BITCue\Projekter\TrackingFlowers\data\annotations\2021_12_30_NorwayAnnotations_NARS-17_IndividualAnnotations_FRCNN_Metrics.csv")
# detections['frame'] = detections['filename'].str.extract('(\d{6})')
# detections['x_c'] = (detections['x_min'] + detections['x_max']) / 2
# detections['y_c'] = (detections['y_min'] + detections['y_max']) / 2
# detections['frame'] = detections['frame'].astype('int')

# frames = list(set(detections['frame'].tolist()))
# frames = sorted([int(i) for i in frames])

# verbose = False # Set to True if you want tracking process printed to screen and False if not


# ## RUN ###

# for i in list_of_parameters:
#     starttime = time.time()
#     resultsFilename = f'../testResults/_parameterTest_NARS-17_3/{prefix_results_filename}_maxDisap_{i[0]}_runMean_{i[1]}_maxDist_{i[2]}.csv'    
    
#     t = tracker(i[0], i[2], i[1], resultsFilename, frames, detections, verbose)
    
#     for f in frames:
#         t.track(f)
#     endtime = time.time()
#     print(f'Tracking done. That took {round(endtime-starttime, 3)} seconds. That is {round((endtime-starttime)/len(frames), 3)} seconds per frame.')
#     t.write_tracks_file()
#     tracks = pd.read_csv(resultsFilename)
#     print(f'maxDis: {i[0]}, runMean: {i[1]} - Number of tracks found: {len(tracks.objectID.unique())}')

# =============================================================================

# ===================== Evaluate tracking accuracy ====


#Get the ground truth annotations on the format [filename, x_min, y_min, x_max, y_max, id_gt]
# gt = impdata("NYAA-04")
# dt = r'U:\BITCue\Projekter\TrackingFlowers\testResults\_parameterTest_NYAA-04_3\parameterTest_NYAA-04_maxDisap_10_runMean_10_maxDist_300.csv'
# results_filename = "../testResults/tempNARS04.csv"

# e = evaluator(dt, gt, results_filename, verbose = True)
# e.run()


# # ===================== Filter with DBSCANSieve ====
# eps_distance = 350

# d = DBSCANsieve(dt, eps_distance = eps_distance, min_sample_polygons = 1)
# filteredTracks = d.run()


# #results_filename_tracked = os.path.splitext(dt)[0] + f'NARS04_Filtered_EpsDist_{eps_distance}.csv'
# results_filename_tracked = "../testResults/tempNARS04.csv"

# filteredTracks.to_csv(results_filename_tracked)


# ===================== Evaluate tracking accuracy of remaining tracks ====


# # dtTracked = pd.readresults_filename_tracked
# gtpd = pd.read_csv(gt)
# gtSub = gtpd.merge(filteredTracks, on=['filename','x_min', 'x_max', 'y_min', 'y_max'], how='inner', indicator=True)
# #gt_sub = os.path.splitext(gt)[0] + f'_Filtered_EpsDist_{eps_distance}.csv'
# #filteredTracks.to_csv(results_filename_tracked)

# results_filename = "../testResults/temp2.csv"

# e = evaluator(results_filename_tracked, gtSub, results_filename)
# e.run()




# ===================== Find a good value for eps ====

#
##
###
####

# Find a good value for eps

epslist = [350]
results_filename = '../testResults/temp_epstest.csv'

temppath = '../testResults/temp_epsExperiment_maxDisap_10_runMean_10_maxDist_300.csv'
gt_temppath = '../testResults/gttemp.csv'

for eps in epslist:
    mmsum = 0
    flowersum = 0
    # Return also the number of flowers/object returned after filtering. Find good combo between this and mismatches.

    
    dt = r'U:\BITCue\Projekter\TrackingFlowers\testResults\_parameterTest_NARS-17_3\parameterTest_NARS-17_maxDisap_10_runMean_10_maxDist_300.csv'
    gt = pd.read_csv(impdata("NARS-17"))
    print(gt)    
    d = DBSCANsieve(dt, eps_distance = eps, min_sample_polygons = 1)
    filteredTracks = d.run()
    filteredTracks.to_csv(temppath)    
    
    gtSub = gt.merge(filteredTracks, on=['filename','x_min', 'x_max', 'y_min', 'y_max'], how='inner', indicator=True)
    print(gtSub)
    e = evaluator(temppath, gt, results_filename, verbose = False)
    mm = e.run()   
    mmsum += mm
    print(f'NARS-17 = {mm}')
    
    

#     # dt = r'U:\BITCue\Projekter\TrackingFlowers\testResults\_parameterTest_THUL-01_3\parameterTest_THUL-01_maxDisap_10_runMean_10_maxDist_300.csv'
#     # gt = pd.read_csv(impdata("THUL-01"))
        
#     # d = DBSCANsieve(dt, eps_distance = eps, min_sample_polygons = 1)
#     # filteredTracks = d.run()
#     # filteredTracks.to_csv(temppath)    
    
#     # gtSub = gt.merge(filteredTracks, on=['filename','x_min', 'x_max', 'y_min', 'y_max'], how='inner', indicator=True)

#     # e = evaluator(temppath, gt, results_filename, verbose = False)
#     # mm = e.run()   
#     # mmsum += mm
#     # print(f'THUL-01 = {mm}')
         
    
#     ### RUN FILTERING ###
#     dt = r'U:\BITCue\Projekter\TrackingFlowers\testResults\_parameterTest_NARS-13_3\parameterTest_NARS-13_maxDisap_10_runMean_10_maxDist_300.csv'
#     gt = pd.read_csv(impdata("NARS-13"))
        
#     d = DBSCANsieve(dt, eps_distance = eps, min_sample_polygons = 1)
#     filteredTracks = d.run()
#     filteredTracks.to_csv(temppath)    
    
#     gtSub = gt.merge(filteredTracks, on=['filename','x_min', 'x_max', 'y_min', 'y_max'], how='inner', indicator=True)
#     gtSub.to_csv(gt_temppath)
    
#     e = evaluator(temppath, gt_temppath, results_filename, verbose = True)
#     mm = e.run()   
#     mmsum += mm
    
#     tracksKept = len(filteredTracks['objectID'].unique())
#     flowersum += tracksKept
#     print(f'NARS-13 = {mm} mismatches with {tracksKept} tracks kept')
    




#     ### RUN FILTERING ###
#     dt = r'U:\BITCue\Projekter\TrackingFlowers\testResults\_parameterTest_NARS-04_3\parameterTest_NARS-04_maxDisap_10_runMean_10_maxDist_300.csv'
#     gt = pd.read_csv(impdata("NARS-04"))
        
#     d = DBSCANsieve(dt, eps_distance = eps, min_sample_polygons = 1)
#     filteredTracks = d.run()
#     filteredTracks.to_csv(temppath)   
    
#     gtSub = gt.merge(filteredTracks, on=['filename','x_min', 'x_max', 'y_min', 'y_max'], how='inner', indicator=True)
#     gtSub.to_csv(gt_temppath)
    
#     e = evaluator(temppath, gt_temppath, results_filename, verbose = True)
#     mm = e.run()   
#     mmsum += mm
    
#     tracksKept = len(filteredTracks['objectID'].unique())
#     flowersum += tracksKept
#     print(f'NARS-04 = {mm} mismatches with {tracksKept} tracks kept')

    
    
    
    
#     ### RUN FILTERING ###
#     dt = r'U:\BITCue\Projekter\TrackingFlowers\testResults\_parameterTest_NYAA-04_3\parameterTest_NYAA-04_maxDisap_10_runMean_10_maxDist_300.csv'
#     gt = pd.read_csv(impdata("NYAA-04"))
    
#     d = DBSCANsieve(dt, eps_distance = eps, min_sample_polygons = 1)
#     filteredTracks = d.run()
#     filteredTracks.to_csv(temppath) 
    
#     gtSub = gt.merge(filteredTracks, on=['filename','x_min', 'x_max', 'y_min', 'y_max'], how='inner', indicator=True)
#     gtSub.to_csv(gt_temppath)

#     e = evaluator(temppath, gt_temppath, results_filename, verbose = True)
#     mm = e.run()   
#     mmsum += mm
    
#     tracksKept = len(filteredTracks['objectID'].unique())
#     flowersum += tracksKept
#     print(f'NYAA-04 = {mm} mismatches with {tracksKept} tracks kept')


#     print(f'"""\neps = {eps} gives {mmsum} mismatches with {flowersum} tracks kept \n"""')




# ===================== Filter with DBSCANSieve ====
# eps_distance = 350

# d = DBSCANsieve(dt, eps_distance = eps_distance, min_sample_polygons = 1)
# filteredTracks = d.run()


# results_filename_tracked = os.path.splitext(dt)[0] + f'_Filtered_EpsDist_{eps_distance}.csv'
# filteredTracks.to_csv(results_filename_tracked)


# ===================== Evaluate tracking accuracy of remaining tracks ====


# # dtTracked = pd.readresults_filename_tracked
# gtpd = pd.read_csv(gt)
# gtSub = gtpd.merge(filteredTracks, on=['filename','x_min', 'x_max', 'y_min', 'y_max'], how='inner', indicator=True)
# #gt_sub = os.path.splitext(gt)[0] + f'_Filtered_EpsDist_{eps_distance}.csv'
# #filteredTracks.to_csv(results_filename_tracked)

# results_filename = "../testResults/temp2.csv"

# e = evaluator(results_filename_tracked, gtSub, results_filename)
# e.run()




####
###
##
#









# ===================== Additional commands ====
## Run evaluator on several files

# path = r'../testResults\tempTHUL01'
# files = [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.csv')]
# print(files)

# results_filename = "../testResults/parameterTest_3_THUL-01_temp.csv"


# write_header(results_filename)

# for f in files:
#     e = evaluator(f, gt, results_filename)
#     e.run()


