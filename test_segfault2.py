import sounddevice
import time

samples = {}


class Sound:
    def __init__(self):
        pass

def audio_callback(self, outdata, frame_count, time_info, status):
    print('ac')


try:
    sd = sounddevice.OutputStream(callback=audio_callback)
    sd.start()
    print('Opened audio device')
except:
    print('Invalid audio device')
    exit(1)

for midinote in range(128):
    for velocity in range(128):
        samples[midinote, velocity] = Sound()

time.sleep(20)