#########################################
# IMPORT
# MODULES
#########################################


import time
import numpy
import sounddevice
import traceback
import rtmidi

from . import samplerbox_audio
from . import config
from .SamplesLoader import SamplesLoader

if config.USE_SERIALPORT_MIDI:
    from .SerialPortMidi import SerialPortMidi
if config.USE_BUTTONS:
    from .GpioButtons import GpioButtons
if config.USE_I2C_7SEGMENTDISPLAY:
    from .SevenSegmentDisplay import SevenSegmentDisplay
if config.USE_SYSTEMLED:
    from .SystemLed import SystemLed


class SamplerBox:
    FADEOUTLENGTH = 30000
    NOTES = ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]

    def __init__(self):
        self.FADEOUT = numpy.linspace(1., 0., self.FADEOUTLENGTH)  # by default, float64
        self.FADEOUT = numpy.power(self.FADEOUT, 6)
        self.FADEOUT = numpy.append(self.FADEOUT, numpy.zeros(self.FADEOUTLENGTH, numpy.float32)).astype(numpy.float32)
        self.SPEED = numpy.power(2, numpy.arange(0.0, 84.0) / 12).astype(numpy.float32)

        self.audio_stream = None
        self.midi_in = []
        self.samples = {}
        self.playing_notes = {}
        self.sustain_playing_notes = []
        self.sustain = False
        self.playing_sounds = []
        # self.global_volume = 10 ** (-12.0 / 20)  # -12dB default global volume
        self.global_volume = 10 ** (-6.0 / 20)  # -12dB default global volume
        self.global_transpose = 0
        self.preset = config.DEFAULT_SOUNDBANK
        self.samples_loader = SamplesLoader(self)
        self.displayer = None

    def audio_callback(self, outdata, frame_count, time_info, status):
        try:
            rmlist = []
            self.playing_sounds = self.playing_sounds[-config.MAX_POLYPHONY:]
            buffer = samplerbox_audio.mixaudiobuffers(self.playing_sounds, rmlist, frame_count, self.FADEOUT,
                                                      self.FADEOUTLENGTH,
                                                      self.SPEED)
            for e in rmlist:
                self.playing_sounds.remove(e)
            buffer *= self.global_volume
            outdata[:] = buffer.reshape(outdata.shape)
        except Exception as e:
            print('exception:', traceback.print_exception(e))

    def midi_callback(self, message, time_stamp=None):
        try:
            print('midi cb', message)
            message = message[0]
            messagetype = message[0] >> 4
            messagechannel = (message[0] & 15) + 1
            note = message[1] if len(message) > 1 else None
            midinote = note
            velocity = message[2] if len(message) > 2 else None
            print('midi cb type', messagetype)
            if messagetype == 9 and velocity == 0:
                messagetype = 8
            if messagetype == 9:  # Note on
                midinote += self.global_transpose
                try:
                    self.playing_notes.setdefault(midinote, []).append(self.samples[midinote, velocity].play(midinote))
                except Exception as e:
                    print('exception:', traceback.print_exception(e))
            elif messagetype == 8:  # Note off
                midinote += self.global_transpose
                if midinote in self.playing_notes:
                    for n in self.playing_notes[midinote]:
                        if self.sustain:
                            self.sustain_playing_notes.append(n)
                        else:
                            n.fadeout(50)
                    self.playing_notes[midinote] = []
            elif messagetype == 12:  # Program change
                print('Program change ' + str(note))
                self.preset = note
                self.load_samples()
            elif (messagetype == 11) and (note == 64) and (velocity < 64):  # sustain pedal off
                for n in self.sustain_playing_notes:
                    n.fadeout(50)
                self.sustain_playing_notes = []
                self.sustain = False
            elif (messagetype == 11) and (note == 64) and (velocity >= 64):  # sustain pedal on
                self.sustain = True
        except Exception as e:
            print('exception:', traceback.print_exception(e))

    def connect_audio_output(self):
        try:
            self.audio_stream = sounddevice.OutputStream(device=config.AUDIO_DEVICE_ID, blocksize=512, samplerate=44100,
                                                         channels=2, dtype='int16', callback=self.audio_callback)
            self.audio_stream.start()
            print('Opened audio device #%i' % config.AUDIO_DEVICE_ID)
        except:
            print('Invalid audio device #%i' % config.AUDIO_DEVICE_ID)
            exit(1)

    def display(self, message):
        if self.displayer:
            self.displayer.display(message)

    def connect_midi_input(self):
        self.midi_in = [rtmidi.MidiIn()]
        previous = []
        while True:
            all_ports = self.midi_in[0].get_ports()
            for num_port, port in enumerate(all_ports):
                if port not in previous and 'Midi Through' not in port:
                    self.midi_in.append(rtmidi.MidiIn())
                    self.midi_in[-1].set_callback(self.midi_callback)
                    self.midi_in[-1].open_port(num_port)
                    print('Opened MIDI: ' + str(port))
            previous = all_ports
            time.sleep(2)

    def load_samples(self):
        self.samples_loader.load_samples()

    def init(self):
        # -- /!\ Possible strange conflict between samples array / audio callback / OOP
        # -- https://github.com/spatialaudio/python-sounddevice/issues/513
        # -- Putting load_samples before connect_audio_output seems to circle this issue.
        self.load_samples()
        self.connect_audio_output()
        self.connect_midi_input()

        if config.USE_SERIALPORT_MIDI:
            spm = SerialPortMidi(self)
            spm.init()
        if config.USE_BUTTONS:
            buttons = GpioButtons(self)
            buttons.init()
        if config.USE_I2C_7SEGMENTDISPLAY:
            self.displayer = SevenSegmentDisplay(self)
            self.displayer.init()
        if config.USE_SYSTEMLED:
            sl = SystemLed(self)
            sl.init()
