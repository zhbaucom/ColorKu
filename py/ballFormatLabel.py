from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import cv2
from tkinter import Tk    # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import pickle


ballpath = 'C:/Users/zachb/Documents/Python4fun/colorKu/images/balls'
ddump = 'C:/Users/zachb/Documents/Python4fun/colorKu/data'
onlyfiles = [f for f in listdir(ballpath) if isfile(join(ballpath, f))]
ball = cv2.imread(ballpath + '/' + onlyfiles[0])
bw = cv2.resize(ball, (15, 15), interpolation = cv2.INTER_AREA)

smallball = []
labels = []
for files in onlyfiles:
    ball = cv2.imread(ballpath + '/' + files)
    bw = cv2.resize(ball, (15, 15), interpolation = cv2.INTER_AREA)
    smallball.append(bw)
    labels.append(files.split('_')[4].replace('.JPG', ''))

ckImg = {
    'labels': np.array(labels),
    'data': np.array(smallball)
}

with open(ddump + '/ckImg.pickle', 'wb') as output:
    pickle.dump(ckImg, output)
