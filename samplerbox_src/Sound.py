import numpy

from . import samplerbox_audio
from .WaveReader import WaveReader
from .PlayingSound import PlayingSound

class Sound:
    def __init__(self, samplerbox, filename, midinote, velocity):
        wf = WaveReader(filename)
        self.samplerbox = samplerbox
        self.fname = filename
        self.midinote = midinote
        self.velocity = velocity
        #if wf.getloops():
        if False:
            self.loop = wf.getloops()[0][0]
            self.nframes = wf.getloops()[0][1] + 2
        else:
            self.loop = -1
            self.nframes = wf.getnframes()
        self.data = self.frames2array(wf.readframes(self.nframes), wf.getsampwidth(), wf.getnchannels())
        wf.close()

    def play(self, note):
        snd = PlayingSound(self.samplerbox, self, note)
        self.samplerbox.playing_sounds.append(snd)
        return snd

    def frames2array(self, data, sampwidth, numchan):
        if sampwidth == 2:
            npdata = numpy.frombuffer(data, dtype=numpy.int16)
        elif sampwidth == 3:
            npdata = samplerbox_audio.binary24_to_int16(data, len(data) // 3)
        if numchan == 1:
            npdata = numpy.repeat(npdata, 2)
        return npdata

