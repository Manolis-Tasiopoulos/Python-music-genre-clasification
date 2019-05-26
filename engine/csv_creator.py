import librosa
import numpy as np
import os
import csv
import warnings
import sys
warnings.filterwarnings('ignore')

db_path = sys.argv[1]

# Creating Header file
header = 'filename bpm chroma_stft rmse spectral_centroid spectral_bandwidth rolloff zero_crossing_rate'

for i in range(1, 21):
    header += 'mfcc' + str(i)


header += ' label'
header = header.split()


# export csv file
file = open('./engine/data.csv', 'w', newline='')
with file:
    writer = csv.writer(file)
    writer.writerow(header)

genres = 'blues classical country disco hiphop jazz metal pop reggae rock'.split()

print("analyse")
sys.stdout.flush()

count = 1;

for g in genres:
    for filename in os.listdir(f'{db_path}/{g}'):
        song_name = f'{db_path}/{g}/{filename}'
        y, sr = librosa.load(song_name, mono=True, duration=30)
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)
        mfcc = librosa.feature.mfcc(y=y, sr=sr)
        rmse = librosa.feature.rmse(y=y)
        bpm, beats = librosa.beat.beat_track(y=y, sr=sr)
        to_append = f'{filename} {bpm} {np.mean(chroma_stft)} {np.mean(rmse)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'
        for e in mfcc:
            to_append += f' {np.mean(e)}'
        to_append += f' {g}'
        file = open('./engine/data.csv', 'a', newline='')
        with file:
            writer = csv.writer(file)
            writer.writerow(to_append.split())
        percents = round(100.0 * count / 1000, 1)
        count += 1
        print(f'{filename}     {percents}%')
        sys.stdout.flush()

print("finish")
sys.stdout.flush()
