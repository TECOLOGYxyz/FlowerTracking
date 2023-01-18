import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from mpl_toolkits import mplot3d

tran = {0:"a",
        1:"b",
        2:"c",
        3:"d"
        }

# Read data

### MAX GAP ###
maxgap = pd.read_csv(r"U:\BITCue\Projekter\TrackingFlowers\data\simulation/maxgapExample.csv")

maxgap['objectLetter'] = maxgap['object'].map(lambda x: tran[x])

f, (ax1, ax2) = plt.subplots(2, 1, sharex=False, height_ratios=[4, 1])

ax1.set_xlim([0, 1000])
ax1.set_ylim([0, 1000])
ax2.margins(y = 0.2)

ax1.scatter(maxgap["x_c"], maxgap["y_c"], c=maxgap['object'])
ax1.set_box_aspect(1)
ax1.set_title('Max gap')
ax2.scatter(maxgap["frame"], maxgap["objectLetter"], c = maxgap['object'])
ax2.xaxis.set_ticks(np.arange(0, 10, 1))
ax2.set_box_aspect(1/4)
ax2.invert_yaxis()
#plt.savefig(r"U:\BITCue\Projekter\TrackingFlowers\data\simulation/maxgapPlot.pdf", bbox_inches='tight')
plt.show()


# ### MAX DIST ###

maxdist = pd.read_csv(r"U:\BITCue\Projekter\TrackingFlowers\data\simulation/maxdistExample.csv")

maxdist['objectLetter'] = maxdist['object'].map(lambda x: tran[x])
print(maxdist)
f, (ax1, ax2) = plt.subplots(2, 1, sharex=False, height_ratios=[4, 1])

ax1.set_xlim([0, 1000])
ax1.set_ylim([0, 1000])
ax1.set_xlabel("hello")
ax2.margins(y = 0.2)

ax1.scatter(maxdist["x_c"], maxdist["y_c"], c = maxdist['object'])
ax1.set_box_aspect(1)
ax1.set_title('Max distance')
ax2.scatter(maxdist["frame"], maxdist["objectLetter"], c = maxdist['object'])
ax2.xaxis.set_ticks(np.arange(0, 20, 2))
ax2.set_box_aspect(1/4)
ax2.invert_yaxis()

arrowX = maxdist['x_c'][(maxdist['frame'] == max(maxdist['frame'][maxdist['object'] == min(maxdist['object'])]))]
arrowY = maxdist['y_c'][(maxdist['frame'] == max(maxdist['frame'][maxdist['object'] == min(maxdist['object'])]))]
arrowXend = maxdist['x_c'][(maxdist['frame'] == min(maxdist['frame'][maxdist['object'] == max(maxdist['object'])]))]
arrowYend = maxdist['y_c'][(maxdist['frame'] == min(maxdist['frame'][maxdist['object'] == max(maxdist['object'])]))]

ax1.annotate("", xy = (arrowX,arrowY), xytext = (arrowXend, arrowYend), arrowprops=dict(arrowstyle="<->"))




#plt.savefig(r"U:\BITCue\Projekter\TrackingFlowers\data\simulation/maxdistPlot.pdf", bbox_inches='tight')
plt.show()



### RUN MEAN ###
runmean = pd.read_csv(r"U:\BITCue\Projekter\TrackingFlowers\data\simulation/runmeanExample.csv")

runmean['objectLetter'] = runmean['object'].map(lambda x: tran[x])

f, (ax1, ax2) = plt.subplots(2, 1, sharex=False, height_ratios=[4, 1])

ax1.set_xlim([0, 1000])
ax1.set_ylim([0, 1000])
ax2.margins(y = 0.2)

ax1.scatter(runmean["x_c"], runmean["y_c"], c = runmean['object'], s = 10)
ax1.set_box_aspect(1)
ax1.set_title('Running mean')
ax2.scatter(runmean["frame"], runmean["objectLetter"], c = runmean['object'], s = 10)
ax2.xaxis.set_ticks(np.arange(0, 501, 100))
ax2.set_box_aspect(1/4)
ax2.invert_yaxis()

#plt.savefig(r"U:\BITCue\Projekter\TrackingFlowers\data\simulation/runmeanPlot.pdf", bbox_inches='tight')
plt.show()

### FRAME RATE ###

framerate = pd.read_csv(r"U:\BITCue\Projekter\TrackingFlowers\data\simulation/framerateExample.csv")

framerate['objectLetter'] = framerate['object'].map(lambda x: tran[x])

f, (ax1, ax2) = plt.subplots(2, 1, sharex=False, height_ratios=[4, 1])

ax1.set_xlim([0, 210])
ax1.set_ylim([0, 210])
ax2.margins(y = 0.2)

ax1.scatter(framerate["x_c"], framerate["y_c"], c = framerate['object'], s = 10)
ax1.set_box_aspect(1)
ax1.set_title('Frame rate')
ax2.scatter(framerate["frame"], framerate["objectLetter"], c = framerate['object'], s = 10)
ax2.xaxis.set_ticks(np.arange(0, 10001, 2000))
ax2.set_box_aspect(1/4)
ax2.invert_yaxis()

#plt.savefig(r"U:\BITCue\Projekter\TrackingFlowers\data\simulation/frameratePlot.pdf", bbox_inches='tight')
plt.show()


### All together now! ###

# figure, axis = plt.subplots(4, 2, height_ratios=[4, 1, 4, 1], width_ratios=[1, 1], figsize=(1,10))

# # Maxgap
# axis[0,0].scatter(maxgap["x_c"], maxgap["y_c"], c = maxgap['object'])
# axis[0,0].set_xlim([0, 1000])
# axis[0,0].set_ylim([0, 1000])
# axis[0,0].scatter(maxgap["x_c"], maxgap["y_c"], c = maxgap['object'])
# axis[0,0].set_box_aspect(1/2)
# axis[0,0].set_title('Max gap')

# axis[1,0].margins(y = 0.2, x = -0.4)
# axis[1,0].scatter(maxgap["frame"], maxgap["objectLetter"], c = maxgap['object'])
# axis[1,0].xaxis.set_ticks(np.arange(0, 10, 1))
# axis[1,0].set_box_aspect(1/8)
# axis[1,0].invert_yaxis()



# # Maxdist
# axis[2,0].scatter(maxdist["x_c"], maxdist["y_c"], c = maxdist['object'])
# axis[2,0].set_xlim([0, 1000])
# axis[2,0].set_ylim([0, 1000])
# axis[2,0].scatter(maxdist["x_c"], maxdist["y_c"], c = maxdist['object'])
# axis[2,0].set_box_aspect(1/2)
# axis[2,0].set_title('Max distance')

# axis[3,0].margins(y = 0.2)
# axis[3,0].scatter(maxdist["frame"], maxdist["objectLetter"], c = maxdist['object'])
# axis[3,0].xaxis.set_ticks(np.arange(0, 20, 2))
# axis[3,0].set_box_aspect(1/8)
# axis[3,0].invert_yaxis()

# arrowX = maxdist['x_c'][(maxdist['frame'] == max(maxdist['frame'][maxdist['object'] == min(maxdist['object'])]))]
# arrowY = maxdist['y_c'][(maxdist['frame'] == max(maxdist['frame'][maxdist['object'] == min(maxdist['object'])]))]
# arrowXend = maxdist['x_c'][(maxdist['frame'] == min(maxdist['frame'][maxdist['object'] == max(maxdist['object'])]))]
# arrowYend = maxdist['y_c'][(maxdist['frame'] == min(maxdist['frame'][maxdist['object'] == max(maxdist['object'])]))]

# axis[2,0].annotate("", xy = (arrowX,arrowY), xytext = (arrowXend, arrowYend), arrowprops=dict(arrowstyle="<->"))


# # Running mean

# axis[0,1].scatter(runmean["x_c"], runmean["y_c"], c = runmean['object'])
# axis[0,1].set_xlim([0, 1000])
# axis[0,1].set_ylim([0, 1000])
# axis[0,1].scatter(runmean["x_c"], runmean["y_c"], c = runmean['object'])
# axis[0,1].set_box_aspect(1/2)
# axis[0,1].set_title('Running mean')

# axis[1,1].margins(y = 0.2)
# axis[1,1].scatter(runmean["frame"], runmean["objectLetter"], c = runmean['object'])
# axis[1,1].xaxis.set_ticks(np.arange(0, 501, 100))
# axis[1,1].set_box_aspect(1/8)
# axis[1,1].invert_yaxis()


# # Frame rate
# axis[2,1].scatter(framerate["x_c"], framerate["y_c"], c = framerate['object'])
# axis[2,1].set_xlim([0, 210])
# axis[2,1].set_ylim([0, 210])
# axis[2,1].scatter(framerate["x_c"], framerate["y_c"], c = framerate['object'])
# axis[2,1].set_box_aspect(1/2)
# axis[2,1].set_title('Frame rate')

# axis[3,1].margins(y = 0.2)
# axis[3,1].scatter(framerate["frame"], framerate["objectLetter"], c = framerate['object'])
# axis[3,1].xaxis.set_ticks(np.arange(0, 10001, 2000))
# axis[3,1].set_box_aspect(1/8)
# axis[3,1].invert_yaxis()



# plt.show()