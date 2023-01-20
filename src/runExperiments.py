# -*- coding: utf-8 -*-

# Import local packages
from track import tracker
from filter import filterer
from evaluate import evaluator

# Import global packages
import pandas as pd
import time
import os
import re

br = '\n'


###################

## Function for importing data
def impdata(camID):
    if camID == "NARS-04":
        gt = r".\data\annotations\2020_05_17_NorwayAnnotations_NARS-04_IndividualAnnotations_FRCNN_Metrics.csv"
    if camID == "NARS-13":
        gt = r".\data\annotations\2020_04_30_NorwayAnnotations_NARS-13_IndividualAnnotations_FRCNN_Metrics.csv"
    if camID == "THUL-01":
        gt = r".\data\annotations\2020_05_15_NorwayAnnotations_THUL-01_IndividualAnnotations_FRCNN_Metrics.csv"
    if camID == "NYAA-04":
        gt = r".\data\annotations\2021_12_13_NorwayAnnotations_NYAA-04_IndividualAnnotations_FRCNN_Metrics.csv"
    if camID == "NARS-17":
        gt = r".\data\annotations\2021_12_30_NorwayAnnotations_NARS-17_IndividualAnnotations_FRCNN_Metrics.csv"
    if camID == "debug":
        gt = r".\data\annotations\debugGT.csv"
    return gt
        




# ===================== Run tracking on several combinations of parameters (parameter test in manuscript) ====

### SETTINGS ###

# prefix_results_filename = "parameterTest_THUL-01"

# list_max_disappeared = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160] # Maximum number of frames a track can be lost before new points will be forces into a new track.
# list_running_mean_threshold = [1,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160] # Maximum number of frames for calculating the running mean of the position of an object If there are less than this number of frames currently in the track, a mean over what is in the track will be used..
# list_max_distance = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000] # If set to 0, this parameter will be ignored. If not zero, points that have a distance to tracked objects higher than this parameter will be forced into new tracks.

# #list_max_disappeared = [100] 
# #list_running_mean_threshold = [5] 
# #list_max_distance = [400]


# list_of_parameters = [(x,y,z) for x in list_max_disappeared for y in list_running_mean_threshold for z in list_max_distance] # A list of all combinations of the above parameters.

# ### PATH TO DETECTIONS ####

# detections = pd.read_csv(r"./data\annotations\2020_05_15_NorwayAnnotations_THUL-01_IndividualAnnotations_FRCNN_Metrics.csv")
# detections['frame'] = detections['filename'].str.extract('(\d{6})')
# detections['x_c'] = (detections['x_min'] + detections['x_max']) / 2
# detections['y_c'] = (detections['y_min'] + detections['y_max']) / 2
# detections['frame'] = detections['frame'].astype('int')

# frames = list(set(detections['frame'].tolist()))
# frames = sorted([int(i) for i in frames])

# verbose = False # Set to True if you want tracking process printed to screen and False if not


# # RUN ###
# #(self, max_gap, max_distance, running_mean_threshold, results_filename, detections, verbose)

# for i in list_of_parameters:
#     starttime = time.time()
#     resultsFilename = f'U:/BITCue/Projekter/TrackingFlowers/delete_runExperimentsTest_parameterTest_THUL-01_3_{prefix_results_filename}_maxDisap_{i[0]}_runMean_{i[1]}_maxDist_{i[2]}.csv'    
    
#     t = tracker(i[0], i[2], i[1], resultsFilename, detections, verbose)
    
#     t.track()
#     endtime = time.time()
#     print(f'Tracking done. That took {round(endtime-starttime, 3)} seconds. That is {round((endtime-starttime)/len(frames), 3)} seconds per frame.')
#     t.write_tracks_file()
#     tracks = pd.read_csv(resultsFilename)
#     print(f'maxDis: {i[0]}, runMean: {i[1]} - Number of tracks found: {len(tracks.objectID.unique())}')

# =============================================================================




# ===================== Run evaluator on all files for the parameter test ====
# path = r"U:\BITCue\Projekter\TrackingFlowers\testResults\trackingParameterTests\_parameterTest_THUL-01"
# files = [os.path.join(path,i) for i in os.listdir(path)]

# gt = pd.read_csv(r"U:\BITCue\Projekter\TrackingFlowers\data\annotations\2020_05_15_NorwayAnnotations_THUL-01_IndividualAnnotations_FRCNN_Metrics.csv")
# gt['frame'] = gt.filename.str.extract('(\d{6})').astype(int)

# # Bounding boxes are given as coordinates for top left, bottom right corner. We need center x and y.
# gt['x_c'] = (gt['x_min'] + gt['x_max']) / 2
# gt['y_c'] = (gt['y_min'] + gt['y_max']) / 2
# gt['object'] = gt['id_gt']
# gt['object'] = gt.apply(lambda x: int(''.join(filter(str.isdigit, x['object']))), axis=1)

# i = 0

# overviewFile = r'U:\BITCue\Projekter\TrackingFlowers/deleteEvaluate_runExperimentsTest.csv'


# with open(overviewFile, 'a') as resultFile: # Write the header of the output file
#     header = f'maxDisap,maxDist,runMean,num_tracks,num_switches {br}'
#     resultFile.write(header)


# for f in files:
#     basename = os.path.basename(f)
#     dt = pd.read_csv(f)
#     dt.rename({'objectID': 'id_tr'}, axis=1, inplace=True)
#     gt['id_gt_int'] = gt.apply(lambda x: int(''.join(filter(str.isdigit, x['id_gt']))), axis=1)
#     print("gt")
#     print(gt)
#     print("dt")
#     print(dt)
#     runMeanSearch = re.search('runMean_(.+?)_max', basename)
#     maxDistSearch = re.search('maxDist_(.+?).csv', basename)
#     maxDisapSearch = re.search('maxDisap_(.+?)_run', basename)


#     runMeanValue = runMeanSearch.group(1)
#     maxDistValue = maxDistSearch.group(1)
#     maxDisapValue = maxDisapSearch.group(1)

#     results_filename = f'U:/BITCue/Projekter/TrackingFlowers/delete_parameterTestEvaluation_maxgap_{maxDisapValue}_runmean_{runMeanValue}_maxdist_{maxDistValue}.csv'

#     e = evaluator(dt, gt, results_filename, verbose = True)
#     num_tracks, num_switches = e.run()
#     i += 1
#     print("Files processed: ", i)
#     with open(overviewFile, 'a') as resultFile:
#         resultFile.write(f'{maxDisapValue},{maxDistValue},{runMeanValue},{num_switches},{num_tracks}{br}')




# ===================== Find a good value for eps ====

#Find a good value for eps

epslist = [50,100,150,200,250,300,350,400,450,500] # [350]
#epslist = [150]
results_filename = r'U:\BITCue\Projekter\TrackingFlowers/deleteEpstest_runExperimentsTest.csv'

temppath = 'temp_epsExperiment_maxDisap_10_runMean_10_maxDist_300.csv'
gt_temppath = 'gttemp.csv'
i = 0


for eps in epslist:
    mmsum = 0
    flowersum = 0
    # Return also the number of flowers/object returned after filtering. Find good combo between this and mismatches.

    
    # ### NARS-13 ###
    # ### RUN FILTERING ###
    dt = r"U:\BITCue\Projekter\TrackingFlowers\testResults\trackingParameterTests\_parameterTest_NARS-13\parameterTest_NARS-13_maxDisap_10_runMean_10_maxDist_300.csv"
    gtSite = "NARS-13"
    gt = pd.read_csv(impdata(gtSite))
    f = list(set(gt['filename'].tolist())) # Make a list of image filenames
    f.sort(key=lambda x: int(''.join(filter(str.isdigit, x)))) # Sort the filenames based on extracted digits in the filename
    d = {k: v+1 for v, k in enumerate(f)} # Make a dictionary with index

    gt['frame'] = gt['filename'].map(d) # Create a frame column by mapping filename to dictionary

       
    d = filterer(dt, eps_distance = eps)
    filteredTracks = d.run()
    filteredTracks.to_csv(temppath)    
    
    gtSub = gt.merge(filteredTracks, on=['filename','x_min', 'x_max', 'y_min', 'y_max'], how='inner', indicator=True)
    gtSub.to_csv(gt_temppath)


    gt = pd.read_csv(gt_temppath)


    if gt.empty:
        mmsum += 0
        flowersum += 0
        print("All tracks removed by filtering.")
    else:
        dt = pd.read_csv(temppath)

        f = list(set(gt['filename'].tolist())) # Make a list of image filenames
        f.sort(key=lambda x: int(''.join(filter(str.isdigit, x)))) # Sort the filenames based on extracted digits in the filename
        d = {k: v+1 for v, k in enumerate(f)} # Make a dictionary with index

        gt['x_c'] = (gt['x_min'] + gt['x_max'])/2
        gt['y_c'] = (gt['y_min'] + gt['y_max'])/2
        gt['frame'] = gt['filename'].map(d) # Create a frame column by mapping filename to dictionary
        gt['id_gt_int'] = gt.apply(lambda x: int(''.join(filter(str.isdigit, x['id_gt']))), axis=1)

        dt.rename({'objectID': 'id_tr'}, axis=1, inplace=True)
        dt['frame'] = dt['filename'].map(d) # Create a frame column by mapping filename to dictionary 

        results_filename = gtSite + "_" + str(eps) + ".csv"

        e = evaluator(dt, gt, results_filename, verbose = False)
        num_tracks, num_switches = e.run()

        mmsum += num_switches

        
        tracksKept = len(filteredTracks['objectID'].unique())
        flowersum += tracksKept
        print(f'{gtSite} = {num_switches} mismatches with {tracksKept} tracks kept')
    

   ### THUL-01 ###
    ### RUN FILTERING ###
    dt = r"U:\BITCue\Projekter\TrackingFlowers\testResults\trackingParameterTests\_parameterTest_THUL-01\parameterTest_THUL-01_maxDisap_10_runMean_10_maxDist_300.csv"
    gtSite = "THUL-01"
    gt = pd.read_csv(impdata(gtSite))
    f = list(set(gt['filename'].tolist())) # Make a list of image filenames
    f.sort(key=lambda x: int(''.join(filter(str.isdigit, x)))) # Sort the filenames based on extracted digits in the filename
    d = {k: v+1 for v, k in enumerate(f)} # Make a dictionary with index

    gt['frame'] = gt['filename'].map(d) # Create a frame column by mapping filename to dictionary

       
    d = filterer(dt, eps_distance = eps)
    filteredTracks = d.run()
    filteredTracks.to_csv(temppath)    
    
    gtSub = gt.merge(filteredTracks, on=['filename','x_min', 'x_max', 'y_min', 'y_max'], how='inner', indicator=True)
    gtSub.to_csv(gt_temppath)

    gt = pd.read_csv(gt_temppath)

    if gt.empty:
        mmsum += 0
        flowersum += 0
        print("All tracks removed by filtering.")
    else:
        dt = pd.read_csv(temppath)

        f = list(set(gt['filename'].tolist())) # Make a list of image filenames
        f.sort(key=lambda x: int(''.join(filter(str.isdigit, x)))) # Sort the filenames based on extracted digits in the filename
        d = {k: v+1 for v, k in enumerate(f)} # Make a dictionary with index

        gt['x_c'] = (gt['x_min'] + gt['x_max'])/2
        gt['y_c'] = (gt['y_min'] + gt['y_max'])/2
        gt['frame'] = gt['filename'].map(d) # Create a frame column by mapping filename to dictionary
        gt['id_gt_int'] = gt.apply(lambda x: int(''.join(filter(str.isdigit, x['id_gt']))), axis=1)

        dt.rename({'objectID': 'id_tr'}, axis=1, inplace=True)
        dt['frame'] = dt['filename'].map(d) # Create a frame column by mapping filename to dictionary 

        results_filename = gtSite + "_" + str(eps) + ".csv"

        e = evaluator(dt, gt, results_filename, verbose = False)
        num_tracks, num_switches = e.run()

        mmsum += num_switches

        tracksKept = len(filteredTracks['objectID'].unique())
        flowersum += tracksKept
        print(f'{gtSite} = {num_switches} mismatches with {tracksKept} tracks kept')

    
#     ### NYAA-04 ###
#     ### RUN FILTERING ###
    dt = r"U:\BITCue\Projekter\TrackingFlowers\testResults\trackingParameterTests\_parameterTest_NYAA-04\parameterTest_NYAA-04_maxDisap_10_runMean_10_maxDist_300.csv"
    gtSite = "NYAA-04"
    gt = pd.read_csv(impdata(gtSite))
    f = list(set(gt['filename'].tolist())) # Make a list of image filenames
    f.sort(key=lambda x: int(''.join(filter(str.isdigit, x)))) # Sort the filenames based on extracted digits in the filename
    d = {k: v+1 for v, k in enumerate(f)} # Make a dictionary with index

    gt['frame'] = gt['filename'].map(d) # Create a frame column by mapping filename to dictionary

       
    d = filterer(dt, eps_distance = eps)
    filteredTracks = d.run()
    filteredTracks.to_csv(temppath)    
    
    gtSub = gt.merge(filteredTracks, on=['filename','x_min', 'x_max', 'y_min', 'y_max'], how='inner', indicator=True)
    gtSub.to_csv(gt_temppath)


    gt = pd.read_csv(gt_temppath)

    if gt.empty:
        mmsum += 0
        flowersum += 0
        print("All tracks removed by filtering.")
    else:

        dt = pd.read_csv(temppath)

        f = list(set(gt['filename'].tolist())) # Make a list of image filenames
        f.sort(key=lambda x: int(''.join(filter(str.isdigit, x)))) # Sort the filenames based on extracted digits in the filename
        d = {k: v+1 for v, k in enumerate(f)} # Make a dictionary with index

        gt['x_c'] = (gt['x_min'] + gt['x_max'])/2
        gt['y_c'] = (gt['y_min'] + gt['y_max'])/2
        gt['frame'] = gt['filename'].map(d) # Create a frame column by mapping filename to dictionary
        gt['id_gt_int'] = gt.apply(lambda x: int(''.join(filter(str.isdigit, x['id_gt']))), axis=1)

        dt.rename({'objectID': 'id_tr'}, axis=1, inplace=True)
        dt['frame'] = dt['filename'].map(d) # Create a frame column by mapping filename to dictionary 

        results_filename = gtSite + "_" + str(eps) + ".csv"

        e = evaluator(dt, gt, results_filename, verbose = False)
        num_tracks, num_switches = e.run()

        mmsum += num_switches
        
        tracksKept = len(filteredTracks['objectID'].unique())
        flowersum += tracksKept
        print(f'{gtSite} = {num_switches} mismatches with {tracksKept} tracks kept')


#     ### NARS-04 ###
#     ### RUN FILTERING ###
    dt = r"U:\BITCue\Projekter\TrackingFlowers\testResults\trackingParameterTests\_parameterTest_NARS-04\parameterTest_NARS-04_maxDisap_10_runMean_10_maxDist_300.csv"
    gtSite = "NARS-04"
    gt = pd.read_csv(impdata(gtSite))
    f = list(set(gt['filename'].tolist())) # Make a list of image filenames
    f.sort(key=lambda x: int(''.join(filter(str.isdigit, x)))) # Sort the filenames based on extracted digits in the filename
    d = {k: v+1 for v, k in enumerate(f)} # Make a dictionary with index

    gt['frame'] = gt['filename'].map(d) # Create a frame column by mapping filename to dictionary

       
    d = filterer(dt, eps_distance = eps)
    filteredTracks = d.run()
    filteredTracks.to_csv(temppath)    
    
    gtSub = gt.merge(filteredTracks, on=['filename','x_min', 'x_max', 'y_min', 'y_max'], how='inner', indicator=True)
    gtSub.to_csv(gt_temppath)


    gt = pd.read_csv(gt_temppath)

    if gt.empty:
        mmsum += 0
        flowersum += 0
        print("All tracks removed by filtering.")
    else:
        dt = pd.read_csv(temppath)

        f = list(set(gt['filename'].tolist())) # Make a list of image filenames
        f.sort(key=lambda x: int(''.join(filter(str.isdigit, x)))) # Sort the filenames based on extracted digits in the filename
        d = {k: v+1 for v, k in enumerate(f)} # Make a dictionary with index

        gt['x_c'] = (gt['x_min'] + gt['x_max'])/2
        gt['y_c'] = (gt['y_min'] + gt['y_max'])/2
        gt['frame'] = gt['filename'].map(d) # Create a frame column by mapping filename to dictionary
        gt['id_gt_int'] = gt.apply(lambda x: int(''.join(filter(str.isdigit, x['id_gt']))), axis=1)

        dt.rename({'objectID': 'id_tr'}, axis=1, inplace=True)
        dt['frame'] = dt['filename'].map(d) # Create a frame column by mapping filename to dictionary 

        results_filename = gtSite + "_" + str(eps) + ".csv"

        e = evaluator(dt, gt, results_filename, verbose = False)
        num_tracks, num_switches = e.run()

        mmsum += num_switches

        
        tracksKept = len(filteredTracks['objectID'].unique())
        flowersum += tracksKept
        print(f'{gtSite} = {num_switches} mismatches with {tracksKept} tracks kept')



        print(f'"""\neps = {eps} gives {mmsum} mismatches with {flowersum} tracks kept \n"""')    

    
    


"""
Eps Result:

eps = 50 gives 158 mismatches with 171 tracks kept

eps = 100 gives 103 mismatches with 153 tracks kept

eps = 150 gives 71 mismatches with 130 tracks kept

eps = 200 gives 47 mismatches with 106 tracks kept

eps = 250 gives 30 mismatches with 75 tracks kept

eps = 300 gives 9 mismatches with 51 tracks kept

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


