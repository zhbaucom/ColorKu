from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import cv2
from tkinter import Tk    # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
exec(open("C:/Users/zachb/Documents/Python4fun/colorKu/py/boardLocater.py").read())


mypath = 'C:/Users/zachb/Documents/Python4fun/colorKu/images/boardTrainRaw3'
outpath = 'C:/Users/zachb/Documents/Python4fun/colorKu/images/boardTrain'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
newnames = ['' for z in np.arange(0,len(onlyfiles))]

# newnames[0:12] = ["B" + "1" + "_R" + y+ "_O" + x for y in ['1', '9', '8'] for x in ["1", "2" ,"3", "4"]]
# newnames[12:16] = ["B" + "1" + "_R" + 'E'+ "_O" + x  for x in ["1", "2" ,"3", "4"]]
# newnames[16:28] = ["B" + "2" + "_R" + y+ "_O" + x for y in ['7', '6', '5'] for x in ["1", "2" ,"3", "4"]]
# newnames[28:32] = ["B" + "2" + "_R" + 'E'+ "_O" + x  for x in ["1", "2" ,"3", "4"]]
# newnames[32:44] = ["B" + "3" + "_R" + y+ "_O" + x for y in ['4', '3', '2'] for x in ["1", "2" ,"3", "4"]]
# newnames[44:48] = ["B" + "3" + "_R" + 'E'+ "_O" + x  for x in ["1", "2" ,"3", "4"]]


# newnames[0:20] = ["B" + "4" + "_R" + y+ "_O" + x for y in ['1', '2', '3','4', "5"] for x in ["1", "2" ,"3", "4"]]
# newnames[20:24] = ["B" + "4" + "_R" + 'E'+ "_O" + x  for x in ["1", "2" ,"3", "4"]]
newnames = ["B" + "5" + "_R" + 'E'+ "_O" + str(i) for i in np.arange(0, len(onlyfiles))]


for i in np.arange(0, len(onlyfiles)):
    filename = mypath + '/' + onlyfiles[i]
    outfile =  outpath + '/' + newnames[i] + '.JPG'

    boardWrite(filename, outfile)
