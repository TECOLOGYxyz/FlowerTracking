# -*- coding: utf-8 -*-

# Import local packages
from track import tracker
from filter import filterer
from evaluate import evaluator
import numpy as np

# Import global packages
import pandas as pd

"""
This script runs the tracking, filtering, and evaluation algorithms against some test data to see if all behaves as expected. Tests will fail if any algorithm does not give the expected output.

"""

correct_tracked = [[0, 687, 811, 0], [1, 714, 480, 0], [1, 466, 376, 1], [1, 236, 822, 2], [2, 428, 299, 1], [2, 693, 881, 0], [3, 630, 335, 1], [3, 299, 861, 0], [4, 702, 323, 1], [5, 643, 303, 1], [5, 450, 325, 3], [5, 231, 769, 4], [6, 660, 814, 4], [7, 582, 856, 4], [7, 333, 278, 5], [7, 657, 265, 6], [7, 138, 720, 7], [8, 108, 652, 7], [8, 645, 780, 4], [9, 394, 197, 7]]
correct_filtered = pd.DataFrame(data={'frame': [1, 7, 7], 'filename': ["simulation_run", "simulation_run", "simulation_run"], 'x_min': [235, 332, 656], 'x_max': [237, 334, 658], 'y_min': [821, 277, 264], 'y_max': [823, 279, 266], 'x_c': [236, 333, 657], 'y_c': [822, 278, 265], 'objectID':[2, 5, 6]})
correct_evaluated = (8,9)

def test_tracking():
    print("Testing tracking algorithm...")
    sims = pd.read_csv(r"./src/test/test_dataExample.csv") # Read the simulated data
    sims['filename'] = "simulation_run" # Add a filename column to the dataframe
    sims['x_min'] = sims["x_c"] - 1 # Add top left, bottom right bounding box coordinates (to simulate format of detection)
    sims['x_max'] = sims["x_c"] + 1
    sims['y_min'] = sims["y_c"] - 1
    sims['y_max'] = sims["y_c"] + 1

    # # We are ready to run tracking on the file
    t = tracker(max_gap = 0, max_distance = 0,  running_mean_threshold = 1, results_filename = r"testResult_trackingOutput.csv", detections = sims, verbose = False) # Instantiate the class instance and pass in the threshold for max_disappeared and the list of frames.
    r = t.track() # Run the tracking algorithm.
    assert r == correct_tracked, "Tracking algorithm is not giving the expected output. Check input and output."
    print("### TRACKING ALGORITHM PASSED TEST ###")



def test_filtering():
    print("Testing filtering algorithm...") 
    dt = r'./src/test/test_trackedExample.csv'
    # gt = pd.read_csv(r".\data\annotations\2020_05_17_NorwayAnnotations_NARS-04_IndividualAnnotations_FRCNN_Metrics.csv")
    # gt['id_gt_int'] = gt.apply(lambda x: int(''.join(filter(str.isdigit, x['id_gt']))), axis=1)

    # Run filtering
    d = filterer(dt, eps_distance = 100)
    filteredTracks = d.run()
    filteredTracks.to_csv(r'testResult_filteringOutput.csv') # Save the filtered tracks to csv
    assert np.array_equal(filteredTracks.values, correct_filtered.values), "Filtering algorithm is not giving the expected output. Check input and output."
    print("### FILTERING ALGORITHM PASSED TEST ###")


def test_evaluating():
    print("Testing evaluation algorithm...")
    ## Run the evalutor on the tracked vs ground truth dataframes to get tracking accuracy scores
    gt = pd.read_csv(r"./src/test/test_dataExample.csv")
    gt['id_gt_int'] = gt['object'] # The evaluator needs a column named "id_gt" with integer objects IDs for the ground truth. For the simulated data, we can just use the original object ids.

    dt = pd.read_csv(r"./src/test/test_trackedExample.csv")
    dt.rename({'objectID': 'id_tr'}, axis=1, inplace=True) # The evaluator needs a column named "id_gt" with integer objects IDs for the ground truth. For the simulated data, we can just use the original object IDs.

    e = evaluator(dt, gt, 'testResult_evaluationOutput.csv', verbose = False)
    k = e.run()
    assert k == correct_evaluated, "Evaluation algorithm is not giving the expected output. Check input and output."
    print("### EVALUATION ALGORITHM PASSED TEST ###")


test_tracking()
test_filtering()
test_evaluating()
print("##### All tests done. Good to go. #####")



### END OF SCRIPT ###