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


###################

### Function for importing data
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
    if camID == "debug":
        gt = r"U:\BITCue\Projekter\TrackingFlowers\data\annotations\debugGT.csv"
    return gt
        


##### EXAMPLE RUN #####
### First let's run the tracking algorithm on some simulated data:
# sims = pd.read_csv(r"./data/simulation/maxgapExample.csv")
# sims['filename'] = "simulation_run"

# sims['x_min'] = sims["x_c"] - 1
# sims['x_max'] = sims["x_c"] + 1
# sims['y_min'] = sims["y_c"] - 1
# sims['y_max'] = sims["y_c"] + 1

# # # We are ready to run tracking on the file
# t = tracker(0, 0, 1, r"U:\BITCue\Projekter\TrackingFlowers/maxgapExample_tracked_delete.csv", sims, True) # Instantiate the class instance and pass in the threshold for max_disappeared and the list of frames.
# t.track() # Run the tracking algorithm.


# #Get the ground truth annotations on the format [filename, x_min, y_min, x_max, y_max, id_gt]
gt = pd.read_csv(r"U:\BITCue\Projekter\TrackingFlowers\data\simulation\maxgapExample.csv")
dt = pd.read_csv(r"U:\BITCue\Projekter\TrackingFlowers/maxgapExample_tracked_delete.csv")

results_filename = "U:\BITCue\Projekter\TrackingFlowers\delete_evaluate.csv"

e = evaluator(dt, gt, results_filename, verbose = True)
e.run()





# ===================== Run evaluator on all files for the parameter test ====





# Read detection/annotation file
# detections = pd.read_csv(r"U:\BITCue\Projekter\TrackingFlowers\data\annotations\2020_05_15_NorwayAnnotations_THUL-01_IndividualAnnotations_FRCNN_Metrics.csv")

# # In this case, frame numbers are hidden in the filename. We'll extract them and  give them their own column.
# detections['frame'] = detections.filename.str.extract('(\d{6})').astype(int)

# # Bounding boxes are given as coordinates for top left, bottom right corner. We need center x and y.
# detections['x_c'] = (detections['x_min'] + detections['x_max']) / 2
# detections['y_c'] = (detections['y_min'] + detections['y_max']) / 2

# # We are ready to run tracking on the file
# t = tracker(4, 500, 5, r"U:\BITCue\Projekter\TrackingFlowers/codeTest_DELETE.csv", detections, True) # Instantiate the class instance and pass in the threshold for max_disappeared and the list of frames.
# t.track() # Run the tracking algorithm.


######
### Let's try it on some simulated data:
# sims = pd.read_csv(r"U:\BITCue\Projekter\TrackingFlowers\data\simulation\maxgapExample.csv")
# sims['filename'] = "codetest_delete"

# sims['x_min'] = sims["x_c"] - 1
# sims['x_max'] = sims["x_c"] + 1
# sims['y_min'] = sims["y_c"] - 1
# sims['y_max'] = sims["y_c"] + 1

# # We are ready to run tracking on the file
# t = tracker(0, 0, 1, r"U:\BITCue\Projekter\TrackingFlowers/maxgapExample_tracked_delete.csv", sims, True) # Instantiate the class instance and pass in the threshold for max_disappeared and the list of frames.
# t.track() # Run the tracking algorithm.


#Get the ground truth annotations on the format [filename, x_min, y_min, x_max, y_max, id_gt]

# gt = pd.read_csv(r"U:\BITCue\Projekter\TrackingFlowers\data\simulation\maxgapExample.csv")
# gt['x_min'] = gt["x_c"] - 1
# gt['x_max'] = gt["x_c"] + 1
# gt['y_min'] = gt["y_c"] - 1
# gt['y_max'] = gt["y_c"] + 1
# gt['frame'] = gt['frame'].astype('int')
# gt['filename'] = "simulated_test1"

# dt = pd.read_csv(r"U:\BITCue\Projekter\TrackingFlowers/maxgapExample_tracked_delete.csv")

# results_filename = "U:\BITCue\Projekter\TrackingFlowers\delete_evaluate.csv"

# e = evaluator(dt, gt, results_filename, verbose = True)
# e.run()



# ===================== Run tracking on several combinations of parameters ====

### SETTINGS ###

# prefix_results_filename = "parameterTest_THUL-01"

# list_max_disappeared = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160] # Maximum number of frames a track can be lost before new points will be forces into a new track.
# list_running_mean_threshold = [1,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160] # Maximum number of frames for calculating the running mean of the position of an object If there are less than this number of frames currently in the track, a mean over what is in the track will be used..
# list_max_distance = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000] # If set to 0, this parameter will be ignored. If not zero, points that have a distance to tracked objects higher than this parameter will be forced into new tracks.

# #list_max_disappeared = [100] # Maximum number of frames a track can be lost before new points will be forces into a new track.
# #list_running_mean_threshold = [5] # Maximum number of frames for calculating the running mean of the position of an object If there are less than this number of frames currently in the track, a mean over what is in the track will be used..
# #list_max_distance = [400] # If set to 0, this parameter will be ignored. If not zero, points that have a distance to tracked objects higher than this parameter will be forced into new tracks.


# list_of_parameters = [(x,y,z) for x in list_max_disappeared for y in list_running_mean_threshold for z in list_max_distance] # A list of all combinations of the above parameters.

# ### PATH TO DETECTIONS ####
# #detections = pd.read_csv(r'../Dummy_fortracking2.csv')

# detections = pd.read_csv(r"U:\BITCue\Projekter\TrackingFlowers\data\annotations\2020_05_15_NorwayAnnotations_THUL-01_IndividualAnnotations_FRCNN_Metrics.csv")
# detections['frame'] = detections['filename'].str.extract('(\d{6})')
# detections['x_c'] = (detections['x_min'] + detections['x_max']) / 2
# detections['y_c'] = (detections['y_min'] + detections['y_max']) / 2
# detections['frame'] = detections['frame'].astype('int')

# frames = list(set(detections['frame'].tolist()))
# frames = sorted([int(i) for i in frames])

# verbose = False # Set to True if you want tracking process printed to screen and False if not


## RUN ###

# for i in list_of_parameters:
#     starttime = time.time()
#     resultsFilename = f'../testResults/MMFix/_parameterTest_THUL-01_3/{prefix_results_filename}_maxDisap_{i[0]}_runMean_{i[1]}_maxDist_{i[2]}.csv'    
    
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





# ===================== Find a good value for eps ====

#
##
###
####

#Find a good value for eps

#epslist = [50,100,150,200,250,300,350,400,450,500] # [350]
# epslist = [350]
# results_filename = '../testResults/MMFix/temp_epstest.csv'

# temppath = '../testResults/MMFix/temp_epsExperiment_maxDisap_10_runMean_10_maxDist_300.csv'
# gt_temppath = '../testResults/gttemp.csv'

# for eps in epslist:
#     mmsum = 0
#     flowersum = 0
#     # Return also the number of flowers/object returned after filtering. Find good combo between this and mismatches.

    
    
#     ### RUN FILTERING ###
#     dt = r'U:\BITCue\Projekter\TrackingFlowers\testResults\MMFix/_parameterTest_NARS-13_3\parameterTest_NARS-13_maxDisap_10_runMean_10_maxDist_300.csv'
#     gtSite = "NARS-13"
#     gt = pd.read_csv(impdata(gtSite))
        
#     d = DBSCANsieve(dt, eps_distance = eps, min_sample_polygons = 1)
#     filteredTracks = d.run()
#     filteredTracks.to_csv(temppath)    
    
#     gtSub = gt.merge(filteredTracks, on=['filename','x_min', 'x_max', 'y_min', 'y_max'], how='inner', indicator=True)
#     gtSub.to_csv(gt_temppath)
    
#     mm1 = MOTMetrics(temppath, gt_temppath, gtSite) 
#     mmsum += mm1
#     #print(f'NARS-13 = {mm}')
    
#     tracksKept = len(filteredTracks['objectID'].unique())
#     flowersum += tracksKept
#     #print(f'NARS-13 = {mm} mismatches with {tracksKept} tracks kept')
    

   

#     ### RUN FILTERING ###
#     dt = r'U:\BITCue\Projekter\TrackingFlowers\testResults\MMFix/_parameterTest_NARS-04_3\parameterTest_NARS-04_maxDisap_10_runMean_10_maxDist_300.csv'
#     gtSite = "NARS-04"
#     gt = pd.read_csv(impdata(gtSite))
        
#     d = DBSCANsieve(dt, eps_distance = eps, min_sample_polygons = 1)
#     filteredTracks = d.run()
#     filteredTracks.to_csv(temppath)   
    
#     gtSub = gt.merge(filteredTracks, on=['filename','x_min', 'x_max', 'y_min', 'y_max'], how='inner', indicator=True)
#     gtSub.to_csv(gt_temppath)
    
#     mm2 = MOTMetrics(temppath, gt_temppath, gtSite)  
#     mmsum += mm2
    
#     tracksKept = len(filteredTracks['objectID'].unique())
#     flowersum += tracksKept
#     #print(f'NARS-04 = {mm} mismatches with {tracksKept} tracks kept')

    
    
    
    ### RUN FILTERING ###
    # dt = r'U:\BITCue\Projekter\TrackingFlowers\testResults\MMFix/_parameterTest_NYAA-04_3\parameterTest_NYAA-04_maxDisap_10_runMean_10_maxDist_300.csv'
    # gtSite = "NYAA-04"
    # gt = pd.read_csv(impdata(gtSite))
    
    # d = DBSCANsieve(dt, eps_distance = eps, min_sample_polygons = 1)
    # filteredTracks = d.run()
    # filteredTracks.to_csv(temppath) 
    
    # gtSub = gt.merge(filteredTracks, on=['filename','x_min', 'x_max', 'y_min', 'y_max'], how='inner', indicator=True)
    # gtSub.to_csv(gt_temppath)
    
    # mm3 = MOTMetrics(temppath, gt_temppath, gtSite) 
    # mmsum += mm3
    
    # tracksKept = len(filteredTracks['objectID'].unique())
    # flowersum += tracksKept
    # #print(f'NYAA-04 = {mm} mismatches with {tracksKept} tracks kept')


    # print(f'"""\neps = {eps} gives {mmsum} mismatches with {flowersum} tracks kept \n"""')    
    
    
    
# Result:
"""
eps = 50 gives 158 mismatches with 165 tracks kept 

eps = 100 gives 103 mismatches with 147 tracks kept 

eps = 150 gives 71 mismatches with 124 tracks kept 

eps = 200 gives 47 mismatches with 100 tracks kept 

eps = 250 gives 30 mismatches with 69 tracks kept 

eps = 300 gives 9 mismatches with 49 tracks kept 

eps = 350 gives 0 mismatches with 28 tracks kept 

eps = 400 gives 0 mismatches with 18 tracks kept 

eps = 450 gives 0 mismatches with 16 tracks kept 

eps = 500 gives 0 mismatches with 11 tracks kept
"""




































### SORT TEST TEMP ###


#Get the ground truth annotations on the format [filename, x_min, y_min, x_max, y_max, id_gt]
# gt = impdata("NYAA-04")
# dt = r'C:\Users\au309263\Documents\BITCue\Workspaces\Python\_Archive\Sort_py3\R_Evaluating_SORT\NYAA-04_SORTed_maxDisap_10_runMean_10_maxDist_300_frame.csv'
# results_filename = "../testResults/SORT_NYAA04.csv"

# e = evaluator(dt, gt, results_filename, verbose = True)
# e.run()


# gt = impdata("THUL-01")
# dt = r'U:\BITCue\Projekter\TrackingFlowers\sort\output\THUL01_SORT_Transfered__maxDisap_10_runMean_0_maxDist_0_NoZero_ForMOTA.csv'
# results_filename = r'U:\BITCue\Projekter\TrackingFlowers\sort\output\MOTA\NYAA-04_SORTed_Result.csv'

# e = evaluator(dt, gt, results_filename, verbose = True)
# e.run()







#### TEMP ###





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

#Find a good value for eps

# epslist = [350] # [350]
# results_filename = '../testResults/temp_epstest.csv'

# temppath = '../testResults/temp_epsExperiment_maxDisap_10_runMean_10_maxDist_300.csv'
# gt_temppath = '../testResults/gttemp.csv'

# for eps in epslist:
#     mmsum = 0
#     flowersum = 0
#     # Return also the number of flowers/object returned after filtering. Find good combo between this and mismatches.

    
#     dt = r'U:\BITCue\Projekter\TrackingFlowers\testResults\_parameterTest_NARS-17_3\parameterTest_NARS-17_maxDisap_10_runMean_10_maxDist_300.csv'
#     gt = pd.read_csv(impdata("NARS-17"))
#     print(gt)    
#     d = DBSCANsieve(dt, eps_distance = eps, min_sample_polygons = 1)
#     filteredTracks = d.run()
    # filteredTracks.to_csv(temppath)    
    
    # gtSub = gt.merge(filteredTracks, on=['filename','x_min', 'x_max', 'y_min', 'y_max'], how='inner', indicator=True)
    # print(gtSub)
    # e = evaluator(temppath, gt, results_filename, verbose = False)
    # mm = e.run()   
    # mmsum += mm
    # print(f'NARS-17 = {mm}')
    
    

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








# ===================== Filtering on distance ====

#
##
###
####

# Find a good value for eps

# epslist = [350] # [350]
# results_filename = '../testResults/temp_epstest.csv'

# temppath = '../testResults/temp_epsExperiment_maxDisap_10_runMean_10_maxDist_300.csv'
# gt_temppath = '../testResults/gttemp.csv'

# for eps in epslist:
#     mmsum = 0
#     flowersum = 0
#     # Return also the number of flowers/object returned after filtering. Find good combo between this and mismatches.

    
#     dt = r'U:\BITCue\Projekter\TrackingFlowers\testResults\_parameterTest_NARS-17_3\parameterTest_NARS-17_maxDisap_10_runMean_10_maxDist_300.csv'
#     gt = pd.read_csv(impdata("NARS-17"))
#     print(gt)    
#     d = distanceSieve(dt, eps_distance = eps, min_sample_polygons = 2)
#     filteredTracks = d.run()






# ===================== Find a good value for filtering distance ====

#
##
###
####

#Find a good value for eps

# epslist =  [50,100,150,200,250,300,350,400,450,500] # [350] #
# results_filename = '../testResults/temp_epstest.csv'

# temppath = '../testResults/temp_epsExperiment_maxDisap_10_runMean_10_maxDist_300.csv'
# gt_temppath = '../testResults/gttemp.csv'

# for eps in epslist:
#     mmsum = 0
#     flowersum = 0
#     # Return also the number of flowers/object returned after filtering. Find good combo between this and mismatches.

    
#     # dt = r'U:\BITCue\Projekter\TrackingFlowers\testResults\_parameterTest_NARS-17_3\parameterTest_NARS-17_maxDisap_10_runMean_10_maxDist_300.csv'
#     # gt = pd.read_csv(impdata("NARS-17"))
#     # print(gt)    
#     # d = distanceSieve(dt, eps_distance = eps, min_sample_polygons = 1)
#     # filteredTracks = d.run()
#     # filteredTracks.to_csv(temppath)    
    
#     # gtSub = gt.merge(filteredTracks, on=['filename','x_min', 'x_max', 'y_min', 'y_max'], how='inner', indicator=True)
#     # print(gtSub)
#     # e = evaluator(temppath, gt, results_filename, verbose = False)
#     # mm = e.run()   
#     # mmsum += mm
#     # print(f'NARS-17 = {mm}')
    
    

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
        
#     d = distanceSieve(dt, eps_distance = eps)
#     filteredTracks = d.run()
#     filteredTracks.to_csv(temppath)    
    
#     gtSub = gt.merge(filteredTracks, on=['filename','x_min', 'x_max', 'y_min', 'y_max'], how='inner', indicator=True)
#     gtSub.to_csv(gt_temppath)
    
#     e = evaluator(temppath, gt_temppath, results_filename, verbose = False)
#     mm = e.run()   
#     mmsum += mm
    
#     tracksKept = len(filteredTracks['objectID'].unique())
#     flowersum += tracksKept
#     print(f'NARS-13 = {mm} mismatches with {tracksKept} tracks kept')
    




#     ### RUN FILTERING ###
#     dt = r'U:\BITCue\Projekter\TrackingFlowers\testResults\_parameterTest_NARS-04_3\parameterTest_NARS-04_maxDisap_10_runMean_10_maxDist_300.csv'
#     gt = pd.read_csv(impdata("NARS-04"))
        
#     d = distanceSieve(dt, eps_distance = eps)
#     filteredTracks = d.run()
#     filteredTracks.to_csv(temppath)   
    
#     gtSub = gt.merge(filteredTracks, on=['filename','x_min', 'x_max', 'y_min', 'y_max'], how='inner', indicator=True)
#     gtSub.to_csv(gt_temppath)
    
#     e = evaluator(temppath, gt_temppath, results_filename, verbose = False)
#     mm = e.run()   
#     mmsum += mm
    
#     tracksKept = len(filteredTracks['objectID'].unique())
#     flowersum += tracksKept
#     print(f'NARS-04 = {mm} mismatches with {tracksKept} tracks kept')

    
    
    
    
#     ### RUN FILTERING ###
#     dt = r'U:\BITCue\Projekter\TrackingFlowers\testResults\_parameterTest_NYAA-04_3\parameterTest_NYAA-04_maxDisap_10_runMean_10_maxDist_300.csv'
#     gt = pd.read_csv(impdata("NYAA-04"))
    
#     d = distanceSieve(dt, eps_distance = eps)
#     filteredTracks = d.run()
#     filteredTracks.to_csv(temppath) 
    
#     gtSub = gt.merge(filteredTracks, on=['filename','x_min', 'x_max', 'y_min', 'y_max'], how='inner', indicator=True)
#     gtSub.to_csv(gt_temppath)

#     e = evaluator(temppath, gt_temppath, results_filename, verbose = False)
#     mm = e.run()   
#     mmsum += mm
    
#     tracksKept = len(filteredTracks['objectID'].unique())
#     flowersum += tracksKept
#     print(f'NYAA-04 = {mm} mismatches with {tracksKept} tracks kept')


#     print(f'"""\neps = {eps} gives {mmsum} mismatches with {flowersum} tracks kept \n"""')





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


