# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 15:30:13 2021

@author: au309263
"""

import streamlit as st
import pandas as pd
from code.track import tracker
from code.filtering import sieve
import time
import matplotlib.pyplot as plt
from PIL import Image



#image = Image.open('streamlit_logo.png')


import base64

LOGO_IMAGE = 'streamlit_logo.png'

st.markdown(
    """
    <style>
    .container {
        display: flex;
    }
    .logo-text {
        font-weight:600 !important;
        font-size:50px !important;
        color: #000000 !important;
        padding-top: 0px !important;
        paddinglleft: 90px;
    }
    .logo-img {
        float:right;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="container">
        <img class="logo-img" width = 50 height = 65 src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}" style="padding-top: 15px;">
        <p class="logo-text">Automatic Flower Tracking</p>
    </div>
    """,
    unsafe_allow_html=True
)


header = st.container()
dataset = st.empty()
plot1, plot2 = st.columns([6,6])
plot3, plot4 = st.columns([6,6])
results = st.container()



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
    
    with dataset.container():
        st.header("Uploaded data")
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
    st.sidebar.write('Contains ground truth track: Yes')
else:
    st.sidebar.write('Contains ground truth track: No')

st.sidebar.write(f'Running mean: {runMean}')
st.sidebar.write(f'Max disappeared: {maxDisap}')
st.sidebar.write(f'Max distance: {maxDist}')


# =============================================================================

st.sidebar.markdown("""<hr style="height:3px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

trackButton = st.sidebar.button('TRACK')
filterButton = st.sidebar.button('FILTER')
               
p = 0
    
if trackButton:    

    t = tracker(maxDisap, maxDist, runMean, "testWebapp.csv", frames, df1, False) # Initiate tracker

    starttime = time.time()
    for f in frames:
        t.track(f)
    endtime = time.time()  
    p = t.return_tracks_webapp() 
    #global p
    p = pd.DataFrame.from_records(p, columns=['frame', 'x_c', 'y_c', 'objectID']) 
    
    #dataset.empty()
    
    # with plot1:
    #     st.header("Uploaded data")
        
    #     fig0, ax0 = plt.subplots()
    #     ax0.scatter(x = df1['x_c'], y = df1['y_c'], s = 15)

    #     st.pyplot(fig0)
    
    
    with plot1:
        
        st.header("Tracking results")
    
        fig, ax = plt.subplots()
        ax.scatter(x = p['x_c'], y = p['y_c'], c = p['objectID'], s = 15)

        st.pyplot(fig)
        


        st.write(f'Tracking done. That took {round(endtime-starttime, 3)} seconds. That is {round((endtime-starttime)/len(frames), 3)} seconds per frame.')
        
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
        

if filterButton:
    t = tracker(maxDisap, maxDist, runMean, "testWebapp.csv", frames, df1, False) # Initiate tracker
    
    for f in frames:
        t.track(f)
    
    p = t.return_tracks_webapp() 
    #global p
    p = pd.DataFrame.from_records(p, columns=['frame', 'x_c', 'y_c', 'objectID']) 
    s = sieve(p)
    d,polyhulls = s.run()
    tracks_filtered = p[p['objectID'].isin(d)]
   
    
    with plot1:
        
        st.write("Tracking results")
    
        fig, ax = plt.subplots()
        ax.scatter(x = p['x_c'], y = p['y_c'], c = p['objectID'], s = 15)

        st.pyplot(fig)
        
        st.write(p)

        @st.cache
        def convert_df(df):
            return df.to_csv().encode('utf-8')


        csv = convert_df(p)

        st.download_button(
           "Press to download result",
           csv,
           "file.csv",
           "tracked/csv",
           key='download-csv'
           )
        
    with plot2:
        st.write("Filtered results")

        fig, ax2 = plt.subplots()
        ax2.scatter(x = tracks_filtered['x_c'], y = tracks_filtered['y_c'], c = tracks_filtered['objectID'], s = 15)

        st.pyplot(fig)
        
        st.write(p)

        @st.cache
        def convert_df(df):
            return df.to_csv().encode('utf-8')


        csv = convert_df(tracks_filtered)

        st.download_button(
           "Press to download results",
           csv,
           "tracked_and_filtered.csv",
           "text/csv",
           key='download-csv'
           )




    
    
    
    
    
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            #header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
        
    #     fig, ax2 = plt.subplots()
    #     ax2.scatter(x = tracks_filtered['x_c'], y = tracks_filtered['y_c'], c = tracks_filtered['objectID'], s = 15)
    
    #     st.pyplot(fig)