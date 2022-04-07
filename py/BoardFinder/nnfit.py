import tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv3D, MaxPooling3D, Conv2D, MaxPooling2D
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping
import h5py
import numpy as np
import matplotlib.pyplot as plt
import pickle
from tensorflow.keras.utils import to_categorical
import pandas as pd

projdir = 'C:/Users/zachb/Documents/Python4fun/colorKu/'
ddump = 'C:/Users/zachb/Documents/Python4fun/colorKu/data'

with open(ddump + '/ckImg.pickle', 'rb') as data:
    ckImg = pickle.load(data)

colors = ["red", "orange", "yellow", "lightgreen", "darkgreen", "lightblue", "darkblue", "lightpurple", "darkpurple", 'empty']
labels = pd.get_dummies(pd.Series(ckImg['labels']).astype(pd.CategoricalDtype(categories=colors)))
# mlab = pd.get_dummies(cat.astype(pd.CategoricalDtype(categories=colors)))
# labels = pd.get_dummies(ckImg['labels'])
ckims = np.array(ckImg['data'])/255.0
# Model configuration
batch_size = 100
no_epochs = 50
learning_rate = 0.0001
no_classes = 10
validation_split = 0.2
verbosity = 1

# Layout
sample_shape = ckims.shape[1:]

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=sample_shape, padding = 'SAME'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', padding = 'SAME'))
model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Conv2D(32, kernel_size=(3, 3), activation='relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(32, activation='relu'))
model.add(Dense(no_classes, activation='softmax'))


# Compile the model
model.compile(loss=tensorflow.keras.losses.categorical_crossentropy,
              optimizer=tensorflow.keras.optimizers.Adam(lr=learning_rate),
              metrics=['accuracy'])

early_stopping_monitor = EarlyStopping(patience = 3, monitor = 'val_loss')

# Fit data to model
history = model.fit(ckims, labels,
            batch_size=batch_size,
            epochs=no_epochs,
            verbose=verbosity,
            validation_split=validation_split,
            callbacks = [early_stopping_monitor])

model.save(projdir + 'models/' + "ballClassifier.h5")

# %run  C:/Users/zachb/Documents/Python4fun/colorKu/py/testBall.py
#
# outlab = labels.columns
#
# preds = model.predict(test_data)
# maxpred = preds.max(axis = 1)
#
# predC = np.array([outlab[preds[i] == maxpred[i]] for i in np.arange(0,preds.shape[0])])
# i = 0
# for i, _ in enumerate(predC):
#     cv2.imshow(str(predC[i].tolist()), cv2.resize(test_data[i], (500,500)))
#     print(i)
