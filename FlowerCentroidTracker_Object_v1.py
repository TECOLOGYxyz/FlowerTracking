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

max_disappeared = 5 # Maximum number of frames the algorithm should continue to look for an object
max_distance = 500 # Maximum distance to a point before it is forced to be registered as a new ID instead of associated with the closest point
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
            
            rows = D.min(axis=1).argsort()
            print(rows)
            # For 
            
            #D_passed = D[D.distance <= max_distance]
            # print(D_passed)
#             D_passed = D_passed.loc[D_passed.groupby('id').distance.idxmin()] # If the there are more than one frame point that is close to an object point, use the one closest. TO-DO: What happens if two frame points have the same distance to the object point?
#             print("Frame points and closest object point, below threshold: \n:", D_passed)
#         
#             D_passed = D_passed[['id', 'x_c_y', 'y_c_y']] # Grab the relevant columns from the D_passed dataframe
#             D_passed.columns = ['id', 'x_c', 'y_c'] # Rename columns
#             D_passed.set_index('id') # Set id as the index
#             objects.update(D_passed) # And update the coordinates for the objects.
#         
#         
        # # If the distance is above the threshold, we'll register the points as new objects
        # D_failed = D[D.distance > max_distance]
        # if not D_failed.empty:
        #     register(D_failed)
        # print("Failed: \n:", D_failed)

#             rows = D.min(axis=1).argsort() # in order to perform this matching we must (1) find the smallest value in each row and then (2) sort the row indexes based on their minimum values so that the row with the smallest value as at the *front* of the index list
#             cols = D.argmin(axis=1)[rows] # next, we perform a similar process on the columns by finding the smallest value in each column and then sorting using the previously computed row index list

#             usedRows = set() # in order to determine if we need to update, register, or deregister an object we need to keep track of which of the rows and column indexes we have already examined
#             usedCols = set()


#             print("These are the matches: ",br, list(zip(rows, cols)), br)

#             for (row, col) in zip(rows, cols): # loop over the combination of the (row, column) index tuples if we have already examined either the row or column value before, ignore it
#                 if row in usedRows or col in usedCols or D[row,col] > max_distance:
#                     continue
#                 
#                 objectID = objectIDs[row] # otherwise, grab the object ID for the current row...
#                 self.objects[objectID] = inputCentroids[col] #  ...set its new centroid...
#                 self.disappeared[objectID] = 0 # ... and reset the disappeared counter

#                 usedRows.add(row)# indicate that we have examined each of the row and column indexes, respectively
#                 usedCols.add(col)

#             unusedRows = set(range(0, D.shape[0])).difference(usedRows) # compute both the row and column index we have NOT yet examined
#             unusedCols = set(range(0, D.shape[1])).difference(usedCols)

#             print("Unused rows: ", unusedRows)
#             print("Unused cols: ", unusedCols)
#             print("Disapeared: ", self.disappeared)
#             #print(D)
#             if unusedRows: # If there are objects that were not matched to a frame detection, set disappeared + 1
#                 for row in unusedRows: # loop over the unused row indexes grab the object ID for the corresponding row index and increment the disappeared counter
#                     objectID = objectIDs[row]
#                     self.disappeared[objectID] += 1

#                     if self.disappeared[objectID] > self.max_disappeared: # check to see if the number of consecutive frames the object has been marked "disappeared" for warrants deregistering the object
#                         self.deregister(objectID)
#             
#             if unusedCols: # If there are frame detections that were not matched to an existing object, add them to the objects
#                 for col in unusedCols:
#                     self.register(inputCentroids[col])
#         return self.objects # return the set of trackable objects



t = tracker(max_disappeared, frames) # Instantiate the class instance and pass in the threshold for max_disappeared and the list of frames.

for f in frames:
    t.update(f)


### PLOT STUFF ###
plt.scatter(detections['x_c'],detections['y_c'], c = detections['frame'])


plt.plot(detections['x_c'],detections['y_c'])

#detections.groupby('').plot(kind='kde', ax=plt.gca())


"""

#### FUNCTIONS ####

def distance(a,b): # Calculate distance between two points.
     dist = np.linalg.norm(a-b)
     return dist


def register(D_failed): # For registering new points. Each row of a pandas dataframe is a new point
    global nextObjectID
    for i,r in D_failed.iterrows():
        centroid = (r['x_c_y'],r['y_c_y'])
        objects.loc[nextObjectID] = centroid
    #disappeared[nextObjectID] = 0 # Set number of times the new object has disappeared to zero. 
        nextObjectID += 1 # Add 1 to the objectID counter so it's ready for the next point


# def deregister(objectID): # to deregister an object ID we delete the object ID from both of our respective dictionaries
#     del objects[objectID]
#     del disappeared[objectID]


def build_tracked_dataframe():
    pass


def get_frame_detections(frame):
    block = detections.loc[detections['frame'] == frame]
    frame_detections = block[["x_c", "y_c"]] # We just need the centroid, so we'll grab that and return it
    return frame_detections


def update(frame_detections):
    global nextObjectID
    
    if objects.empty: # if Objects is empty, we are currently not tracking any objects, so we take the input and set it as the objects
        objects['x_c'] = frame_detections['x_c']
        objects['y_c'] = frame_detections['y_c']
        nextObjectID = frame_detections.shape[0] + 1 # Set the nextObjectID to one above the number of objects we just added
        print("First frame. Added these objects: \n", objects)
    else:
        print("We are tracking objects") # We are already tracking objects, so we need to compare the new frame detections with the already registered objects
        frame_detections['f_id'] = frame_detections.index
        D = objects.reset_index().merge(frame_detections, how='cross') # Calculate the cross product between the rows of the object points and the frame points (get all combination of rows between the two dataframes)
        D['distance'] = np.linalg.norm(D[["x_c_x", "y_c_x"]].values - D[["x_c_y", "y_c_y"]].values, axis=1)
        
        print("Full distance df: \n", D)
        # Get all the frame points and their closest object point
        D = D.iloc[D.groupby('f_id').distance.idxmin()] # Here's the objects with their closest point from the frame detections
        print("Frames points and closest object point: \n", D)
        
        # If the distance between a tracked object and a frame point is equal to or less than the thresshold, we'll update the object coordinates
        
        D_passed = D[D.distance <= max_distance]
        D_passed = D_passed.loc[D_passed.groupby('id').distance.idxmin()] # If the there are more than one frame point that is close to an object point, use the one closest. TO-DO: What happens if two frame points have the same distance to the object point?
        print("Frame points and closest object point, below threshold: \n:", D_passed)
        
        D_passed = D_passed[['id', 'x_c_y', 'y_c_y']] # Grab the relevant columns from the D_passed dataframe
        D_passed.columns = ['id', 'x_c', 'y_c'] # Rename columns
        D_passed.set_index('id') # Set id as the index
        objects.update(D_passed) # And update the coordinates for the objects.
        
        
        # If the distance is above the threshold, we'll register the points as new objects
        D_failed = D[D.distance > max_distance]
        if not D_failed.empty:
            register(D_failed)
        print("Failed: \n:", D_failed)
        
        # Find the frame detections that were not associated with an object and register them
        
        
        # Find the objects that were not associated with a point and add 1 to their dis_count

def plot_tracking(detections, frame, title):
    plt.scatter(detections['x_c'], detections['y_c'])
    plt.xlim(0, 6080)
    plt.ylim(0, 3420)
    plt.title(title + str(f))
    plt.show()



for f in frames:
    frame_detections = get_frame_detections(f)
    plot_tracking(frame_detections,f, "Untracked")
    update(frame_detections)
    plot_tracking(objects, f, "Tracked")

print("Final objects \n", objects)

"""
#plot_untracked(detections)
#plot_tracked(objects)


# def update(frame_detections):
#     if not objects: # if Objects is empty, we are currently not tracking any objects and take the input centroids and register each of them
#         for i in range(0, len(frame_detections)):
#             #print(i, frame_detections[i])
#             register(frame_detections[i])
#     else:
#         print("Objects: \n",objects)
#         print("New centroids: \n", frame_detections)
#         objectIDs = list(objects.keys()) # grab the set of object IDs and corresponding centroids
#         objectCentroids = list(objects.values())
#         D = sc_dist.cdist(np.array(objectCentroids), frame_detections)
#         print(D)
#         rows = D.min(axis=1).argsort() # in order to perform this matching we must (1) find the smallest value in each row and then (2) sort the row indexes based on their minimum values so that the row with the smallest value as at the *front* of the index list
#         cols = D.argmin(axis=1)[rows]
#         print("Rows: ", rows)
#         print("Cols :", cols) # next, we perform a similar process on the columns by finding the smallest value in each column and then sorting using the previously computed row index list


######





# for f in frames:
#     frame_detections = get_frame_detections(f)
#     #print(frame_detections)
#     update(frame_detections)

#print(np.array(objects))
