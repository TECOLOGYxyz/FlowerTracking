# # -*- coding: utf-8 -*-
# """
# Created on Thu Nov  7 11:07:43 2019

# @author: Hjalte Mann

# This script stitches images in a folder together to a time-lapse video
# """

from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import pandas as pd


#df = pd.read_csv(r"U:\BITCue\Projekter\TrackingFlowers\data\annotations\2020_04_30_NorwayAnnotations_NARS-13_IndividualAnnotations_FRCNN_Metrics.csv")
#df = pd.read_csv(r'../testResults/_parameterTest_NYAA-04_3/parameterTest_NYAA-04_maxDisap_10_runMean_60_maxDist_300.csv')
gt = pd.read_csv(r'../data\annotations\2021_12_13_NorwayAnnotations_NYAA-04_IndividualAnnotations_FRCNN_Metrics.csv')

df2 = pd.read_csv(r'../testResults/_parameterTest_NYAA-04_3/parameterTest_NYAA-04_maxDisap_0_runMean_0_maxDist_0.csv')
df3 = pd.read_csv(r'../testResults/filtered4_NYAA-04_maxDisap_0_runMean_0_maxDist_0.csv')



#m = pd.merge(df, gt, on = ['filename', 'x_min', 'x_max', 'y_min', 'y_max'], how = 'inner')
m2 = pd.merge(df2, gt, on = ['filename', 'x_min', 'x_max', 'y_min', 'y_max'], how = 'inner')
m3 = pd.merge(df3, gt, on = ['filename', 'x_min', 'x_max', 'y_min', 'y_max'], how = 'inner')
#m4 = pd.merge(df4, gt, on = ['filename', 'x_min', 'x_max', 'y_min', 'y_max'], how = 'inner')


#plt.scatter(m['frame'], m['id_gt'], c = m['objectID'], s = 15)
#plt.show()

plt.scatter(df2['x_c'], df2['y_c'], c = df2['objectID'], s = 15)
plt.show()

plt.scatter(df3['x_c'], df3['y_c'], c = df3['objectID'], s = 15)
plt.show()



m2Grouped = m2.groupby(['id_gt'])
colour = []
l = 0
d = OrderedDict()

for i, g in m2Grouped: # Create dictionary with most common objectID for each id_gt
    f = g.iloc[0]['id_gt']
    v = g['objectID'].value_counts()[:1].index.tolist()[0]
    d[f] = v

for i,r in m2.iterrows():
    oid = r['objectID'] 
    f = r['id_gt']
    
    most_common = d[f]
    #print(most_common)
    
    if oid != most_common:
        print(f'{oid} is not {most_common}')
        #print(type(oid))
        #print(type(most_common))
        colour.append(0)
        l += 1
    else:
        colour.append(1)

m2['colour'] = colour
m2.to_csv("hello2.csv")
print(l)

fig, ax0 = plt.subplots(figsize=(15,10))
scat0 = ax0.scatter(m2['frame'], m2['id_gt'], c = m2['colour'], s = 40)


# plt.scatter(m2['frame'], m2['id_gt'], c = m2['objectID'], s = 15)
# plt.show()

#####
m3Grouped = m3.groupby(['id_gt'])
colour = []
l = 0
d = OrderedDict()

for i, g in m3Grouped: # Create dictionary with most common objectID for each id_gt
    f = g.iloc[0]['id_gt']
    v = g['objectID'].value_counts()[:1].index.tolist()[0]
    d[f] = v

for i,r in m3.iterrows():
    oid = r['objectID'] 
    f = r['id_gt']
    
    most_common = d[f]
    #print(most_common)
    
    if oid != most_common:
        print(f'{oid} is not {most_common}')
        #print(type(oid))
        #print(type(most_common))
        colour.append(0)
        l += 1
    else:
        colour.append(1)
        

m3['colour'] = colour
#m3.to_csv("hello2.csv")
print(l)

fig, ax1 = plt.subplots(figsize=(15,10))
scat1 = ax1.scatter(m3['frame'], m3['id_gt'], c = m3['colour'], s = 40)


fig, ax1 = plt.subplots(figsize=(15,10))
scat1 = ax1.scatter(m3['frame'], m3['objectID'], c = m3['colour'], s = 40)



####

# m4Grouped = m4.groupby(['id_gt'])
# colour = []
# l = 0
# d = OrderedDict()

# for i, g in m4Grouped: # Create dictionary with most common objectID for each id_gt
#     f = g.iloc[0]['id_gt']
#     v = g['objectID'].value_counts()[:1].index.tolist()[0]
#     d[f] = v

# for i,r in m4.iterrows():
#     oid = r['objectID'] 
#     f = r['id_gt']
    
#     most_common = d[f]
#     #print(most_common)
    
#     if oid != most_common:
#         print(f'{oid} is not {most_common}')
#         #print(type(oid))
#         #print(type(most_common))
#         colour.append(0)
#         l += 1
#     else:
#         colour.append(1)

# m4['colour'] = colour
# #m3.to_csv("hello2.csv")
# print(l)

# fig, ax2 = plt.subplots(figsize=(15,10))
# scat2 = ax2.scatter(m4['frame'], m4['id_gt'], c = m4['colour'], s = 40)


#scat0.axes.get_yaxis().set_visible(False)

# for i, g in m2Grouped:
#     print(g)
#     v = g['objectID'].value_counts()[:1].index.tolist()[0]
#     print(f'Most common: {v}')
#     for i,r in g.iterrows():
#         oid = r['objectID']
#         #print(oid)
#         if oid != v:
#             colour.append("0")
#             i += 1
#             #print(f'{oid} is not {v}')
#         else:
#             #print(f'{oid} is {v}')
#             colour.append("1")
            
#             #print(r)
#             #break
# print(i)            
#m2['colour'] = colour
#print(m2)

# m2.to_csv("hello.csv")

#fig, ax0 = plt.subplots(figsize=(15,10))
#scat0 = ax0.scatter(m2['frame'], m2['id_gt'], c = m2['colour'], s = 40)
#scat0.axes.get_yaxis().set_visible(False)
# scat0.show()




#df['frame'] = df['filename'].str.extract('(\d{6})')

#df['x_c'] = (df['x_min'] + df['x_max']) / 2
#df['y_c'] = (df['y_min'] + df['y_max']) / 2

#df['frame'] = df['frame'].astype('int')


# dfGrouped = df.groupby(['frame'])

# frames = list(set(df['frame'].tolist()))

# points = []

# for i,group in dfGrouped:
#         xs = []
#         ys= []
#         for i,line in group.iterrows():
#             x = line['x_c']
#             y = line['y_c']
#             xs.append(x)
#             ys.append(y)
#         points.append([xs,ys])


# # Use matplotlib ggplot stylesheet if available
# try:
#     plt.style.use('ggplot')
# except:
#     pass

#print(points)


#####


# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation

# x = np.linspace(0, 10, 100)
# y = np.sin(x)

# fig, ax = plt.subplots()
# line, = ax.plot(x, y, color='k')

# def update(num, x, y, line):
#     line.set_data(x[:num], y[:num])
#     line.axes.axis([0, 10, 0, 1])
#     return line,

# ani = animation.FuncAnimation(fig, update, len(x), fargs=[x, y, line],
#                               interval=25, blit=True)
# ani.save('test.gif')
# plt.show()


####


# x = np.array(points[0][0])
# y = np.array(points[0][1]) 

# t = np.array(range(len(frames)))

# # Set up the figure and axis
# fig, ax = plt.subplots(figsize=(30, 16))

# time_text = ax.text(0.10, 1.1, '', transform=ax.transAxes)

# # ----------------------------------------------------------------------------

# ax.set(xlim=(0, 6080), ylim=(0, 3420))
# scat2 = ax.scatter(-1,1, s = 100)
# scat = ax.scatter(x,y, s = 202)


# for i,c in enumerate(x):
#     line, = ax.plot(x[i],y[i])

# time_text.set_text('')
    
# def animate(i):
#     print(i)
#     # Must pass scat.set_offsets an N x 2 array
#     x_i = np.array(points[i][0])
#     y_i = np.array(points[i][1])
    
#     x_i_pre = np.array(points[i-1][0])
#     y_i_pre = np.array(points[i-1][1])
    
#     #x_i_prepre = np.array(points[i-2][0])
#     #y_i_prepre = np.array(points[i-2][1])
#     scat2.set_offsets(np.c_[x_i_pre, y_i_pre])
#     scat.set_offsets(np.c_[x_i, y_i])
    
#     #scat2.set_offsets(np.c_[x_i_pre, y_i_pre])
#     #line.set_data(x_i[:i][0], y_i[:i][1])
#     #line.set_data(300, 500)
#     time_text.set_text(f'Frame {t[i]}')
#    # for i,c in enumerate(x_i):
#     #    line.set_data = ax.plot(x_i[i],y_i[i])
    


# # ----------------------------------------------------------------------------
# # Save the animation
# #anim = FuncAnimation(fig, animate, interval=100, frames=len(frames)-1, repeat=False)
# #fig.show()
# print("Saving")

# #anim.save('../testResults/' + 'scatter' + '.gif',dpi = 80, writer=PillowWriter(fps=5))


