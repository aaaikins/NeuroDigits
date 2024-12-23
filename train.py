import numpy as np

import tensorflow as tf

from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint


(X_train, y_train), (X_test, y_test) = mnist.load_data()

# Normalize pixel values to [0, 1]
X_train = X_train.astype(np.float32)/255
X_test = X_test.astype(np.float32)/255

# Add channel dimension (28x28x1)
X_train = np.expand_dims(X_train, -1)
X_test = np.expand_dims(X_test, -1)

# One-hot encoding of labels
y_train = tf.keras.utils.to_categorical(y_train)
y_test = tf.keras.utils.to_categorical(y_test)

model = Sequential()

model.add(Conv2D(32,(3,3), input_shape=(28,28,1), activation='relu'))
model.add(MaxPool2D((2,2)))
model.add(Conv2D(64,(3,3), activation='relu'))
model.add(MaxPool2D((2,2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(10, activation='softmax'))


model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=["accuracy"])

# Set up callbacks for training
es = EarlyStopping(monitor='val_accuracy', min_delta=0.01, patience=5, verbose=1, mode='max')
mc = ModelCheckpoint('Aikins_cnn_model.keras', monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')

cb = [es, mc]

model.fit(X_train, y_train, epochs=50, validation_split=0.3, batch_size=64, callbacks=cb)

model.save('cnn_model.keras')
