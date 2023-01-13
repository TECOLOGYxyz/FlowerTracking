# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 12:50:10 2021

@author: au309263
"""
import sys

sys.path.append("..")
import pandas as pd
from track import tracker

#from filtering import sieve
#from DBSCANFiltering import DBSCANsieve
#from distanceFiltering import distanceSieve
#from evaluate import evaluator
#import os
import time
import os
import pandas as pd
from scipy.spatial import distance as dist
import os
import re
import numpy as np

import motmetrics as mm
br = '\n'
###################

# ===================== Run evaluator on all files for the parameter test ====

#max_disappeared, max_distance, running_mean_threshold, results_filename, frames, detections, verbose
simulated = pd.read_csv(r"U:\BITCue\Projekter\TrackingFlowers\data\simulation\maxgapExample.csv")
simulated['x_min'] = simulated["x_c"] - 1
simulated['x_max'] = simulated["x_c"] + 1
simulated['y_min'] = simulated["y_c"] - 1
simulated['y_max'] = simulated["y_c"] + 1
simulated['frame'] = simulated['frame'].astype('int')
simulated['filename'] = "simulated_test1"

t = tracker(4, 200, 1, r"U:\BITCue\Projekter\TrackingFlowers\delete.csv", simulated, True) # Instantiate the class instance and pass in the threshold for max_disappeared and the list of frames.
starttime = time.time()
t.track()
endtime = time.time()
#print(f'Tracking done. That took {round(endtime-starttime, 3)} seconds. That is {round((endtime-starttime)/len(frames), 3)} seconds per frame.')
#t.write_tracks_file()


def write_header(results_filename):
    with open(results_filename, 'a') as resultFile: # Write the header of the output file
        header = f'maxDisap,maxDist,runMean,num_frames,num_detections,num_objects,num_predictions,num_unique_objects,num_tracks,num_matches,num_switches,num_misses,num_false_positives,precision,recall,mota,motp,mostly_tracked,partially_tracked,mostly_lost{br}'
        resultFile.write(header)


#results_filename = r'U:\BITCue\Projekter\TrackingFlowers\testResults/' + "framerateExample_100th" + '_0_0_1.csv'
results_filename = r'U:\BITCue\Projekter\TrackingFlowers/delete_run.csv'
write_header(results_filename)

acc = mm.MOTAccumulator(auto_id=True)# Create an accumulator that will be updated during each frame

sort = pd.read_csv(r"U:\BITCue\Projekter\TrackingFlowers/delete.csv")

frames = list(set(simulated['frame'].to_list()))

for fr in frames:
    gtBoxes = simulated[simulated['frame'] == fr]#.copy(deep=True)
    sortBoxes = sort[sort['frame'] == fr]
    
    gtCentroids = []
    sortCentroids = []
    
    for ind, r in gtBoxes.iterrows():
        c = [r['x_c'], r['y_c']]
        gtCentroids.append(c)
    
    for ind, r in sortBoxes.iterrows():
        c = [r['x_c'], r['y_c']]
        sortCentroids.append(c)   
        
    
    gtIDs = gtBoxes['object'].tolist()
    sortIDs = sortBoxes['objectID'].tolist()
    D = dist.cdist(gtCentroids, sortCentroids)
    D[D>0]=np.nan # Since we work on tracked ground truth boxes and not detections, we'll set NaN on distance above zero to enforce that only identical boxes are associated. 
    #print(D)
    
    acc.update(gtIDs, sortIDs, D) # Append frame data to accumulator

print(sort)
num_tracks = len(set(sort['objectID']))    
mh = mm.metrics.create()
summary = mh.compute(acc, metrics=['num_frames','num_detections', 'num_objects', 'num_predictions', 'num_unique_objects', 'num_matches','num_switches', 'num_misses', 'num_false_positives', 'precision', 'recall', 'mota', 'motp', 'mostly_tracked', 'partially_tracked', 'mostly_lost'], name='acc')
#print(f'Site: {s}. GT: {impdata(s)}. SORT: {fi}')
#print(summary['num_frames'].values[0])


num_frames = summary['num_frames'].values[0]
num_detections = summary['num_detections'].values[0]
num_objects = summary['num_objects'].values[0]
num_predictions = summary['num_predictions'].values[0]
num_unique_objects = summary['num_unique_objects'].values[0]
num_matches = summary['num_matches'].values[0]
num_switches = summary['num_switches'].values[0]
num_misses = summary['num_misses'].values[0]
num_false_positives = summary['num_false_positives'].values[0]
precision = summary['precision'].values[0]
recall = summary['recall'].values[0]
mota =  summary['mota'].values[0]
motp =  summary['motp'].values[0]
mostly_tracked = summary['mostly_tracked'].values[0]
partially_tracked = summary['partially_tracked'].values[0]
mostly_lost = summary['mostly_lost'].values[0]

print("Number of mismatches: ", num_switches)
print("MOTA: ", mota)
print("Number of tracks: ", num_tracks)
#write_results_file(results_filename, maxDisap, maxDist, runMean, num_frames, num_detections, num_objects, num_predictions, num_unique_objects, num_tracks, num_matches, num_switches, num_misses, num_false_positives, precision, recall, mota, motp, mostly_tracked, partially_tracked, mostly_lost)        
#del acc


# br = '\n'

# def write_header(results_filename):
#     with open(results_filename, 'a') as resultFile: # Write the header of the output file
#         header = f'maxDisap,maxDist,runMean,num_frames,num_detections,num_objects,num_predictions,num_unique_objects,num_tracks,num_matches,num_switches,num_misses,num_false_positives,precision,recall,mota,motp,mostly_tracked,partially_tracked,mostly_lost{br}'
#         resultFile.write(header)

# def write_results_file(results_filename,maxDisap,maxDist,runMean,num_frames,num_detections,num_objects, num_predictions,num_unique_objects,num_tracks,num_matches,num_switches,num_misses,num_false_positives,precision,recall,mota,motp,mostly_tracked,partially_tracked,mostly_lost):
#     with open(results_filename, 'a') as resultFile:
#         resultFile.write(f'{maxDisap}, {maxDist}, {runMean}, {num_frames},{num_detections},{num_objects},{num_predictions},{num_unique_objects},{num_tracks},{num_matches},{num_switches},{num_misses},{num_false_positives},{precision},{recall},{mota},{motp},{mostly_tracked},{partially_tracked},{mostly_lost}{br}')



# def prepGT(gt, d):
#     gt['x_c'] = (gt['x_min'] + gt['x_max'])/2
#     gt['x_c'] = gt['x_c'].round(0).astype(int)
    
#     gt['y_c'] = (gt['y_min'] + gt['y_max'])/2
#     gt['y_c'] = gt['y_c'].round(0).astype(int)

#     gt['frame'] = gt['filename'].map(d) # Create a frame column by mapping filename to dictionary
    
#     gt['id_gt_int'] = gt.apply(lambda x: int(''.join(filter(str.isdigit, x['id_gt']))), axis=1)
    
#     return gt


# def prepSORT(sort, d):
 
#     #sort.drop([6, 7, 8, 9], axis=1, inplace = True)
#     #print(sort)
#     # Make sure coordinates are right! sort.rename({0: 'frame', 1: 'id_tr', 2: 'x_min', 3: 'x_max', 4: 'y_min', 5: 'y_max', 'objectID': 'id_tr'}, axis=1, inplace=True)
#     sort.rename({'objectID': 'id_tr'}, axis=1, inplace=True)
#     #print(sort)
#     sort['frame'] = sort['filename'].map(d) # Create a frame column by mapping filename to dictionary
    
#     sort['x_c'] = (sort['x_min'] + sort['x_max'])/2
#     sort['x_c'] = sort['x_c'].round(0).astype(int)
    
#     sort['y_c'] = (sort['y_min'] + sort['y_max'])/2
#     sort['y_c'] = sort['y_c'].round(0).astype(int)  
    
#     return sort


# def MOTMetrics(dt, gt,  site):
#     #path = r'../testResults\MMFix/_parameterTest_' + site + '_3'
#     #files = [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.csv')]
#     files = [dt]
#     gt = pd.read_csv(gt) #impdata(site))



#     f = list(set(gt['filename'].tolist())) # Make a list of image filenames
#     f.sort(key=lambda x: int(''.join(filter(str.isdigit, x)))) # Sort the filenames based on extracted digits in the filename
#     d = {k: v+1 for v, k in enumerate(f)} # Make a dictionary with index
    
#     gt = prepGT(gt, d)

    
#     results_filename = r'U:\BITCue\Projekter\TrackingFlowers\testResults/' + site + '_Simulation_20221128.csv'
#     write_header(results_filename)
    
#     frames = list(set(gt['frame'].to_list()))

#     for fi in files:
        
#         runMeanSearch = re.search('runMean_(.+?)_max', fi)
#         maxDistSearch = re.search('maxDist_(.+?).csv', fi)
#         maxDisapSearch = re.search('maxDisap_(.+?)_run', fi)
        
#         if runMeanSearch:
#             runMean = runMeanSearch.group(1)
    
#         if maxDistSearch:
#             maxDist = maxDistSearch.group(1)
                
#         if maxDisapSearch:
#             maxDisap = maxDisapSearch.group(1)
            
        
#         #print("Setting up accumulator")    
#         acc = mm.MOTAccumulator(auto_id=True)# Create an accumulator that will be updated during each frame
        
        
#         sort = pd.read_csv(fi)
#         sort = prepSORT(sort, d)

#         #num_tracks = len(set(sort['id_tr']))
#         #print("Number of tracks: ", num_tracks)

#         for fr in frames:
#             gtBoxes = gt[gt['frame'] == fr]#.copy(deep=True)
#             sortBoxes = sort[sort['frame'] == fr]
            
#             gtCentroids = []
#             sortCentroids = []
            
#             for ind, r in gtBoxes.iterrows():
#                 c = [r['x_c'], r['y_c']]
#                 gtCentroids.append(c)
            
#             for ind, r in sortBoxes.iterrows():
#                 c = [r['x_c'], r['y_c']]
#                 sortCentroids.append(c)   
                
         
#             gtIDs = gtBoxes['id_gt_int'].tolist()
#             sortIDs = sortBoxes['id_tr'].tolist()
#             D = dist.cdist(gtCentroids, sortCentroids)
#             D[D>0]=np.nan # Since we work on tracked ground truth boxes and not detections, we'll set NaN on distance above zero to enforce that only identical boxes are associated. 
#             #print(D)
         
#             acc.update(gtIDs, sortIDs, D) # Append frame data to accumulator
            
#         mh = mm.metrics.create()
#         summary = mh.compute(acc, metrics=['num_frames','num_detections', 'num_objects', 'num_predictions', 'num_unique_objects', 'num_matches','num_switches', 'num_misses', 'num_false_positives', 'precision', 'recall', 'mota', 'motp', 'mostly_tracked', 'partially_tracked', 'mostly_lost'], name='acc')
#         #print(f'Site: {s}. GT: {impdata(s)}. SORT: {fi}')
#         #print(summary['num_frames'].values[0])


#         num_frames = summary['num_frames'].values[0]
#         num_detections = summary['num_detections'].values[0]
#         num_objects = summary['num_objects'].values[0]
#         num_predictions = summary['num_predictions'].values[0]
#         num_unique_objects = summary['num_unique_objects'].values[0]
#         num_matches = summary['num_matches'].values[0]
#         num_switches = summary['num_switches'].values[0]
#         num_misses = summary['num_misses'].values[0]
#         num_false_positives = summary['num_false_positives'].values[0]
#         precision = summary['precision'].values[0]
#         recall = summary['recall'].values[0]
#         mota =  summary['mota'].values[0]
#         motp =  summary['motp'].values[0]
#         mostly_tracked = summary['mostly_tracked'].values[0]
#         partially_tracked = summary['partially_tracked'].values[0]
#         mostly_lost = summary['mostly_lost'].values[0]
        
#         #print("Number of mismatches: ", num_switches)
#        # print("MOTA: ", mota)
#         #write_results_file(results_filename, maxDisap, maxDist, runMean, num_frames, num_detections, num_objects, num_predictions, num_unique_objects, num_tracks, num_matches, num_switches, num_misses, num_false_positives, precision, recall, mota, motp, mostly_tracked, partially_tracked, mostly_lost)        
#     #del acc
#     return num_switches

#######





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

    
    
    
#     ### RUN FILTERING ###
#     dt = r'U:\BITCue\Projekter\TrackingFlowers\testResults\MMFix/_parameterTest_NYAA-04_3\parameterTest_NYAA-04_maxDisap_10_runMean_10_maxDist_300.csv'
#     gtSite = "NYAA-04"
#     gt = pd.read_csv(impdata(gtSite))
    
#     d = DBSCANsieve(dt, eps_distance = eps, min_sample_polygons = 1)
#     filteredTracks = d.run()
#     filteredTracks.to_csv(temppath) 
    
#     gtSub = gt.merge(filteredTracks, on=['filename','x_min', 'x_max', 'y_min', 'y_max'], how='inner', indicator=True)
#     gtSub.to_csv(gt_temppath)
    
#     mm3 = MOTMetrics(temppath, gt_temppath, gtSite) 
#     mmsum += mm3
    
#     tracksKept = len(filteredTracks['objectID'].unique())
#     flowersum += tracksKept
#     #print(f'NYAA-04 = {mm} mismatches with {tracksKept} tracks kept')


#     print(f'"""\neps = {eps} gives {mmsum} mismatches with {flowersum} tracks kept \n"""')    
    



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


