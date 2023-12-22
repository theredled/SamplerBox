import wave
import traceback
from chunk import Chunk
import struct


#########################################
# SLIGHT MODIFICATION OF PYTHON'S WAVE MODULE
# TO READ CUE MARKERS & LOOP MARKERS
#########################################
class WaveReader(wave.Wave_read):
    '''
    def initfp(self, file):
        self._convert = None
        self._soundpos = 0
        self._cue = []
        self._loops = []
        self._ieee = False
        self._file = Chunk(file, bigendian=False)
        #print('wr', self._file); return
        if self._file.getname() != b'RIFF':
            raise IOError('file does not start with RIFF id')
        if self._file.read(4) != b'WAVE':
            raise IOError('not a WAVE file')
        self._fmt_chunk_read = 0
        self._data_chunk = None
        while 1:
            self._data_seek_needed = 1
            try:
                chunk = Chunk(self._file, bigendian=False)
            except EOFError as e:
                print('exception:', traceback.print_exception(e))
            chunkname = chunk.getname()
            if chunkname == b'fmt ':
                self._read_fmt_chunk(chunk)
                self._fmt_chunk_read = 1
            elif chunkname == b'data':
                if not self._fmt_chunk_read:
                    raise IOError('data chunk before fmt chunk')
                self._data_chunk = chunk
                self._nframes = chunk.chunksize // self._framesize
                self._data_seek_needed = 0
            elif chunkname == b'cue ':
                numcue = struct.unpack('<i', chunk.read(4))[0]
                for i in range(numcue):
                    id, position, datachunkid, chunkstart, blockstart, sampleoffset = struct.unpack('<iiiiii', chunk.read(24))
                    self._cue.append(sampleoffset)
            elif chunkname == b'smpl':
                manuf, prod, sampleperiod, midiunitynote, midipitchfraction, smptefmt, smpteoffs, numsampleloops, samplerdata = struct.unpack(
                    '<iiiiiiiii', chunk.read(36))
                for i in range(numsampleloops):
                    cuepointid, type, start, end, fraction, playcount = struct.unpack('<iiiiii', chunk.read(24))
                    self._loops.append([start, end])
            chunk.skip()
        if not self._fmt_chunk_read or not self._data_chunk:
            raise IOError('fmt chunk and/or data chunk missing')

    def getmarkers(self):
        return self._cue

    def getloops(self):
        return self._loops

'''