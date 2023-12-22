#########################################
# MIDI IN via SERIAL PORT
#
#########################################

import serial
import threading

class SerialPortMidi:
    def __init__(self, samplerbox):
        self.samplerbox = samplerbox

    def init(self):
        self.ser = serial.Serial('/dev/ttyAMA0', baudrate=31250)
        MidiThread = threading.Thread(target=self.midi_serial_callback)
        MidiThread.daemon = True
        MidiThread.start()

    def midi_serial_callback(self):
        message = [0, 0, 0]
        while True:
            i = 0
            while i < 3:
                data = ord(self.ser.read(1))  # read a byte
                if data >> 7 != 0:
                    i = 0  # status byte!   this is the beginning of a midi message: http://www.midi.org/techspecs/midimessages.php
                message[i] = data
                i += 1
                if i == 2 and message[0] >> 4 == 12:  # program change: don't wait for a third byte: it has only 2 bytes
                    message[2] = 0
                    i = 3
            self.samplerbox.midi_callback(message, None)