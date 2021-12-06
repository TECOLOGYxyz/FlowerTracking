# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 16:36:42 2021



Custom flower tracker

Multiobject tracker tracker

Max distance, max dissapeared, running mean


Detections are in the format: 

@author:
Hjalte Mann
TECOLOGY.xyz

"""

import pandas as pd # Replace with cudf if performance is too slow?
from collections import OrderedDict
import numpy as np
from scipy.spatial import distance as dist
#from scipy.ndimage.filters import uniform_filter1d
import matplotlib.pyplot as plt
import time
from statistics import mean


br = "\n"

"""
TO-DO

- Record tracks and output a result file
- Create running mean solution
- Plot results
- Create option to disregard max_distance (to use on non-fixed objects)

"""


#### SETTINGS ####

resultFilename = "../testResults/trackResults7.csv"

max_disappeared = 4 # Maximum number of frames the algorithm should continue to look for an object
max_distance = 500 # Maximum distance to a point before it is forced to be registered as a new ID instead of associated with the closest point
running_mean_threshold = 5 # Number of frames for calculating the running mean of the position of an object

######


# objects = OrderedDict()
# objects[0] = [[2,3]]
# objects[1] = [[4,5]]
# objects[1].append([6,7])

# means = OrderedDict()

# def runningMean(dic):
#     for key, value in dic.items():
#         print(key, value)
#         print(len(value))
#         if len(value) == 1:
#             means[key] = value
#         if len(value) > 1:
#             c_m = [mean([i[0] for i in value]), mean([i[1] for i in value])]
#             means[key] = c_m
            
       
# runningMean(objects)

# print("Objects: ", br, objects)
# print("Means: ", br, means)

#### PATH TO DETECTIONS ####
#detections = pd.read_csv(r'../Dummy_fortracking2.csv')
detections = pd.read_csv(r"U:\BITCue\Projekter\TrackingFlowers\data\annotations\2020_05_15_NorwayAnnotations_THUL-01_IndividualAnnotations_FRCNN_Metrics.csv")


detections['frame'] = detections['filename'].str.extract('(\d{6})')

detections['x_c'] = (detections['x_min'] + detections['x_max']) / 2
detections['y_c'] = (detections['y_min'] + detections['y_max']) / 2

detections['frame'] = detections['frame'].astype('int')

frames = list(set(detections['frame'].tolist()))
frames = sorted([int(i) for i in frames])
print(frames)


#print("Here are the detections",br,detections,br)


with open(resultFilename, 'a') as resultFile:
    header = 'frame,filename,x_c,y_c,objectID\n'
    resultFile.write(header)  

class tracker():
    def __init__(self, max_disappeared, frames):
        self.nextObjectID = 0 # Counter for object ids
        self.objects = OrderedDict() # Dictionary. objectID is the key, centroid is the content
        self.means = OrderedDict() # Dictionary to keep track of running means of object coordinates
        
        self.disappeared = OrderedDict() # Keeps track of how long an objectID has been lost

        self.max_disappeared = max_disappeared # store max_disappeared number of frames
        self.frames = frames
        
        self.tracks = []
        
    def store_tracking_results(self, frame, centroid, objectID):
        #print(br, f'Object ID {objectID} with centroid {centroid} in frame {frame} stored.', br)
        self.tracks.append([frame, centroid[0], centroid[1], objectID])

    def write_tracks_file(self):
        starttime = time.time()
        #line = detections.loc[(detections['frame'] == frame) & (detections['x_c'] == centroid[0])]
    
        with open(resultFilename, 'a') as resultFile:
            for t in self.tracks:
                frame = t[0]
                x_c = t[1]
                y_c = t[2]
                objectID = t[3]
                filename = detections.loc[detections['frame'] == frame, 'filename'].iloc[0]
                resultFile.write(f'{frame},{filename},{x_c},{y_c},{objectID}{br}')
        endtime = time.time()
        print(f'Writing done. That took {round(endtime-starttime, 4)} seconds.')

    def get_frame_detections(self, frame):
        block = detections.loc[detections['frame'] == frame]
        frame_detections = block[["x_c", "y_c"]] # We just need the centroid, so we'll grab that and return it
        return frame_detections

    def register(self, frame, centroid): # For registering a point
        print("Centroid for registering: ", centroid)
        self.objects[self.nextObjectID] = [centroid] # Set the new centroid as content for the new objectID in the Objects dictionary
        self.means[self.nextObjectID] = centroid
        
        self.disappeared[self.nextObjectID] = 0 # Set number of times the new object has disappeared to zero. 

        self.length_dict = {key: len(value) for key, value in self.objects.items()}
        
        self.store_tracking_results(frame, centroid, self.nextObjectID)
        
        self.nextObjectID += 1 # Add 1 to the objectID counter so it's ready for the next point
        
        print("Current objects: ", br, self.objects)
        
    def deregister(self, objectID): # deregister object by deleting it from the objects dict and removing the associated counter from the disappeared dict.
        del self.objects[objectID]
        del self.disappeared[objectID]
        del self.means[objectID]
    
    def update_object(self, objectID, centroid):
        # First we'll update the dictionary storing the object centroids
        print("Received in update", br, "Object id: ", objectID, br, "Centroid: ", centroid, br)
        if len(self.objects[objectID]) < running_mean_threshold:
            print("Length is less than running mean threshold.")
            print("Appending ", [centroid], " to ", self.objects[objectID])
            self.objects[objectID].append(centroid)
            
        if len(self.objects[objectID]) == running_mean_threshold:
            print("Length is equal to running mean threshold.")
            print("Deleting first item in ",self.objects[objectID], "(",self.objects[objectID][0],")")
            del self.objects[objectID][0]
            print("Appending ", centroid)
            
            self.objects[objectID].append(centroid)
            print("Updated: ",self.objects[objectID] )
        
    def update_means(self):
        print("Updating means dictionary")
        for key, value in self.objects.items():
            print("Key ", key, "value", value)
            if len(value) > 1:
                print("Length is more than one")
                c_m = [mean([i[0] for i in value]), mean([i[1] for i in value])]
                print("Means calculated to: ", c_m)
                self.means[key] = c_m
        print("Current mean dict: ", br, self.means)
        
        
    def track(self, frame):
        frame_detections = self.get_frame_detections(frame)#  Get the detections for the current frame
        print(f'FRAME {frame}. Contains {len(frame_detections)} points.')
        """
        If a frame has no detections, we +1 to disappeared of all objects being tracked. 
        If this takes any objects above the max_disappeared threshold, we remove them from the objects.
        """

        if frame_detections.empty: # If the frame has no detections, we will add 1 to disappeared for all objects that are being tracked.
            for objectID in list(self.disappeared.keys()): # loop over any existing tracked objects and mark them as +1 in disappeared
                print("Object id in disappeared: ", objectID)
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
        
        #inputCentroids = frame_detections.to_numpy()
        inputCentroids = frame_detections[['x_c', 'y_c']].values.tolist()
        
        print("input centroids: ",br ,inputCentroids)
        
        if not self.objects: # if Objects is empty, we are currently not tracking any objects and take the input centroids and register each of them
            print("Not tracking objects. Initiating tracking on current detections.")
            for i in range(0, len(inputCentroids)):
                print("Adding detection ", i)
                self.register(frame, inputCentroids[i])

            print("Current objects: ", self.objects)
            print("Object 0: ",self.objects[0])
            print("Current lengths: ", self.length_dict)
            
            
        else: # We are already tracking objects, so let's see if we can associate any frame detections with objects that are being tracked.
            print(br,"We are tracking existing objects.")    
            objectIDs = list(self.means.keys()) # grab the set of object IDs and corresponding centroids
            objectCentroids = list(self.means.values())

            
            print("Obj. ID: ",objectIDs)
            print("Obj. Centroids: ",br,objectCentroids)
            print("Input centroids: ",br, inputCentroids)

            D = dist.cdist(objectCentroids, inputCentroids) # compute the distance between each pair of object centroids and input centroids, respectively. Our goal will be to match an input centroid to an existing object centroid 

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
                    
                    #print("Loop ", c)
                    #print(D, br)
                    # Here we need to update the centroid coordinates of the objects.
                    #print("Setting the centroid for object ", objectIDs[result[0]], "to ", inputCentroids[result[1]])
                    
                    print(br)
                    print("Input centroid: ", inputCentroids[result[1]])
                    print("Object ids: ", objectIDs[result[0]])
                    ### Use update here! self.objects[objectIDs[result[0]]] = inputCentroids[result[1]]
                    self.update_object(objectIDs[result[0]], inputCentroids[result[1]])
                    
                    
                    print(self.objects[objectIDs[result[0]]])
                    print(self.objects)
                    print(br)
                    
                    #self.objects[objectIDs[result[0]]] = inputCentroids[result[1]]
                    self.store_tracking_results(frame, inputCentroids[result[1]], objectIDs[result[0]]) # And store the tracking information
              
                else:
                    #print("Association based on distance done. Now dealing with points that were not associated.")
                    pass
            
            self.update_means()
            #print("Object indexes: ", objectIndexes)
            #print("Input indexes: ", inputIndexes)
            
            print("Object indices: ",br, objectIndexes, br)
            print("Disappeared df: ", br, self.disappeared, br)
            
            
            for o in objectIndexes: # Add 1 to disappeared objects
                objectID = objectIDs[o]
                self.disappeared[objectID] += 1
                if self.disappeared[objectID] > self.max_disappeared: # if we have reached a maximum number of consecutive frames where a given object has been marked as missing, deregister it
                    self.deregister(objectID)
                    #print("Deregistering!")
            
            for i in inputIndexes: # Start tracking new objects
                #print("Registering point: ", i, "With the centroid: ", inputCentroids[i])
                self.register(frame, inputCentroids[i])
        






### RUN ###
t = tracker(max_disappeared, frames) # Instantiate the class instance and pass in the threshold for max_disappeared and the list of frames.

starttime = time.time()

for f in frames:
    t.track(f)
    
endtime = time.time()
print(f'Tracking done. That took {round(endtime-starttime, 3)} seconds. That is {round((endtime-starttime)/len(frames), 3)} seconds per frame.')
   
t.write_tracks_file()


### PLOT STUFF ###
#plt.scatter(detections['x_c'], detections['y_c'], c = detections['frame'])
#plt.plot(detections['x_c'],detections['y_c'])

tracks = pd.read_csv(resultFilename)
print(tracks)

#tracks['hello'] = tracks['objectID'].astype(float).astype(int)
#plt.scatter(tracks['x_c'], tracks['y_c'], c = tracks['objectID'])
#detections.groupby('').plot(kind='kde', ax=plt.gca())

