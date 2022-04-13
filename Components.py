# python C:/Users/zachb/Documents/Python4fun/colorKu/py/testBall.py
from os import listdir, chdir
from os.path import isfile, join
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import cv2
from tkinter import Tk    # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from keras.models import load_model
import sys
chdir('C:/Users/zachb/Documents/GitHubProjects/ColorKu/')
exec(open("py/BoardFinder/boardLocater.py").read())
exec(open("py/CKsolve/ckSolve.py").read())


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

while True:
    try:
        val = input("Are the labels correct? (y/n): ")
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


oldColorZ = np.array(["red", "orange", "yellow", "lightgreen", "darkgreen", "lightblue", "darkblue", "lightpurple", "darkpurple", 'empty'])
Colorz2 = np.array(["Red", "Orange", "Yellow", "Light Green", "Dark Green", "Light Blue", "Dark Blue",  "Light Purple", "Dark Purple", None])


puzz_vec = []
for i in range(9):
    for j in range(9):
        puzz_vec = puzz_vec + [Colorz2[oldColorZ == boardPreds[i][j]]]
puzz_vec = np.concatenate(np.array(puzz_vec))


exec(open("py/CKsolve/ckSolve.py").read())
while True:
    pz = ckPuzzle(puzz_vec)
    pz.solve1step()
    print(pz.plt_puzz())
    if pz.error_check() != 'No error':
        print("Found errors!!!")
        print(pz.error_check())
        break
    if not pz.puzz_change():
        print("Could not find any additional cells with current logic...")
        print(pz.plt_puzz())
        break

    oneORall = input("Show 'one' or 'all' solveable spots? (one/all): ")
    showTF = input("Show colors of solveable spot(s) (T/F): ")
    if showTF == 'T':
        showTF = True
    elif showTF == 'F':
        showTF = False

    pz.puzzle_update(oneORall)

    print(pz.plt_puzz_update(show_updated_values = showTF))

    accept_updates = input("Accept updates?(y/n): ")
    if accept_updates == 'y':
        puzz_vec = pz.puzzdf_update
    else:
        break
