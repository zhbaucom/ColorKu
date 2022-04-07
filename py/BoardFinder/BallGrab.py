from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import cv2
from tkinter import Tk    # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

outpath = 'C:/Users/zachb/Documents/Python4fun/colorKu/images/boardTrain'
ballpath = 'C:/Users/zachb/Documents/Python4fun/colorKu/images/balls'
onlyfiles = [f for f in listdir(outpath) if isfile(join(outpath, f))]

#B4 filter
onlyfiles = pd.Series(onlyfiles)[['B5' in i for i in onlyfiles]].tolist()

# Paremeters to find balls
inpt = [156, 242, 327, 421, 502, 590, 681, 769, 852]
coverSize = 38

colors = ["red", "orange", "yellow", "lightgreen", "darkgreen", "lightblue", "darkblue", "lightpurple", "darkpurple"]
basecol = np.array([[x for _ in np.arange(0,9)] for x in colors])

for i, _ in enumerate(onlyfiles):

    splitfile = onlyfiles[i].split("_")

    O = int(list(splitfile[2])[1]) - 1
    Ri = list(splitfile[1])[1]
    if Ri == 'E':
        bc = np.array([['empty' for _ in np.arange(0,9)] for x in colors])
    else:
        R = 10-int(Ri)
        bc = np.vstack((basecol[R:9], basecol[0:R]))

    colref = np.rot90(bc, O)

    img = cv2.imread(outpath+'/'+onlyfiles[i])
    file = onlyfiles[i].replace(".JPG","")

    row = inpt[0]
    col = inpt[0]
    for x, row in enumerate(inpt):
        for y, col in enumerate(inpt):
            cell = np.array(img[np.arange(row-coverSize, row+(coverSize + 1)), :][:, np.arange(col-coverSize, col+(coverSize + 1))])
            cv2.imwrite(ballpath+ '/' + file + '_C'+str(x) + str(y) + '_' + colref[x,y] +'.JPG', cell)
