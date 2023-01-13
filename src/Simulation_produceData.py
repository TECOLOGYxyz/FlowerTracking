from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
import pandas as pd
import random as rand
import numpy as np
import math
from mpl_toolkits import mplot3d
import pprint
from operator import add, sub
import csv



# Get random point in the full image - this is the center point of the flower (in theory stalk position)

# Define a radius for the flower

# Generate random point within the flower circle

# Define a movement radius (max movement between frames)

# Generate random point within the movement radius and within the flower radius

# xDim = 1
# yDim = 1
# flowerRadius = 0.2 #frameDiag * 0.2
# movementRadius = 0.2 # flowerRadius * 0.001
# numberFlowers = 4
# pointsPerFlower = 1000

rand.seed(42)


### DEFINE SOME FUNCTIONS ###
class simulate():
    def __init__(self, flowerRadius, movementRadius, numberFlowers, pointsPerFlower, filename, experiment):
        self.flowerRadius = flowerRadius
        self.movementRadius = movementRadius
        self.numberFlowers = numberFlowers
        self.pointsPerFlower = pointsPerFlower
        #self.fixedPosition = fixedPosition
        #self.delete = delete
        self.flowerCenters = []
        self.flowers = []
        self.filename = filename
        self.experiment = experiment

    def checkPointInCircle(self, flowerCenter, flowerRadius, flowerPoint):
        # Compare radius of circle
        # with distance of its center
        # from given point

        if ((flowerPoint[0] - flowerCenter[0]) * (flowerPoint[0] - flowerCenter[0]) +
            (flowerPoint[1] - flowerCenter[1]) * (flowerPoint[1] - flowerCenter[1]) <= flowerRadius * flowerRadius):
            return True
        else:
            return False

    def getFlowerCenter(self):
        xFlower, yFlower = rand.uniform(0,1), rand.uniform(0,1)#flowerRadius, math.floor(xDim-flowerRadius)), rand.uniform(math.floor(yDim-flowerRadius))
        return [xFlower, yFlower]


    def getFirstFlowerPoint(self, flowerCenter):
        while True:
            r = self.flowerRadius * math.sqrt(rand.uniform(0, 1))
            theta = rand.uniform(0, 1) * 2 * math.pi

            x = flowerCenter[0] + r * math.cos(theta) #Convert to Cartesian coordinates
            y = flowerCenter[1]  + r * math.sin(theta)
            if  (0 < x < 1) and (0 < y < 1):
                return [x,y]


    def getFlowerPoints(self, firstFlowerPoint, numPoints, flowerCenter, flowerRadius):
        flowerPoints = [firstFlowerPoint]

        currentX = firstFlowerPoint[0]
        currentY = firstFlowerPoint[1]

        for i in range(numPoints-1):
            #print("Making point")
            #print("Current x and y: ", currentX, currentY)
            while True: 
                r = self.movementRadius * math.sqrt(rand.uniform(0, 1))
                theta = rand.uniform(0, 1) * 2 * math.pi
                #print("r and theta: ", r, theta)
                x = currentX + r * math.cos(theta) # Convert to Cartesian coordinates
                y = currentY  + r * math.sin(theta)
                #print("x and y:", x, y)
                if  (0 < x < 1) and (0 < y < 1) and (self.checkPointInCircle(flowerCenter, flowerRadius, (x,y))): # Check if point is within frame and within flower circle
                    flowerPoints.append([x,y])
                    currentX = x
                    currentY = y
                    break

        #print(f'{len(flowerPoints)} flower points generated.')
        return flowerPoints

        # Convert to integer frame
    def convertToInteger(self, flowers):
        convertedFlowers = []
        for s in flowers:
            f = []
            for k in s:
                x = int(k[0] * 1000)
                y = int(k[1] * 1000)
                f.append([x, y])
            convertedFlowers.append(f)
        return convertedFlowers

    ### Insert frame number and object IDs. Change this to a better solution?
    def addFrame(self, flowers, frameStart, objectStart):
        for s, k in enumerate(flowers): 
            for i, j in enumerate(k):
                j.insert(0, i+frameStart) # Insert frame number
                j.insert(0, s+objectStart) # Insert object id number
        return flowers

    def saveData(self, flowers):
        with open(self.filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows([["object", "frame", "x_c", "y_c"]])
            for s in flowers:
                writer.writerows(s)
        print("Dataset saved to csv.")


    def deletions(self, flowers):
        #d = [[0,10], [1,11], [1, 20], [0, 21]]
        # print("Before")
        # print(flowers)
        # d = [[1,1], [0,2]]
        # de = [flowers[k[0]][k[1]] for k in d]
        # after = []
        print("Before:")
        print(flowers)
        for flower in flowers:
            de = 5
            print(f'Deleting {de} points from {flower} with length {len(flower)}]')
            for i in range(de):
                flower.pop(rand.randrange(len(flower)))
        print("After")
        print(flowers)
        return flowers


    def main(self):
        if self.experiment == "runmean":
            c = [[0.3, 0.3], [0.7, 0.3], [0.3, 0.7], [0.7, 0.7]]
            for k in range(self.numberFlowers):
                t = c[k]
                self.flowerCenters.append(t)
                fp = self.getFirstFlowerPoint(t)
                flowerL = self.getFlowerPoints(fp, self.pointsPerFlower, t, self.flowerRadius)
                self.flowers.append(flowerL)
            s = self.convertToInteger(self.flowers)
            s = self.addFrame(s, 0, 0)
            self.saveData(s)
            return s
        
        if self.experiment == "maxdist":
            print("Experiment chosen: ", self.experiment)
            c = [[0.25, 0.75], [0.75, 0.25]]
            x = []
            for k in range(self.numberFlowers):
                self.flowers = []
                t = c[k]
                self.flowerCenters.append(t)
                fp = self.getFirstFlowerPoint(t)
                flowerL = self.getFlowerPoints(fp, self.pointsPerFlower, t, self.flowerRadius)
                self.flowers.append(flowerL)
                s = self.convertToInteger(self.flowers)
                s = self.addFrame(s, k*self.pointsPerFlower, k)
                print(f'Flower {k}: {s}')
                x = x + s
            self.saveData(x)
            return x

        if self.experiment == "maxgap":
            c = [[0.3, 0.3], [0.7, 0.3], [0.3, 0.7], [0.7, 0.7]]
            for k in range(self.numberFlowers):
                t = c[k]
                self.flowerCenters.append(t)
                fp = self.getFirstFlowerPoint(t)
                flowerL = self.getFlowerPoints(fp, self.pointsPerFlower, t, self.flowerRadius)
                self.flowers.append(flowerL)
            s = self.convertToInteger(self.flowers)
            s = self.addFrame(s, 0, 0)
            s = self.deletions(s)
            self.saveData(s)
            return s

        if self.experiment == "framerate":
            c = [[0.1, 0.1], [0.1, 0.1], [0.1, 0.1], [0.1, 0.1]]
            for k in range(self.numberFlowers):
                t = c[k]
                self.flowerCenters.append(t)
                fp = self.getFirstFlowerPoint(t)
                flowerL = self.getFlowerPoints(fp, self.pointsPerFlower, t, self.flowerRadius)
                self.flowers.append(flowerL)
            s = self.convertToInteger(self.flowers)
            s = self.addFrame(s, 0, 0)
            self.saveData(s)
            return s


        else:
            print("No known experiment chosen.")
            for k in range(self.numberFlowers):
                t = self.getFlowerCenter()
                self.flowerCenters.append(t)
                fp = self.getFirstFlowerPoint(t)
                flowerL = self.getFlowerPoints(fp, self.pointsPerFlower, t, self.flowerRadius)
                self.flowers.append(flowerL)
                s = self.convertToInteger(self.flowers)
                s = self.addFrame(s)
                self.saveData(s)
            return s



#flowerRadius, movementRadius, numberFlowers, pointsPerFlower, fixedPosition, filename)

## RUNNING MEAN DATASET ###
# s = simulate(0.2, 0.2 ,4, 500, "data/simulation/runmeanExample.csv", "runmean")
# p = s.main()

## MAX DISTANCE DATASET ###
# s = simulate(0.2, 0.1 ,2, 10, "data/maxdistExample.csv", "maxdist")
# p = s.main()
# print(p)


 ## MAX GAP DATASET ###
# s = simulate(0.2, 0.1, 4, 10, "data/maxgapExample.csv", "maxgap")
# p = s.main()


 ## FRAME RATE DATASET ###
# s = simulate(0.1, 0.001, 4, 10000, "data/framerateExample.csv", "framerate")
# p = s.main()

# Frame rate 2nd
"""
Read the data
Grab every second frame
Adjust frame number
"""
#df = pd.read_csv(r"U:\BITCue\Projekter\TrackingFlowers\data\simulation\framerateExample.csv")
# second = df.iloc[::2]
# second['frame'] = second.groupby(['object']).cumcount()
# second.to_csv(r"U:\BITCue\Projekter\TrackingFlowers\data\simulation\framerateExample_2nd.csv", index=False)


# Frame rate 3rd
# fourth = df.iloc[::4]
# fourth['frame'] = fourth.groupby(['object']).cumcount()
# fourth.to_csv(r"U:\BITCue\Projekter\TrackingFlowers\data\simulation\framerateExample_4th.csv", index=False)

# Frame rate 10th
# tenth = df.iloc[::10]
# tenth['frame'] = tenth.groupby(['object']).cumcount()
# tenth.to_csv(r"U:\BITCue\Projekter\TrackingFlowers\data\simulation\framerateExample_10th.csv", index=False)

# Frame rate 20th
# twentieth = df.iloc[::20]
# twentieth['frame'] = twentieth.groupby(['object']).cumcount()
# twentieth.to_csv(r"U:\BITCue\Projekter\TrackingFlowers\data\simulation\framerateExample_20th.csv", index=False)

# Frame rate 30th
# thirteth = df.iloc[::30]
# thirteth['frame'] = thirteth.groupby(['object']).cumcount()
# thirteth.to_csv(r"U:\BITCue\Projekter\TrackingFlowers\data\simulation\framerateExample_30th.csv", index=False)

# Frame rate 100th
#hundreth = df.iloc[::100]
#hundreth['frame'] = hundreth.groupby(['object']).cumcount()
#hundreth.to_csv(r"U:\BITCue\Projekter\TrackingFlowers\data\simulation\framerateExample_100th.csv", index=False)






# # ### PLOT DATA - 3D ###
# # fig = plt.figure()
# # ax = plt.axes(projection ='3d') # syntax for 3-D projection
# # ax.set_xlim([0, 1000])
# # ax.set_ylim([0, 1000])

# # # Add data to plot
# # for s in flowers:
# #     #print(s)
# #     ax.plot3D(np.array(s)[:,2], np.array(s)[:,3], np.array(s)[:,1])

# # ax.set_title('Generated flower tracks')
# # plt.show()

# # ### PLOT DATA - 2D ###
# fig, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot
# for i,s in enumerate(p):
    #fc = [int(b*1000) for b in flowerCenters[i]]
    # k = plt.Circle((fc), flowerRadius*1000, fill = False, color = "r")
    # ax.add_patch(k)
    # ax.scatter(np.array(s)[:,2], np.array(s)[:,3])
    # for l in s:
    #     k = plt.Circle((l[2], l[3]), movementRadius*1000, fill = False)
    #     ax.add_patch(k)
# plt.xlim([0, 1000])
# plt.ylim([0, 1000])
# plt.show()




    ### ADD NOISE - DISCARDED ###
    # def addNoise(self, flowers):
    #     positionChoices = rand.sample(range(1,self.pointsPerFlower), 3)
    #     # np.random.seed(42)
    #     # flowerChoices = np.random.choice(range(numberFlowers), size = 100)
    #     np.random.seed(43)
    #     coordChoices = np.random.choice([0,1], size = 200)
    #     np.random.seed(44)
    #     operatorChoices = np.random.choice([0,1], size = 200)
    #     ops = [add, sub]
    #     operatorChoices = [ops[i] for i in operatorChoices]
    #     ccc = rand.sample(range(1, 201), 200)
    #     ccc = [x/100 for x in ccc]

    #     print(positionChoices)
    #     print(flowers)
    #     for i,p in enumerate(positionChoices):
    #     # flowerChoice = flowerChoices[i]
    #         coordChoice = coordChoices[i]
    #         positionChoice = p
    #         operatorChoice = operatorChoices[i]
    #         factorChoice = ccc[i]

    #         noise = int(200 * factorChoice)

    #         for f in flowers:
    #             f[positionChoice][coordChoice] = operatorChoice(f[positionChoice][coordChoice], noise)

    #             if f[positionChoice][coordChoice]< 0:
    #                 f[positionChoice][coordChoice]= 0
    #             if f[positionChoice][coordChoice] > 1000:
    #                 f[positionChoice][coordChoice] = 1000
    #     return flowers
