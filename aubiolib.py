import numpy as np
from aubio import source, tempo


def get_file_beats(path, samplerate=44100, win_s=1024):
    hop_s = win_s//2
    s = source(path, samplerate, hop_s)
    samplerate = s.samplerate
    o = tempo("specdiff", win_s, hop_s, samplerate)
    beats = []
    total_frames = 0
    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = o.get_last_s()
            beats.append(int(this_beat*samplerate))
            #if o.get_confidence() > .2 and len(beats) > 2.:
            #    break
        total_frames += read
        if read < hop_s:
            break
    beats = np.array(beats) / samplerate
    beats = beats - np.insert(beats[:-1], 0, 0)
    return beats
