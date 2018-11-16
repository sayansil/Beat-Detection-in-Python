import soundfile as sf
import matplotlib.pyplot as plt
import math

class BiquadFilter:

    def __init__(self, samplingFreq, channels):
        self.samplingFreq = samplingFreq
        self.channels = channels
        #self.centerFreq = centerFreq
        #self.filterType = filterType

        # piOverSamplingFreq = (math.pi * 2)/samplingFreq
        piOverSamplingFreq = math.pi/samplingFreq

        self.b0 = 0
        self.b1 = 0
        self.b2 = 0
        self.a0 = 0
        self.a1 = 0
        self.a2 = 0
        self.bi1m = [0]*self.channels
        self.bi2m = [0]*self.channels
        self.bo1m = [0]*self.channels
        self.bo2m = [0]*self.channels

        self.w = piOverSamplingFreq#*self.centerFreq
        self.cosw = float(math.cos(self.w))
        self.a = float(math.sin(self.w))/(2)
        self.b0 = (1 - self.cosw)/2
        self.b1 = (1 - self.cosw)
        self.b2 = self.b0
        self.a0 = 1 + self.a
        self.a1 = -2*self.cosw
        self.a2 = 1-self.a

    def toString(self):
        return "a0: {0}\na1: {1}\na2: {2}\nb0: {3}\nb1: {4}\nb2: {5}".format(self.a0, self.a1, self.a2, self.b0, self.b1, self.b2)

    def apply(self, inputBuffer, outputBuffer):
        bufferSize = len(inputBuffer)
        for i in range(0, self.channels):
            outputBuffer[0 + i] = (self.b0*inputBuffer[0 + i] + self.b1*self.bi1m[i] + self.b2*self.bi2m[i] + self.a1*self.bo1m[i] + self.a2*self.bo2m[i])/self.a0
            outputBuffer[self.channels + i] = (self.b0*inputBuffer[self.channels + i] + self.b1*inputBuffer[0 + i] + self.b2*self.bi1m[i] - self.a1*outputBuffer[0 + i] - self.a2*self.bo1m[i])/self.a0

            j = 2*self.channels
            while j<bufferSize:
                outputBuffer[j + i] = (self.b0*inputBuffer(j + i) + self.b1*inputBuffer(j - self.channels + i) + self.b2*inputBuffer(j - self.channels + i) - self.a2*outputBuffer(j - 2*self.channels + i))/self.a0
                j += self.channels

            self.bi2m[i] = inputBuffer(bufferSize - 2*self.channels + i)
            self.bi1m[i] = inputBuffer(bufferSize - self.channels + i)
            self.bo2m[i] = outputBuffer(bufferSize - 2*self.channels + i)
            self.bo1m[i] = outputBuffer(bufferSize - self.channels + i)

wav, s = sf.read("/home/pratyush/Downloads/output.wav")
wav = [i*j for (i, j) in wav]

filter = BiquadFilter(s, 1)


plt.figure(figsize=(20, 10))
plt.plot(wav)
plt.show()
