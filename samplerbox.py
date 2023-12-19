#
#  SamplerBox
#
#  author:    Joseph Ernest (twitter: @JosephErnest, mail: contact@samplerbox.org)
#  url:       http://www.samplerbox.org/
#  license:   Creative Commons ShareAlike 3.0 (http://creativecommons.org/licenses/by-sa/3.0/)
#
#  samplerbox.py: Main file (now requiring at least Python 3.7)
#

import rtmidi, time
import src.samplerbox as samplerbox

midi_in = [rtmidi.MidiIn()]
previous = []
while True:
    all_ports = midi_in[0].get_ports()
    for num_port,port in enumerate(all_ports):
        if port not in previous and 'Midi Through' not in port:
            midi_in.append(rtmidi.MidiIn())
            midi_in[-1].set_callback(samplerbox.MidiCallback)
            midi_in[-1].open_port(num_port)
            print('Opened MIDI: ' + str(port))
    previous = all_ports
    time.sleep(2)
