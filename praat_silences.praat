#reads several files and extracts all sileneces
#saves silences in text file (one for each recording)

#specify the path where the audio files are stored. Audio files need to be .wav files! 
dir$ = myDirectory 
#create a list with all audio files for batch import
strings = Create Strings as file list: "list", dir$ +"/*.wav"
numberOfFiles = Get number of strings

#load all files from myDirectory
for file from 1 to numberOfFiles
 selectObject: strings
 fileName$ = Get string: file
 Read from file: dir$+"/"+fileName$
 sound$ = selected$("Sound", 1)
 #praat calculates the intensity. The first argument corresponds to the minimum pitch that praat should expect. For male voices, a lower pitch may be more adequate.
 #The second argument corresponds to the time window that praat will use for the calculation. 
 #The minimum duration depends also on the pitch: lower pitch requires longer time windows (hertz is the number of waves per second). The minimum for 100 hz is 32 ms.
 #Praat adapts the time window if necessary to the minimum time window.
 #"yes" refers to the question "substract mean?" which allows you to substract constant noise from the mic.
 To Intensity: 100, 0.03, "yes"
 Rename: "intensity"
 #-25 corresponds to the threshold: praat calculates the maximum intensity and substracts the threshold value. All sounds with an intensity below the threshold will be identified as "silent".
 #0.5 corresponds to the minimum duration for a silent segment in seconds (0.5=500 ms). Very short pauses around 100ms-150ms may be caused by plosives. 
 #0.05 corresponds to the minimum duration of a sounding segment. You may increase the value in order to avoid capturing mouse clicks or keypresses or other technical noises.
 #The last two arguments are the text lables: "silent" for all silent segments, "sounding" for all sounding segments.
 textgrid=To TextGrid (silences): -25, 0.5, 0.05, "silent", "sounding"

 #headings for silence file. I usually save relevant variables in the filename. 
 writeFileLine: "silences_"+fileName$+".txt", "recording", tab$, "intervalNumber", tab$, "text", tab$, "startTs", tab$, "endTs", newline$
 #looping through intervals
 numberOfIntervals = Get number of intervals: 1
 for intervalNumber from 1 to numberOfIntervals
  #selectObject: textgrid
  startTs = Get start point: 1, intervalNumber
  endTs = Get end point: 1, intervalNumber
  text$ = Get label of interval: 1, intervalNumber
  appendFile: "silences_"+fileName$+".txt", fileName$, tab$, intervalNumber, tab$, text$, tab$, startTs, tab$, endTs, newline$
 endfor

 removeObject: textgrid

endfor









