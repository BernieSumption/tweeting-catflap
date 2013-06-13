

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

class GPIOWatcher(object):
    
    def __init__(self, headerNo, onHigh=None, onLow=None, debounceMillis=2000):
        self.headerNo = headerNo
        self.onHigh = onHigh
        self.onLow = onLow
        self.debounceMillis = debounceMillis
        GPIO.setup(self.headerNo, GPIO.IN)
        self.last_reported_state = self.read()
    
    def read(self):
        """Return True if the GPIO header is positive, False if negative"""
        return GPIO.input(self.headerNo) == 1
    
    def enter_loop(self, intervalMillis = 100):
        """Loop endlessly, firing onHigh or onLow as states change"""
        while True:
            state = self.read()
            if state != self.last_reported_state:
                if state and self.onHigh:
                    self.onHigh()
                elif not state and self.onLow:
                    self.onLow()
                self.last_reported_state = state
            time.sleep(intervalMillis / 1000.0)

if __name__ == "__main__":
    def printMessage():
        print "Take a picture!"
    watcher = GPIOWatcher(7, onHigh=printMessage)
    print watcher.read()
    watcher.enter_loop()