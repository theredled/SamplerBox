import time, threading
import RPi.GPIO as GPIO

#########################################
# BUTTONS (RASPBERRY PI GPIO)
#
#########################################
class GpioButtons:
    def __init__(self, samplerbox):
        self.samplerbox = samplerbox
        self.lastbuttontime = 0

    def buttons_callback(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        while True:
            now = time.time()
            if not GPIO.input(18) and (now - self.lastbuttontime) > 0.2:
                lastbuttontime = now
                self.samplerbox.preset -= 1
                if self.samplerbox.preset < 0:
                    self.samplerbox.preset = 127
                self.samplerbox.LoadSamples()
            elif not GPIO.input(17) and (now - self.lastbuttontime) > 0.2:
                lastbuttontime = now
                self.samplerbox.preset += 1
                if self.samplerbox.preset > 127:
                    self.samplerbox.preset = 0
                self.samplerbox.LoadSamples()
            time.sleep(0.020)

    def init(self):
        ButtonsThread = threading.Thread(target=self.buttons_callback)
        ButtonsThread.daemon = True
        ButtonsThread.start()