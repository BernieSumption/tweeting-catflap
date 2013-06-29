

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

class GPIOWatcher(object):
    
    def __init__(self, headerNo, onChange=None, debounceSeconds=2):
        """
        headerNo - the physical pin number of the GPIO header
        callback - a function called when a change is observed
        debounceSeconds - don't fire a change event if one has been fired within this time
        """
        self.headerNo = headerNo
        self.onChange = onChange
        self.debounceSeconds = debounceSeconds
        self.lastEventTime = 0
        GPIO.setup(self.headerNo, GPIO.IN)
        self.last_reported_state = self.read()
    
    def read(self):
        """Return True if the GPIO header is positive, False if negative"""
        return GPIO.input(self.headerNo) == 1
    
    def enter_loop(self, pollingIntervalSeconds = 0.1):
        """Loop endlessly, firing onChange as states change"""
        while True:
            state = self.read()
            if state != self.last_reported_state:
                self.last_reported_state = state
                timeNow = time.time()
                if timeNow > self.lastEventTime + self.debounceSeconds:
                    self.onChange()
                    self.lastEventTime = timeNow
            time.sleep(pollingIntervalSeconds)

if __name__ == "__main__":
    def printMessage():
        print "Change detected!"
    watcher = GPIOWatcher(7, onChange=printMessage)
    watcher.enter_loop()