import sounddevice
import time

class SamplerBox:
    def __init__(self):
        self.samples = {}

    def audio_callback(self, outdata, frame_count, time_info, status):
        print('ac')

    def init(self):
        self.connect_audio_output()
        time.sleep(1)

        self.load_samples()

    def connect_audio_output(self):
        try:
            sd = sounddevice.OutputStream(callback=self.audio_callback)
            sd.start()
            print('Opened audio device')
        except:
            print('Invalid audio device')
            exit(1)

    def load_samples(self):
        for midinote in range(128):
            for velocity in range(128):
                self.samples[midinote, velocity] = Sound()


class Sound:
    def __init__(self):
        pass


sb = SamplerBox()
sb.init()
#sb.connect_audio_output()
time.sleep(20)

