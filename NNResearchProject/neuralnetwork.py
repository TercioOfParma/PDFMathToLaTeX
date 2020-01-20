import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import ModelCheckpoint, TensorBoard
from sklearn.model_selection import train_test_split
from config import language_tags, max_letters

data = np.load('arr.npy')
#data = np.load('data.csv')
print(language_tags)
print(2 + len(language_tags))
inputs = data[:, 2+len(language_tags):]
labels = data[:, 1:1+len(language_tags)]

x_train, x_test, y_train, y_test = train_test_split(inputs, labels, test_size=0.15)

print(x_test.shape)
print(y_test.shape)
print(x_train.shape)
print(y_train.shape)

network = Sequential()
network.add(Dense(200, input_dim=128*max_letters - 1, activation='sigmoid'))
network.add(Dense(150, activation='sigmoid'))
network.add(Dense(100, activation='sigmoid'))
network.add(Dense(100, activation='sigmoid'))
network.add(Dense(len(language_tags), activation='softmax'))

network.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

filepath = "weightslang.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
tboard = TensorBoard(log_dir='./logs', write_graph=True, write_images=True)
callbacks_list = [checkpoint, tboard]

network.fit(x_train, y_train, epochs=30, batch_size=1000, validation_data=(x_test, y_test), callbacks=callbacks_list)

network.save_weights(filepath)
