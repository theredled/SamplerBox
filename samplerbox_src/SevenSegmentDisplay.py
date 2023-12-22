
#########################################
# 7-SEGMENT DISPLAY
#
#########################################
# requires: 1) i2c-dev in /etc/modules and 2) dtparam=i2c_arm=on in /boot/config.txt
#

import smbus
import time

class SevenSegmentDisplay:
    def __init__(self, samplerbox):
        self.samplerbox = samplerbox

    def init(self):
        self.bus = smbus.SMBus(1)  # using I2C
        self.samplerbox.display('----')
        time.sleep(0.5)

    def display(self, s):
        for k in '\x76\x79\x00' + s:  # position cursor at 0
            try:
                self.bus.write_byte(0x71, ord(k))
            except:
                try:
                    self.bus.write_byte(0x71, ord(k))
                except:
                    pass
            time.sleep(0.002)