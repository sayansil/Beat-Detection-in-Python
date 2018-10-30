import numpy as np
from aubio import source, tempo
import soundfile as sf

def get_file_beats(path, samplerate=44100, window_size=1024, block_size=43*1024):
    wav, s = sf.read(wav_file)
    beats = np.array([])
    for sample_index in range(0, len(wav)-window_size, window_size):
        Ejs = np.array([])
        for i in range(sample_index, sample_index + window_size - block_size, block_size):
            Ej = 0.0
            for j in range(i, i+block_size):
                Ej = Ej + pow(wav[j][0], 2) + pow(wav[j][1], 2)
            Ejs = np.append(Ejs, Ej)
        
        avgE = (block_size/window_size) * np.sum(Ejs)
        varE = (block_size/window_size) * np.sum(pow(avgE - Ejs, 2))
        C = (-0.0000015) * varE + 1.5142857
        
        beat_blocks = np.array(np.where(Ejs > C*avgE)).flatten()
        beat_blocks = beat_blocks * block_size + sample_index
        beats = np.append(beats, beat_blocks)
        
    beat_gaps = beats/samplerate
    beat_gaps = beat_gaps - np.insert(beat_gaps[:-1], 0, 0)

    return beat_gaps
