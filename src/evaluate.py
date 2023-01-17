# -*- coding: utf-8 -*-

# Import global packages
import motmetrics as mm
from scipy.spatial import distance as dist
import numpy as np

br = '\n'


class evaluator():
    def __init__(self, dt, gt, results_filename, verbose):
        self.dt = dt
        self.gt = gt
        self.results_filename = results_filename
        self.verbose = verbose


    def write_header(self, results_filename):
        with open(results_filename, 'a') as resultFile: # Write the header of the output file
            header = f'num_frames,num_detections,num_objects,num_predictions,num_unique_objects,num_tracks,num_matches,num_switches,num_misses,num_false_positives,precision,recall,mota,motp,mostly_tracked,partially_tracked,mostly_lost{br}'
            resultFile.write(header)

    def write_results_file(self, results_filename, num_frames,num_detections,num_objects, num_predictions,num_unique_objects,num_tracks,num_matches,num_switches,num_misses,num_false_positives,precision,recall,mota,motp,mostly_tracked,partially_tracked,mostly_lost):
        with open(results_filename, 'a') as resultFile:
            resultFile.write(f'{num_frames},{num_detections},{num_objects},{num_predictions},{num_unique_objects},{num_tracks},{num_matches},{num_switches},{num_misses},{num_false_positives},{precision},{recall},{mota},{motp},{mostly_tracked},{partially_tracked},{mostly_lost}{br}')


    def run(self):
        frames = list(set(self.gt['frame'].to_list()))

        acc = mm.MOTAccumulator(auto_id=True)# Create an accumulator that will be updated during each frame

        num_tracks = len(set(self.dt['id_tr']))
        

        for fr in frames:
            gtBoxes = self.gt[self.gt['frame'] == fr]
            dtBoxes = self.dt[self.dt['frame'] == fr]
            
            gtCentroids = []
            dtCentroids = []
            
            for ind, r in gtBoxes.iterrows():
                c = [r['x_c'], r['y_c']]
                gtCentroids.append(c)
            
            for ind, r in dtBoxes.iterrows():
                c = [r['x_c'], r['y_c']]
                dtCentroids.append(c)   
                
            
            gtIDs = gtBoxes['id_gt_int'].tolist()
            dtIDs = dtBoxes['id_tr'].tolist()
            D = dist.cdist(gtCentroids, dtCentroids)
            D[D>0]=np.nan # Since we work on tracked ground truth boxes and not detections, we'll set NaN on distance above zero to enforce that only identical boxes are associated. 
            #print(D)
            
            acc.update(gtIDs, dtIDs, D) # Append frame data to accumulator
            
        mh = mm.metrics.create()
        summary = mh.compute(acc, metrics=['num_frames','num_detections', 'num_objects', 'num_predictions', 'num_unique_objects', 'num_matches','num_switches', 'num_misses', 'num_false_positives', 'precision', 'recall', 'mota', 'motp', 'mostly_tracked', 'partially_tracked', 'mostly_lost'], name='acc')

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
        if self.verbose:
            print("Number of tracks: ", num_tracks)
            print("Number of mismatches: ", num_switches)
            print("MOTA: ", mota)
        self.write_header(self.results_filename)
        self.write_results_file(self.results_filename, num_frames, num_detections, num_objects, num_predictions, num_unique_objects, num_tracks, num_matches, num_switches, num_misses, num_false_positives, precision, recall, mota, motp, mostly_tracked, partially_tracked, mostly_lost)        
        return num_tracks, num_switches

### END OF SCRIPT ###