import os, re, threading
from . import config
from .Sound import Sound


class SamplesLoader:
    def __init__(self, samplerbox):
        self.samplerbox = samplerbox
        self.samplesdir = config.SAMPLES_DIR if os.listdir(
            config.SAMPLES_DIR) else '.'  # use current folder (containing 0 Saw) if no user media containing samples has been found
        self.loading_thread = None
        self.loading_interrupt = False

    def load_samples(self):
        if self.loading_thread:
            self.loading_interrupt = True
            self.loading_thread.join()
            self.loading_thread = None

        self.loading_interrupt = False
        self.loading_thread = threading.Thread(target=self.async_load_samples)
        self.loading_thread.daemon = True
        self.loading_thread.start()

    def load_samples_by_definition_file(self, definitionfname, dirname):
        with open(definitionfname, 'r') as definitionfile:
            for i, pattern in enumerate(definitionfile):
                try:
                    if r'%%volume' in pattern:  # %%paramaters are global parameters
                        self.samplerbox.global_volume *= 10 ** (float(pattern.split('=')[1].strip()) / 20)
                        continue
                    if r'%%transpose' in pattern:
                        self.samplerbox.global_transpose = int(pattern.split('=')[1].strip())
                        continue
                    defaultparams = {'midinote': '0', 'velocity': '127', 'notename': ''}
                    if len(pattern.split(',')) > 1:
                        defaultparams.update(dict([item.split('=') for item in
                                                   pattern.split(',', 1)[1].replace(' ', '').replace('%', '').split(
                                                       ',')]))
                    pattern = pattern.split(',')[0]
                    pattern = re.escape(pattern.strip())  # note for Python 3.7+: "%" is no longer escaped with "\"
                    pattern = pattern.replace(r"%midinote", r"(?P<midinote>\d+)").replace(r"%velocity",
                                                                                          r"(?P<velocity>\d+)") \
                        .replace(r"%notename", r"(?P<notename>[A-Ga-g]#?[0-9])").replace(r"\*",
                                                                                         r".*?").strip()  # .*? => non greedy
                    for fname in os.listdir(dirname):
                        if self.loading_interrupt:
                            return False
                        m = re.match(pattern, fname)
                        if m:
                            info = m.groupdict()
                            midinote = int(info.get('midinote', defaultparams['midinote']))
                            velocity = int(info.get('velocity', defaultparams['velocity']))
                            notename = info.get('notename', defaultparams['notename'])
                            if notename:
                                midinote = self.samplerbox.NOTES.index(notename[:-1].lower()) + (
                                        int(notename[-1]) + 2) * 12
                            self.samplerbox.samples[midinote, velocity] = Sound(self.samplerbox,
                                                                                os.path.join(dirname, fname),
                                                                                midinote,
                                                                                velocity)
                except:
                    print("Error in definition file, skipping line %s." % (i + 1))
        return True

    def async_load_samples(self):
        # -- Resets
        self.samplerbox.playing_sounds = []
        self.samplerbox.samples = {}
        self.samplerbox.global_volume = 10 ** (-12.0 / 20)  # -12dB default global volume
        self.samplerbox.global_transpose = 0

        # -- Find dir name for instrument
        basename = next((f for f in os.listdir(self.samplesdir) if f.startswith("%d " % self.samplerbox.preset)),
                        None)  # or next(glob.iglob("blah*"), None)
        if basename:
            dirname = os.path.join(self.samplesdir, basename)
        else:
            print('Preset empty: %s' % self.samplerbox.preset)
            self.samplerbox.display("E%03d" % self.samplerbox.preset)
            return
        print('Preset loading: %s (%s)' % (self.samplerbox.preset, basename))
        self.samplerbox.display("L%03d" % self.samplerbox.preset)

        definitionfname = os.path.join(dirname, "definition.txt")
        # -- instrument with definition file
        if os.path.isfile(definitionfname):
            ret = self.load_samples_by_definition_file(definitionfname, dirname)
            if not ret:
                return
        # -- Instrument with samples by filename
        # -- -- found samples goes into `self.samplerbox.samples`
        else:
            for midinote in range(0, 127):
                if self.loading_interrupt:
                    return
                file = os.path.join(dirname, "%d.wav" % midinote)
                if os.path.isfile(file):
                    self.samplerbox.samples[midinote, 127] = Sound(self.samplerbox, file, midinote, 127)

        # -- create notes map from found samples keys
        initial_keys = set(self.samplerbox.samples.keys())
        for midinote in range(128):
            lastvelocity = None
            for velocity in range(128):
                # -- deduct sample from last velocity found
                if (midinote, velocity) not in initial_keys:
                    # SEGFAULT A CAUSE DE ICI PAR EX
                    self.samplerbox.samples[midinote, velocity] = lastvelocity
                else:
                    if not lastvelocity:
                        for v in range(velocity):
                            self.samplerbox.samples[midinote, v] = self.samplerbox.samples[midinote, velocity]
                    lastvelocity = self.samplerbox.samples[midinote, velocity]
            if not lastvelocity:
                for velocity in range(128):
                    try:
                        self.samplerbox.samples[midinote, velocity] = self.samplerbox.samples[midinote - 1, velocity]
                    except Exception as e:
                        pass
                        #print('Exception:', e)
        if len(initial_keys) > 0:
            print('Preset loaded: ' + str(self.samplerbox.preset))
            self.samplerbox.display("%04d" % self.samplerbox.preset)
        else:
            print('Preset empty: ' + str(self.samplerbox.preset))
            self.samplerbox.display("E%03d" % self.samplerbox.preset)
        print('Thread samples ok')
