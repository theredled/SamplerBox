import traceback


class PlayingSound:
    def __init__(self, samplerbox, sound, note):
        self.samplerbox = samplerbox
        self.sound = sound
        self.pos = 0
        self.fadeoutpos = 0
        self.isfadeout = False
        self.note = note

    def fadeout(self, i):
        self.isfadeout = True

    def stop(self):
        try:
            self.samplerbox.playing_sounds.remove(self)
        except Exception as e:
            print('exception:', traceback.print_exception(e))
