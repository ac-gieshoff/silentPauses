# -*- coding: utf-8 -*-
"""

description: Python script to convert audio or video files into another format and to cut audiofiles or videofiles based on timestamps indicated in a table. 
Ressources: https://zulko.github.io/moviepy/ref/ffmpeg.html
Caution: I have not tried all audio and video extensions yet. mp3, wav, mp4 worked fine; mkv, flv and avi did not.

"""

#import modules
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import pandas as pd

#for video files, specify the frame rate
fps= 25
#import table. Replace "myTable.xlsx" with the full path to your table. You can specify the name of the sheet if necessary. 
#The argument "converters" allows you to specify the correct format for certain columns if necessary.
#myTable has a column "path" specifying the path were the audio or video is stored, 
#"id" which you can use to create a meaningful filename your your new file (in my case "id" corresponded to the name of the parent directory), 
#"segment" which is the name you would like to give to the segment you extract (optional)
#"startTs" : time indicated as HH:MM:SS.ssss, extract from here 
#endTs: time indicated as HH:MM:SS.ssss, extract up to here
tabelle = pd.read_excel(r"myTable.xlsx", 
                        sheet_name="mySheet", converters={"path":str, "id":str})

#The main idea is to loop through the table, load the audio or video file, 
#cut it according to the time indicated in the table and save is in the same or another format in a new directory. Converting to .wav can be useful to work in praat.
#cutting can be useful if your video or audio file contains more than the part you are interested in.

#loop through tabelle, retrieve path
for index, row in tabelle.iterrows():
    print(index)
    id = row["id"]
    
#retrieve path
    path = row["path"]#needs to be defined as string
#if "path" is not indicated in the table, skip the row
    if pd.isna(path):
        print("no path indicated. check table")
    elif id not in path:
        print("id is not in path. check table")
    else:
 #get name of the segment
        segment = row["segment"]
        segment = str(segment)
    
 #specify the name for the output file
#retrieve last element of "path" (result: myTable.xlsx; in my case the path was indicated as follows: "Desktop:\\id\\myTable.xlsx")
        name = path.split("\\")[-1]
  #retrieve first element (=myTable)
        name = name.split(".")[0]
    #specify the full path for the output file. You can change the format by changing the extension, i.e. you can convert mp3 for instance in wav (convenient for praat).
        out_name = "nameOfOutputFolder" +  name + segment + ".mp4" 
        
     
#define start and endpoint for cutting: can be extracted from table. We want to convert the time points in seconds

#extract the start time from the table. 
        start = row["startTs"]
        #split string and extract last part.
       #sec also contains the milliseconds
        sec = float(start.split(":")[-1])
        minute = int(start.split(":")[-2])
        #multiply the minutes by 60 (to obtain seconds)and add everything
        t1 = minute * 60 +sec
        
        #same procedure
        end = row["endTs"]
        sec = float(end.split(":")[-1])
        minute = int(end.split(":")[-2])
        t2 = minute * 60 +sec

#cut video or audio file
        ffmpeg_extract_subclip(path, t1, t2, targetname = out_name)
        print("done")

print("stop")




