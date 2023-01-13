from matplotlib.markers import MarkerStyle
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.transforms import Affine2D
from matplotlib.markers import JoinStyle, CapStyle

import matplotlib.path as mpath
import numpy as np


# marker_inner = dict(markersize=35,
#                     markerfacecolor='tab:blue',
#                     markerfacecoloralt='lightsteelblue',
#                     markeredgecolor='brown',
#                     markeredgewidth=8,
#                     )

# text_style = dict(horizontalalignment='right', verticalalignment='center',
#                   fontsize=12, fontfamily='monospace')
# marker_style = dict(linestyle=':', color='0.8', markersize=50,
#                     markerfacecolor="yellow", markeredgecolor="black", transform = Affine2D().rotate_deg(90) )


# def format_axes(ax):
#     ax.margins(0.2)
#     ax.set_axis_off()
#     ax.invert_yaxis()




# star = mpath.Path.unit_regular_star(8)
# circle = mpath.Path.unit_circle()
# # concatenate the circle with an internal cutout of the star
# cut_star = mpath.Path(
#     vertices=np.concatenate([circle.vertices, star.vertices[::-1, ...]]),
#     codes=np.concatenate([circle.codes, star.codes]))

# fig, ax = plt.subplots()
# #fig.suptitle('Path markers', fontsize=14)
# #fig.subplots_adjust(left=0.4)

# markers = {'star': star}

# # for y, (name, marker) in enumerate(markers.items()):
# #     print("y", y)
# #     print("name ", name)
# #     print("marker", marker)
# #ax.text(-0.5, 0, 'star', **text_style)
# ax.plot([0] * 1, marker=star, **marker_style)
# format_axes(ax)

# plt.show()


# theta = np.linspace(-1000*np.pi, 1000*np.pi, 20000)

# k = 4 #11/3

# x = np.cos(k*theta)*np.sin(theta)
# y = np.cos(k*theta)*np.cos(theta)

# fig = plt.figure()
# plt.rcParams['figure.figsize']=[6,6]

# plt.fill(x, y, edgecolor = None, facecolor = 'grey', alpha = 0.5)
# plt.show()

# theta = np.linspace(-5*np.pi, 5*np.pi, 1000)
# k = 20 #11/3

# x = np.cos(k*theta)*np.sin(theta)
# y = np.cos(k*theta)*np.cos(theta)

# #fig = plt.figure()
# #plt.rcParams['figure.figsize']=[6,6]

# plt.fill(x/10, y/10, edgecolor = None, facecolor = 'orange', alpha = 0.5)
# plt.show()


# import turtle
# from svg_turtle import SvgTurtle


# #t = turtle.Turtle()
# t = SvgTurtle(1000, 1000)
# s = turtle.Screen()
# s.bgcolor('black')
# t.speed(0)

# for i in range(17):
#     t.color('#850080')
#     t.begin_fill()
#     t.circle(190-i,90)
#     t.left(98)
#     t.end_fill()

#     t.color('#E400DC')
#     t.begin_fill()
#     t.circle(190-i, 90)
#     t.left(18)
#     t.end_fill()

# t.save_as('petals_purple.svg')


# #t = turtle.Turtle()
# t = SvgTurtle(1000, 1000)
# s = turtle.Screen()
# s.bgcolor('black')
# t.speed(0)

# n = 45
# angle = 180 - 180 / n
# for i in range(n):
#     t.color('yellow')
#     t.begin_fill()
#     t.forward(100)
#     t.right(angle)

# t.save_as('center.svg')



# ### FRAMES ###
fig, axes = plt.subplots(5, 1, sharex=False)
ax1, ax2, ax3, ax4, ax5 = axes.flatten()


# # # Frame 1
frame1_x = [50, 235, 243]
frame1_y = [150,125, 40]
frame1_z = [1,5,2]

ax1.scatter(frame1_x, frame1_y, s = 1)
ax1.set_xlim([0, 300])
ax1.set_ylim([0, 200])
ax1.set_box_aspect(2/3)
ax1.axes.get_yaxis().set_visible(False)
ax1.axes.get_xaxis().set_visible(False)

# # # Frame 2
frame2_x = [65,30, 255]
frame2_y = [165,34, 126]
frame2_z = [1,3,5]

ax2.scatter(frame2_x, frame2_y, s = 1)
#ax2.set_title('Frame 2', loc = "left")
ax2.set_xlim([0, 300])
ax2.set_ylim([0, 200])
ax2.set_box_aspect(2/3)
ax2.axes.get_yaxis().set_visible(False)
ax2.axes.get_xaxis().set_visible(False)

# # # Frame 3

frame3_x = [30,45,229, 265]
frame3_y = [145,54, 110, 46]
frame3_z = [1,3,5,2]

ax3.scatter(frame3_x, frame3_y, s = 1)
ax3.set_xlim([0, 300])
ax3.set_ylim([0, 200])
ax3.set_box_aspect(2/3)
ax3.axes.get_yaxis().set_visible(False)
ax3.axes.get_xaxis().set_visible(False)

# # # Frame 4
frame4_x = [66,132, 17,275]
frame4_y = [144,101,17, 30]
frame4_z = [1,4,3,2]

ax4.scatter(frame4_x, frame4_y, s = 1)
ax4.set_xlim([0, 300])
ax4.set_ylim([0, 200])
ax4.set_box_aspect(2/3)
ax4.axes.get_yaxis().set_visible(False)
ax4.axes.get_xaxis().set_visible(False)


# # # Frame 5
frame5_x = [29,125, 219]
frame5_y = [166,83, 122]
frame5_z = [1,4, 5]

ax5.scatter(frame5_x, frame5_y, s = 1)
ax5.set_xlim([0, 300])
ax5.set_ylim([0, 200])
ax5.set_box_aspect(2/3)
ax5.axes.get_yaxis().set_visible(False)
ax5.axes.get_xaxis().set_visible(False)


# # # Frame 6
# frame6_x = [50, 253]
# frame6_y = [150, 29]
# frame6_z = [1,2]

# ax6.scatter(frame6_x, frame6_y, s = 1)
# ax6.set_xlim([0, 300])
# ax6.set_ylim([0, 200])
# ax6.set_box_aspect(2/3)
# ax6.axes.get_yaxis().set_visible(False)
# ax6.axes.get_xaxis().set_visible(False)


# plt.subplots_adjust(wspace=0, hspace=0.06)
# plt.margins(y = 0.1)
# plt.savefig("frames.svg", bbox_inches='tight', pad_inches=0.01)
plt.show()




colors=["#FF4F00", "#0040A9", "#000000", "#008507", "#850080"]

fig, axFull = plt.subplots(1, 1, sharex=False)

xs = frame1_x + frame2_x + frame3_x + frame4_x + frame5_x 
ys = frame1_y + frame2_y + frame3_y + frame4_y + frame5_y 
zs = frame1_z + frame2_z + frame3_z + frame4_z + frame5_z 

coly = [colors[i-1] for i in zs]

axFull.scatter(xs, ys, s = 80, c = coly)

axFull.set_xlim([0, 300])
axFull.set_ylim([0, 200])
axFull.set_box_aspect(2/3)
#axFull.axes.get_yaxis().set_visible(False)
#axFull.axes.get_xaxis().set_visible(False)
axFull.set_xticks([])
axFull.set_yticks([])
axFull.set_ylabel('Y', labelpad=-0.5)
axFull.set_xlabel('X', labelpad=-0.5)
# plt.savefig("sum.svg", bbox_inches='tight', pad_inches=0.01)
plt.show()



colors=["#FF4F00", "#0040A9", "#000000", "#008507", "#850080"]

fig, axFrames = plt.subplots(1, 1, sharex=False)
axFrames.set_yticks([1,2,3,4,5], minor=False)
axFrames.set_xticks([1,2,3,4,5], minor=False)
plt.grid(visible=None, which='both', axis='y')
axFrames.set_axisbelow(True)
on = frame1_z + frame2_z + frame3_z + frame4_z + frame5_z
print("ON ", on)
#fn = [1,1,2,2,2,2,3,3,3,3,3,4,4,4,5,5]
fn = [1]*len(frame1_z) + [2]*len(frame2_z) +[3]*len(frame3_z) + [4]*len(frame4_z) + [5]*len(frame5_z)
print(fn)

letters = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e"}

coly = [colors[i-1] for i in zs]

axFrames.scatter(fn, on, s = 80, c = coly)

#axFrames.set_xlim([0, 300])
#axFrames.set_ylim([0, 200])
axFrames.set_box_aspect(1.431/3)
#axFrames.axes.get_yaxis().set_visible(False)
#axFrames.axes.get_xaxis().set_visible(False)
axFrames.invert_yaxis()
axFrames.set_ylabel('Flower', labelpad=-0.5)
axFrames.set_xlabel('Frame', labelpad=-0.5)
plt.margins(y = 0.2)
letterOn = [letters[i] for i in on]
plt.yticks(on, letterOn)
plt.savefig("time.svg", bbox_inches='tight', pad_inches=0.01)
plt.show()

