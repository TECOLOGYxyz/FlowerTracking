---
new_session: FALSE
title: |
  **Monitoring the phenology of individual flowers using deep learning and automatic tracking**
author:
- Hjalte M. R. Mann
- Alexandros Iosifidis
- Toke T. Høye
date: "november 30, 2021"
output:
  word_document: default
  pdf_document:
    fig_caption: yes
    keep_tex: yes
    latex_engine: pdflatex
  html_document:
    df_print: paged
fontfamily: mathpazo
fontsize: 12pt
geometry: margin = 1in
header-includes:
- \usepackage{setspace}\doublespacing
- \usepackage[left]{lineno}
- \linenumbers
- \usepackage{dcolumn}
- \usepackage{caption}
- \usepackage{float}
- \usepackage{afterpage}
- \usepackage{siunitx}
- \usepackage{amsmath}
keywords: Citizen science, Arctic, insects
bibliography: ./library.bib
csl: ./journal-of-ecology.csl
abstract: ABSTRACT | Often simple variables will be used to describe the flowering phenology of a population of plants, e.g. onset or peak of flowering and to infer respones to climate change. Here we show that image-based monitoring of field plots at very high temporal resolution can return information on flowering phenology at the level of indiviuals. Further, we present an automatic flower tracking algorithm.
---






\newpage
**NOTES**

What questions do we want to answer?

*Flower information*



\pagebreak



# Introduction

The flowering phenology of a population may mask responses at the individual level. For example, 

Does flower visitation rates and/or reproductive success depend on the timing of flowering for the indiviual flower?




# Material and methods

## Study site



## The image series

## Flower annotations




We built a framework for tracking, filtering, and evaluating tracking of objects in time-lapse image series.

# Automatic tracking

Our algorithm tracks objects based on distances between centroids of bounding boxes. 

The tracking algorithm has a set of user adjusted parameters that can optimise tracking accuracy.

The parameters are particularly relevant for optimal tracking of objects that are constrained to a specific area such as flowers.

It is important to note, however, that the tracking algorithm can be used to track any objects.

The tracking algorithm can be applied both offline (on a set of detections/annotations that have already been produced) or online (realtime tracking frame per frame).


### User parameters

**Max distance threshold**, **running mean**, **max disappeared**, 


As the wind shifts, the flower heads changes direction. This can happen instantaneously (i.e. between two censecutive frames). As they are constrained by their stalk, there is a limit to the distance they can move.

Establishing associations between points based on just the distance between points in the current and the previous frame can cause errors when flowers are in close vicinity of each other.

The flowers move around a center point because of their stalk. We base the tracking on the distance between a point in the current frame and the running mean of the positions of the previous X points in a track.







# Evaluating tracking perfomance

Mota counts shifts in tracking.

To derive flowering length, in theory we just need to track the most extreme points correctly and don't care about other points (although we filter by length when overlap).

To associate other information to the flower, for example flower visits, we want as much as possible of the track to be correct.


## Filtering tracks

Tracks that overlap have significant risk of errors. Overlapping tracks can be caused by a single flower that was erroneously assigned to several tracks, two flowers that were located sufficiently close to each other that there areas overlapped (e.g. when wind moves the flowers around), false positive detections close to a flower.Best case is two flowers that flowered in the same area but were separated by time. Here we will remove overlapping tracks to reduce the risk of error.

We remove tracks consisting on only one or two points. For tracks consisting of three points, we establish the triangle from the points.

For tracks consisting of more than three points, we calculate the convex hull of all the points included in the track. 
Second, we check for overlap between all pairs of polygons made from the vertices of each convex hull. If the polygons for two tracks overlap, we'll filter out both/the shortest??






# Results



![](../figures/figure_1.png){ width=100% }
**Figure 1:** Figure text....



# Discussion

## Flower phenology



# Acknowledgements



# Data availability

The code that supports the results in this paper will be made openly available at https://github.com/TECOLOGYxyz. Raw data as well as the trained flower detection model will be archived on https://zenodo.org/.






