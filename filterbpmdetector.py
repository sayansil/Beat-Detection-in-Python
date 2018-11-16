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

        self.audioFile = AudioFile()
        self.audioFilter = AudioFilter()

        self.bufferRefillCount = 0
        self.nextFrame = 0
        self.inputBuffer = []
        self.peaks = []
        self.distanceHistogram = {}
        self.bpmHistogram = {}
        self._bpm = -1.0
        self.threshold = 0.0

    def computePeaks(self):
        outputBuffer = []
        self.audioFile.readNormalizedFrames(self.inputBuffer, self.framesToRead)
        self.audioFilter.apply(self.inputBuffer, outputBuffer)

        maxVal = 0.0
        #outputBuffer.foreach(x => if (x> maxVal) maxVal = x)
        self.threshold = self.thresholdMultiplier*maxVal
        self.bufferRefillCount += 1

        while self.bufferRefillCount*self.framesToRead < self.audioFile.numFramesToRead:
            while self.nextFrame < self.bufferRefillCount*self.framesToRead:
                localIndex = self.nextFrame - (self.bufferRefillCount - 1)*self.framesToRead
                maxValue = 0.0
                for i in range(0, self.audioFile.numChannels):
                    channelValue = outputBuffer[localIndex + i]
                    if channelValue > maxValue:
                        maxValue = channelValue
                if maxValue > self.threshold:
                    self.peaks += self.nextFrame
                    self.nextFrame += self.skip
                else:
                    self.nextFrame += 1
            outputBuffer = []
            self.audioFile.readNormalizedFrames(self.inputBuffer, self.framesToRead)
            self.bufferRefillCount += 1
            maxVal = 0.0
            #outputBuffer.foreach(x => if (x> maxVal) maxVal = x)
            self.threshold = (self.threshold + self.thresholdMultiplier*maxVal)/2

    def computeDistanceHistogram(self):

    def computeBpmHistogram(self):


    def computeBpm(self):
        maxTempo = 0.0
        maxCount = 0
        #bpmHistogram.foreach(p => {
            #val tempo = p._1
            #val count = p._2
            #if (count > maxCount) {
            #maxTempo = tempo
            #maxCount = count
            #}
        #})
        self._bpm = maxTempo

    def bpm(self):
        if self._bpm == -1:
            self.computePeaks()
            self.computeDistanceHistogram()
            self.computeBpmHistogram()
            self.computeBpm()
        return self._bpm