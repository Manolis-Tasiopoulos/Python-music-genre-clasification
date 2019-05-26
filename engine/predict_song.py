import pandas as pd
import librosa
import numpy as np


# Kera's
from keras.models import load_model
from sklearn.preprocessing import StandardScaler

import warnings
import sys
warnings.filterwarnings('ignore')

song_path = sys.argv[1]

#load csv file for scaling

print("predict")
sys.stdout.flush()

genres = 'blues classical country disco hiphop jazz metal pop reggae rock'.split()

data = pd.read_csv('./engine/data.csv')
data = data.drop(['filename'], axis='columns')

scaler = StandardScaler()
X = scaler.fit(np.array(data.iloc[:, :-1], dtype=float))

# Load model
model = load_model('./engine/Genre_model.h5')


# Divide song to information's
song_name = song_path
y, sr = librosa.load(song_name, mono=True, duration=30)
chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
zcr = librosa.feature.zero_crossing_rate(y)
mfcc = librosa.feature.mfcc(y=y, sr=sr)
rmse = librosa.feature.rmse(y=y)
bpm, beats = librosa.beat.beat_track(y=y, sr=sr)


test_sample = [bpm, np.mean(chroma_stft),  np.mean(rmse), np.mean(spec_cent), np.mean(spec_bw),
               np.mean(rolloff), np.mean(zcr)]


for e in mfcc:
    test_sample.append(np.mean(e))

test_sample = np.array(test_sample)
X_transformed = scaler.transform(test_sample.reshape(-1, 1).T)
predictions = model.predict(np.array(X_transformed.reshape(1, 27)))
max_val = np.argmax(predictions)


count = 0
results = ''

print("results")
sys.stdout.flush()

for p in predictions[0]:
    if count == np.argmax(predictions[0]):
        print(f'{genres[count]}: {int(np.round(p, decimals=3) * 100)}%   <--- Song is probably {genres[count]}')
    else:
        print(f'{genres[count]}: {int(np.round(p, decimals=3) * 100)}% ')


    sys.stdout.flush()
    count += 1


print("---finish---")
sys.stdout.flush()
