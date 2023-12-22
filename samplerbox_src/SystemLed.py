import os

class SystemLed:
    def __init__(self, samplerbox):
        self.samplerbox = samplerbox

    def init(self):
        os.system("modprobe ledtrig_heartbeat")
        os.system("echo heartbeat >/sys/class/leds/led0/trigger")
