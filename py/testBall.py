# python C:/Users/zachb/Documents/Python4fun/colorKu/py/testBall.py
from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import cv2
from tkinter import Tk    # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from keras.models import load_model
import sys
exec(open("C:/Users/zachb/Documents/Python4fun/colorKu/py/boardLocater.py").read())


projdir = 'C:/Users/zachb/Documents/Python4fun/colorKu/'

filename = askopenfilename()
# filename = 'C:/Users/zachb/Documents/Python4fun/colorKu/images/boardPics/ck2.png'
img = boardGrab(filename)
cv2.imshow('The board',img)



while True:
    try:
        val = input("Is the plot squarely in the frame (y/n): ")
    except ValueError:
        print("Sorry, I didn't understand that.")
        continue

    if val == 'y':
        cv2.destroyAllWindows()
        print("GREAT!")
        break
    elif val == 'n':
        print("Retake picture and retry...")
        sys.exit()
    else:
        print("Must choose 'y' or 'n': ")
        continue



colors = ["red", "orange", "yellow", "lightgreen", "darkgreen", "lightblue", "darkblue", "lightpurple", "darkpurple", 'empty']
inpt = [156, 242, 327, 421, 502, 590, 681, 769, 852]
coverSize = 38

ballHold = []
for x, row in enumerate(inpt):
    for y, col in enumerate(inpt):
        cell = np.array(img[np.arange(row-coverSize, row+(coverSize + 1)), :][:, np.arange(col-coverSize, col+(coverSize + 1))])
        ballHold.append(cv2.resize(cell, (15, 15), interpolation = cv2.INTER_AREA))

test_data = np.array(ballHold)/255.0

model = load_model(projdir + 'models/' + "ballClassifier.h5")

outlab = pd.Series(colors)
preds = model.predict(test_data)
maxpred = preds.max(axis = 1)
i = 0
predC = np.array([outlab[preds[i] == maxpred[i]] for i in np.arange(0,preds.shape[0])])


boardPreds = predC.reshape((9,9))

img2 = img.copy()
plt.figure(figsize=(10, 8))
plt.imshow(img2[:,:,[2, 1, 0]])
for x, row in enumerate(inpt):
    for y, col in enumerate(inpt):
        plt.text(row-35, col, boardPreds[y, x], rotation = 20, fontsize = 'large', fontweight = 'bold')
plt.show()

# for i in np.arange(0, 81):
#     cv2.imshow(str(predC[i].tolist()), cv2.resize(test_data[i], (500,500)))
#     print(i)
