import pandas as pd
import numpy as np


# Preprocess
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler


# Kera's
from keras import models
from keras import layers


import warnings
import sys
warnings.filterwarnings('ignore')

csv_path = sys.argv[1]

# Extracting data from csv file
data = pd.read_csv(csv_path)
data = data.drop(['filename'], axis='columns')


genre_list = data.iloc[:, -1]   # choose only the genre from dataset
encoder = LabelEncoder()        # transform genre_list to numbers between 0 - 9
y = encoder.fit_transform(genre_list)

scaler = StandardScaler()
X = scaler.fit_transform(np.array(data.iloc[:, :-1], dtype=float))


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)  # len(y_train) -> 800    len(y_test) -> 200



# Keras classification and model building
model = models.Sequential()

model.add(layers.Dense(256, activation='relu', input_shape=(X_train.shape[1],)))
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

print("training")
sys.stdout.flush()

history = model.fit(X_train,
                    y_train,
                    epochs=20,
                    batch_size=64)
sys.stdout.flush()




# Save the model
model.save('./engine/Genre_model.h5')

print("Model saved")
sys.stdout.flush()
