class AudioFilter:

    def __init__(self):
        self.inputBuffer = 0
        self.outputBuffer = 0

    def apply(self, inputBuffer, outputBuffer):
        self.inputBuffer = inputBuffer
        self.outputBuffer = outputBuffer


class AudioFile:

    def __init__(self):
        self.sampleBuffer = []
        self.offset = 0
        self.numFramesToRead = 0

    def readNormalizedFrames(self, sampleBuffer=[], offset=0, numFramesToRead=0):
        self.sampleBuffer = sampleBuffer
        self.offset = offset
        self.numFramesToRead = numFramesToRead


class FilterBPMDetector:

    def __init__(self, thresholdMultiplier, skip, framesToRead):
        self.thresholdMultiplier = thresholdMultiplier
        self.skip = skip
        self.framesToRead = framesToRead
        # Add objects as __init__ parameters
        audioFile = AudioFile()
        audioFilter = AudioFilter()

        self.bufferRefillCount = 0
        self.nextFrame = 0
        self.inputBuffer = []
        self.peaks = []
        self.distanceHistogram = {}
        self.bpmHistogram = {}
        self.bpm = -1.0
        self.threshold = 0.0


    def computePeaks(self):
        outputBuffer = []
        audioFile.readNormalizedFrames(inputBuffer, framesToRead)