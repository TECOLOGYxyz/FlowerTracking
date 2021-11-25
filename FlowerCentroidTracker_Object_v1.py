# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 16:36:42 2021



Custom flower tracker

Simple centroid tracker that 

Detections are in the format: 

@author:
Hjalte Mann
TECOLOGY.xyz

"""

import pandas as pd # Replace with cudf if performance is too slow?
from collections import OrderedDict
import numpy as np
from scipy.spatial import distance as dist
from scipy.ndimage.filters import uniform_filter1d
import matplotlib.pyplot as plt
br = "\n"


#### SETTINGS ####

max_disappeared = 4 # Maximum number of frames the algorithm should continue to look for an object
max_distance = 20 # Maximum distance to a point before it is forced to be registered as a new ID instead of associated with the closest point
running_mean_threshold = 5 # Number of frames for calculating the running mean of the position of an object

######


#### PATH TO DETECTIONS ####
detections = pd.read_csv('Dummy_fortracking2.csv')
detections['x_c'] = (detections['x_min'] + detections['x_max']) / 2
detections['y_c'] = (detections['y_min'] + detections['y_max']) / 2

frames = list(set(detections['frame'].tolist()))

print("Here are the detections",br,detections,br)


class tracker():
    def __init__(self, max_disappeared, frames):
        self.nextObjectID = 0 # Counter for object ids
        self.objects = OrderedDict() # Dictionary. objectID is the key, centroid is the content
        self.disappeared = OrderedDict() # Keeps track of how long an objectID has been lost

        self.max_disappeared = max_disappeared # store max_disappeared number of frames
        self.frames = frames

    def store_tracking_results(self, frame, objectIDs):
        pass

    def get_frame_detections(self,frame):
        block = detections.loc[detections['frame'] == frame]
        frame_detections = block[["x_c", "y_c"]] # We just need the centroid, so we'll grab that and return it
        return frame_detections

    def register(self, centroid): # For registering a point
        self.objects[self.nextObjectID] = centroid # Set the new centroid as content for the new objectID in the Objects dictionary
        self.disappeared[self.nextObjectID] = 0 # Set number of times the new object has disappeared to zero. 
        self.nextObjectID += 1 # Add 1 to the objectID counter so it's ready for the next point

        self.length_dict = {key: len(value) for key, value in self.objects.items()}

    def deregister(self, objectID): # deregister object by deleting it from the objects dict and removing the associated counter from the disappeared dict.
        del self.objects[objectID]
        del self.disappeared[objectID]

    def update(self, frame):
        frame_detections = self.get_frame_detections(frame)#  Get the detections for the current frame
        print(f'FRAME {frame}. Contains {len(frame_detections)} points.')
        """
        If a frame has no detections, we +1 to disappeared of all objects being tracked. 
        If this takes any objects above the max_disappeared threshold, we remove them from the objects.
        """

        if frame_detections.empty: # If the frame has no detections, we will add 1 to disappeared for all objects that are being tracked.
            for objectID in list(self.disappeared.keys()): # loop over any existing tracked objects and mark them as +1 in disappeared
                self.disappeared[objectID] += 1

                if self.disappeared[objectID] > self.max_disappeared: # if we have reached a maximum number of consecutive frames where a given object has been marked as missing, deregister it
                    self.deregister(objectID)
            return self.objects # return early as there are no centroids or tracking info to update

        """
        If there are detctions in the frame, we will:
            1. Create a numpy array of the frame points
            2. Check if we are currently tracking objects.
                If not, we will start tracking the frame points
                If so, we will 
            3. 
        """
        
        inputCentroids = frame_detections.to_numpy()

        if not self.objects: # if Objects is empty, we are currently not tracking any objects and take the input centroids and register each of them
            print("Not tracking objects. Initiating tracking on current detections.")
            for i in range(0, len(inputCentroids)):
                print("Added detection ", i)
                self.register(inputCentroids[i])

            print("Current objects: ", self.objects)
            print("Object 0: ",self.objects[0])
            print("Current lengths: ", self.length_dict)
            
            
        else: # We are already tracking objects, so let's see if we can associate any frame detections with objects that are being tracked.
            print(br,"We are tracking existing objects.")    
            objectIDs = list(self.objects.keys()) # grab the set of object IDs and corresponding centroids
            objectCentroids = list(self.objects.values())
            
            print("Obj. ID: ",objectIDs)
            print("Obj. Centroids: ",br,objectCentroids)
            print("Input centroids: ",br, inputCentroids)

            D = dist.cdist(np.array(objectCentroids), inputCentroids) # compute the distance between each pair of object centroids and input centroids, respectively. Our goal will be to match an input centroid to an existing object centroid 

            print("Distance matrix: \n", D)
            D[D >= max_distance] = np.nan
            
            objectIndexes = list(range(0,len(D)))
            inputIndexes = list(range(len(D[0])))
            
            for c in range(len(D[0])): # Loop over the input centroids
                if not np.isnan(D).all():
                    result = np.unravel_index(np.nanargmin(D, axis=None), D.shape)
                    
                    D[result[0], :] = np.nan 
                    D[:,result[1]] = np.nan
                    
                    objectIndexes.remove(result[0])
                    inputIndexes.remove(result[1])
                    
                    # Here we need to update the centroid coordinates of the objects.
                    print("Setting the centroid for object ", objectIDs[result[0]], "to ", inputCentroids[result[1]]  )
                    self.objects[objectIDs[result[0]]] = inputCentroids[result[1]]
                else:
                    print("Association based on distance done. Now dealing with points that were not associated.")
                    pass
            
            print("Object indexes: ", objectIndexes)
            print("Input indexes: ", inputIndexes)
            
            print(objectIDs)
            
            for o in objectIndexes: # Add 1 to disappeared objects
                objectID = objectIDs[o]
                self.disappeared[objectID] += 1
                
                if self.disappeared[objectID] > self.max_disappeared: # if we have reached a maximum number of consecutive frames where a given object has been marked as missing, deregister it
                    self.deregister(objectID)
                    print("Deregistering!")
            
            for i in inputIndexes: # Start tracking new objects
                print("Registering point: ", i, "With the centroid: ", inputCentroids[i])
                self.register(inputCentroids[i])
            



t = tracker(max_disappeared, frames) # Instantiate the class instance and pass in the threshold for max_disappeared and the list of frames.

for f in frames:
    t.update(f)


### PLOT STUFF ###
plt.scatter(detections['x_c'],detections['y_c'], c = detections['frame'])


plt.plot(detections['x_c'],detections['y_c'])

#detections.groupby('').plot(kind='kde', ax=plt.gca())


