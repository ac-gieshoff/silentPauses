# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 12:29:53 2021

@author: gies
descriptin: cuts videos based on timepoints in table, attention: does not work with mkv
"""

#import modules
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import pandas as pd
#import datetime


#define frame rate for the video (useful for calculation later)
fps= 25
#import table. Change path accoridngly
tabelle = pd.read_excel(r"S:\\pools\l\L-IUED-CLINT-admin\07-Vorgehen Datenbearbeitung\ELF Dense Spots\Test_Datenbearbeitung\Python_EdE\EdE_DS_5_Vorlage_Script_Zuschneiden.xlsx", 
                        sheet_name="EdE_DS_5", converters={"path":str, "participant":str})

#if path does not contain participant name, skip
#retrieve start and end point

#loop through tabelle, retrieve path
for index, row in tabelle.iterrows():
    print(index)
    participant = row["participant"]
    
#retrieve path
    path = row["filename"]#needs to be defined as string
#if empty, skip
    if pd.isna(path):
        print("no path indicated. check table")
    elif participant not in path:
        print("participant name is not in path. check table")
    else:
        #get dense spot
        densespot = row["DS"]
        densespot = str(densespot)
#name = os.path.splitext(name)[0]
        name = path.split("\\")[-1]
        name = name.split(".")[0]
        out_name = "S:\\pools\\l\\L-IUED-CLINT-analysis\\densespots\\videos\\" +  name + "_startST_endTT_DS_" + densespot + ".mp4" 
        
     
#define start and endpoint for cutting: can be extracted from table. We want to convert the time points in seconds
#fps in webcam-videos is 25
#extract the start time from the table. It comes as a string.
        start = row["start_at"]
        #split string and extract last part.Convert to integer, multiply by frame rate (milliseconds) and divide by 1000 (1 second=1000ms)
        #ms = int(start.split(".")[-1])*fps/1000
        sec = float(start.split(":")[-1])
        minute = int(start.split(":")[-2])
        #multiply the minutes by 60 (to obtain seconds)and add everything
        #t1 = minute*60+sec+ms
        t1 = minute * 60 +sec
        
        #same procedure
        end = row["end_zt"]
        #ms = int(end.split(".")[-1])*fps/1000
        sec = float(end.split(":")[-1])
        minute = int(end.split(":")[-2])
        #t2 = minute*60+sec+ms
        t2 = minute * 60 +sec

#cuts video
        ffmpeg_extract_subclip(path, t1, t2, targetname = out_name)
        print("done")

print("stop")




