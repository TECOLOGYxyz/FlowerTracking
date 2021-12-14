# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 15:30:13 2021

@author: au309263
"""

import streamlit as st
import pandas as pd
from code.track import tracker
import time
import matplotlib.pyplot as plt


header = st.container()
dataset = st.container()
results = st.container()
blabla = st.container()


with header:
    st.title("Automatic Flower Tracking")
#    st.header("What")



# with header:
#     st.header("How?")


st.sidebar.title("Upload data")

uploaded_file = st.sidebar.file_uploader('Choose a file')
if uploaded_file is not None:    
    df1=pd.read_csv(uploaded_file)
    
    
    df1['frame'] = df1['filename'].str.extract('(\d{6})')
    df1['x_c'] = (df1['x_min'] + df1['x_max']) / 2
    df1['y_c'] = (df1['y_min'] + df1['y_max']) / 2
    df1['frame'] = df1['frame'].astype('int')

    frames = list(set(df1['frame'].tolist()))
    frames = sorted([int(i) for i in frames])
    
    
    fig0, ax0 = plt.subplots()
    ax0.scatter(x = df1['x_c'], y = df1['y_c'], s = 15)

    st.pyplot(fig0)
    
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
     'Set number of frames for max disappeared',
     options=range(0,100), key = "maxDisap")

maxDist = st.sidebar.select_slider(
     'Set number of frames for max distance',
     options=range(0,5000), key = "maxDist")


st.sidebar.markdown("""<hr style="height:3px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

if gt_choice == 'Yes':
    st.sidebar.write('Data contain ground truth tracks')
else:
    st.sidebar.write('Data does not contain ground truth tracks')

st.sidebar.write(f'Running mean: {runMean}')
st.sidebar.write(f'Max disappeared: {maxDisap}')
st.sidebar.write(f'Max distance: {maxDist}')


# =============================================================================

st.sidebar.markdown("""<hr style="height:3px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

trackButton = st.sidebar.button('TRACK')


                    
if trackButton:    

    t = tracker(maxDisap, maxDist, runMean, "testWebapp.csv", frames, df1, False) # Initiate tracker

    starttime = time.time()
    for f in frames:
        t.track(f)
        
    p = t.return_tracks_webapp()
    
    p = pd.DataFrame.from_records(p, columns=['frame', 'x_c', 'y_c', 'objectID']) 
    
    fig, ax = plt.subplots()
    ax.scatter(x = p['x_c'], y = p['y_c'], c = p['objectID'], s = 15)

    st.pyplot(fig)

    st.write(p)

    


    @st.cache
    def convert_df(df):
        return df.to_csv().encode('utf-8')


    csv = convert_df(p)

    st.download_button(
        "Press to download tracking results",
        csv,
        "file.csv",
        "text/csv",
        key='download-csv'
        )


    endtime = time.time()
    print(f'Tracking done. That took {round(endtime-starttime, 3)} seconds. That is {round((endtime-starttime)/len(frames), 3)} seconds per frame.')
        #t.write_tracks_file()
    
    with results:
        st.title("Results")
        st.write(f'Tracking done. That took {round(endtime-starttime, 3)} seconds. That is {round((endtime-starttime)/len(frames), 3)} seconds per frame.')

