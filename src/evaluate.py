import motmetrics as mm
import pandas as pd
import re
from scipy.spatial import distance as dist
import numpy as np

br = '\n'


class evaluator():
    def __init__(self, dt, gt, results_filename, verbose = True):
        self.dt = dt #pd.read_csv(dt)
        self.gt = gt #pd.read_csv(gt)
        self.results_filename = results_filename

        self.verbose = verbose

        print("Detections", br)
        print(self.dt, br)

        print("Ground truth", br)
        print(self.gt, br)


    def write_header(self):
        with open(self.results_filename, 'a') as resultFile: # Write the header of the output file
            header = f'num_frames,num_detections,num_objects,num_predictions,num_unique_objects,num_tracks,num_matches,num_switches,num_misses,num_false_positives,precision,recall,mota,motp,mostly_tracked,partially_tracked,mostly_lost{br}'
            resultFile.write(header)

    def write_results_file(self, num_frames, num_detections, num_objects, num_predictions, num_unique_objects, num_tracks, num_matches, num_switches, num_misses, num_false_positives, precision, recall, mota, motp, mostly_tracked, partially_tracked, mostly_lost):
        with open(self.results_filename, 'a') as resultFile:
            resultFile.write(f'{num_frames},{num_detections},{num_objects},{num_predictions},{num_unique_objects},{num_tracks},{num_matches},{num_switches},{num_misses},{num_false_positives},{precision},{recall},{mota},{motp},{mostly_tracked},{partially_tracked},{mostly_lost}{br}')


    def run(self):
        self.write_header()
        acc = mm.MOTAccumulator(auto_id=True)# Create an accumulator that will be updated during each frame

        frames = list(set(self.gt['frame'].to_list()))

        for fr in frames:
            gtBoxes = self.gt[self.gt['frame'] == fr]#.copy(deep=True)
            dtBoxes = self.dt[self.dt['frame'] == fr]
            
            print("gtBoxes", br, gtBoxes, br, br)
            print("dtBoxes", br, dtBoxes, br, br)

            gtCentroids = []
            dtCentroids = []
            
            print("gtCentroids")
            for ind, r in gtBoxes.iterrows():
                c = [r['x_c'], r['y_c']]
                gtCentroids.append(c)
            
            for ind, r in dtBoxes.iterrows():
                c = [r['x_c'], r['y_c']]
                dtCentroids.append(c)   
                
            
            gtIDs = gtBoxes['object'].tolist()
            sortIDs = dtBoxes['objectID'].tolist()
            D = dist.cdist(gtCentroids, dtCentroids)
            print("Dist: ",br,D,br)
            D[D>0]=np.nan # Since we work on tracked ground truth boxes and not detections, we'll set NaN on distance above zero to enforce that only identical boxes are associated. 
            #print(D)
            
            acc.update(gtIDs, sortIDs, D) # Append frame data to accumulator

        print(self.dt)
        num_tracks = len(set(self.dt['objectID']))    
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
        self.write_results_file(num_frames, num_detections, num_objects, num_predictions, num_unique_objects, num_tracks, num_matches, num_switches, num_misses, num_false_positives, precision, recall, mota, motp, mostly_tracked, partially_tracked, mostly_lost)        











    # def write_header(results_filename):
    #     with open(results_filename, 'a') as resultFile: # Write the header of the output file
    #         header = f'maxDisap,maxDist,runMean,num_frames,num_detections,num_objects,num_predictions,num_unique_objects,num_tracks,num_matches,num_switches,num_misses,num_false_positives,precision,recall,mota,motp,mostly_tracked,partially_tracked,mostly_lost{br}'
    #         resultFile.write(header)

    # def write_results_file(results_filename,maxDisap,maxDist,runMean,num_frames,num_detections,num_objects, num_predictions,num_unique_objects,num_tracks,num_matches,num_switches,num_misses,num_false_positives,precision,recall,mota,motp,mostly_tracked,partially_tracked,mostly_lost):
    #     with open(results_filename, 'a') as resultFile:
    #         resultFile.write(f'{maxDisap}, {maxDist}, {runMean}, {num_frames},{num_detections},{num_objects},{num_predictions},{num_unique_objects},{num_tracks},{num_matches},{num_switches},{num_misses},{num_false_positives},{precision},{recall},{mota},{motp},{mostly_tracked},{partially_tracked},{mostly_lost}{br}')


    # # ### Prepare ground truth data
    # # def prepGT(self, gt, d):
    # #     gt['x_c'] = (gt['x_min'] + gt['x_max'])/2
    # #     gt['x_c'] = gt['x_c'].round(0).astype(int)
        
    # #     gt['y_c'] = (gt['y_min'] + gt['y_max'])/2
    # #     gt['y_c'] = gt['y_c'].round(0).astype(int)

    # #     gt['frame'] = gt['filename'].map(d) # Create a frame column by mapping filename to dictionary
        
    # #     gt['id_gt_int'] = gt.apply(lambda x: int(''.join(filter(str.isdigit, x['id_gt']))), axis=1)
        
    # #     return gt

    # # ### Prepare tracked data
    # # def prepDT(self, dt, d):
    # #     #sort.drop([6, 7, 8, 9], axis=1, inplace = True)
    # #     #print(sort)
    # #     # Make sure coordinates are right! sort.rename({0: 'frame', 1: 'id_tr', 2: 'x_min', 3: 'x_max', 4: 'y_min', 5: 'y_max', 'objectID': 'id_tr'}, axis=1, inplace=True)
    # #     dt.rename({'objectID': 'id_tr'}, axis=1, inplace=True)
    # #     #print(sort)
    # #     dt['frame'] = dt['filename'].map(d) # Create a frame column by mapping filename to dictionary
        
    # #     dt['x_c'] = (dt['x_min'] + dt['x_max'])/2
    # #     dt['x_c'] = dt['x_c'].round(0).astype(int)
        
    # #     dt['y_c'] = (dt['y_min'] + dt['y_max'])/2
    # #     dt['y_c'] = dt['y_c'].round(0).astype(int)  

    # #     return dt


    # def run(self):

    #     f = list(set(self.gt['filename'].tolist())) # Make a list of image filenames
    #     f.sort(key=lambda x: int(''.join(filter(str.isdigit, x)))) # Sort the filenames based on extracted digits in the filename
    #     d = {k: v+1 for v, k in enumerate(f)} # Make a dictionary with index
        
    #     gt = self.prepGT(self.gt, d)
    #     dt = self.prepDT(self.dt, d)
    #     self.write_header(self.results_filename)
        
    #     frames = list(set(gt['frame'].to_list()))


        
    #     # runMeanSearch = re.search('runMean_(.+?)_max', fi)
    #     # maxDistSearch = re.search('maxDist_(.+?).csv', fi)
    #     # maxDisapSearch = re.search('maxDisap_(.+?)_run', fi)
        
    #     # if runMeanSearch:
    #     #     runMean = runMeanSearch.group(1)
    
    #     # if maxDistSearch:
    #     #     maxDist = maxDistSearch.group(1)
                
    #     # if maxDisapSearch:
    #     #     maxDisap = maxDisapSearch.group(1)
            
        
    #     #print("Setting up accumulator")    
    #     acc = mm.MOTAccumulator(auto_id=True)# Create an accumulator that will be updated during each frame

    #     sort = self.prepSORT(sort, d)

    #     #num_tracks = len(set(sort['id_tr']))
    #     #print("Number of tracks: ", num_tracks)

    #     for fr in frames:
    #         gtBoxes = gt[gt['frame'] == fr]#.copy(deep=True)
    #         sortBoxes = sort[sort['frame'] == fr]
            
    #         gtCentroids = []
    #         sortCentroids = []
            
    #         for ind, r in gtBoxes.iterrows():
    #             c = [r['x_c'], r['y_c']]
    #             gtCentroids.append(c)
            
    #         for ind, r in sortBoxes.iterrows():
    #             c = [r['x_c'], r['y_c']]
    #             sortCentroids.append(c)   
                
        
    #         gtIDs = gtBoxes['id_gt_int'].tolist()
    #         sortIDs = sortBoxes['id_tr'].tolist()
    #         D = dist.cdist(gtCentroids, sortCentroids)
    #         D[D>0]= np.nan # Since we work on tracked ground truth boxes and not detections, we'll set NaN on distance above zero to enforce that only identical boxes are associated. 
    #         #print(D)
        
    #         acc.update(gtIDs, sortIDs, D) # Append frame data to accumulator
            
    #     mh = mm.metrics.create()
    #     summary = mh.compute(acc, metrics=['num_frames','num_detections', 'num_objects', 'num_predictions', 'num_unique_objects', 'num_matches','num_switches', 'num_misses', 'num_false_positives', 'precision', 'recall', 'mota', 'motp', 'mostly_tracked', 'partially_tracked', 'mostly_lost'], name='acc')
    #     #print(f'Site: {s}. GT: {impdata(s)}. SORT: {fi}')
    #     #print(summary['num_frames'].values[0])


    #     num_frames = summary['num_frames'].values[0]
    #     num_detections = summary['num_detections'].values[0]
    #     num_objects = summary['num_objects'].values[0]
    #     num_predictions = summary['num_predictions'].values[0]
    #     num_unique_objects = summary['num_unique_objects'].values[0]
    #     num_matches = summary['num_matches'].values[0]
    #     num_switches = summary['num_switches'].values[0]
    #     num_misses = summary['num_misses'].values[0]
    #     num_false_positives = summary['num_false_positives'].values[0]
    #     precision = summary['precision'].values[0]
    #     recall = summary['recall'].values[0]
    #     mota =  summary['mota'].values[0]
    #     motp =  summary['motp'].values[0]
    #     mostly_tracked = summary['mostly_tracked'].values[0]
    #     partially_tracked = summary['partially_tracked'].values[0]
    #     mostly_lost = summary['mostly_lost'].values[0]
        
    #     print("Number of mismatches: ", num_switches)
    #     print("MOTA: ", mota)
    #     #write_results_file(results_filename, maxDisap, maxDist, runMean, num_frames, num_detections, num_objects, num_predictions, num_unique_objects, num_tracks, num_matches, num_switches, num_misses, num_false_positives, precision, recall, mota, motp, mostly_tracked, partially_tracked, mostly_lost)        
    #     #del acc
    #     return num_switches