# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 15:30:13 2021

@author: au309263
"""

import streamlit as st
import pandas as pd
from track import tracker
import time



header = st.container()
dataset = st.container()
features = st.container()
blabla = st.container()


with header:
    st.title("Automatic Flower Tracking")
    st.header("What")



with header:
    st.header("How?")


st.sidebar.title("Upload data")

uploaded_file = st.sidebar.file_uploader('Choose a file')


st.sidebar.markdown("""<hr style="height:3px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)



st.sidebar.title("Set parameters")

gt_choice = st.sidebar.radio(
     "Data contains ground truth track",
     ('No', 'Yes'))

if gt_choice == 'Yes':
    st.sidebar.write('Your data should contain a column named "id_gt" with IDs for ground truth tracks.')
else:
    st.sidebar.write("You'll run your data without tracking performance evaluation")

st.sidebar.markdown("""<hr style="height:3px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

runMean = st.sidebar.select_slider(
     'Set number of frames for running mean',
     options=range(0,100), key = "runMean")

maxDisap = st.sidebar.select_slider(
     'Set number of frames for running mean',
     options=range(0,100), key = "maxDisap")

maxDist = st.sidebar.select_slider(
     'Set number of frames for running mean',
     options=range(0,5000), key = "maxDist")


st.sidebar.markdown("""<hr style="height:3px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

if gt_choice == 'Yes':
    st.sidebar.write('Data contain ground truth tracks')
else:
    st.sidebar.write('Data does not contain ground truth tracks')

st.sidebar.write(f'Running mean: {runMean}')
st.sidebar.write(f'Running mean: {runMean}')
st.sidebar.write(f'Max disappeared: {maxDisap}')
st.sidebar.write(f'Max distance: {maxDist}')


# =============================================================================

if uploaded_file is not None:
    df1=pd.read_csv(uploaded_file)
    df1['frame'] = df1['filename'].str.extract('(\d{6})')
    df1['x_c'] = (df1['x_min'] + df1['x_max']) / 2
    df1['y_c'] = (df1['y_min'] + df1['y_max']) / 2
    df1['frame'] = df1['frame'].astype('int')

    frames = list(set(df1['frame'].tolist()))
    frames = sorted([int(i) for i in frames])


    t = tracker(maxDisap, maxDist, runMean, "testWebapp.csv", frames) # Initiate tracker

    starttime = time.time()
    for f in frames:
        t.track(f)
        endtime = time.time()
        print(f'Tracking done. That took {round(endtime-starttime, 3)} seconds. That is {round((endtime-starttime)/len(frames), 3)} seconds per frame.')
        #t.write_tracks_file()
