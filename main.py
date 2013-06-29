

from gpio_watcher import GPIOWatcher
from subprocess import call
from datetime import datetime
from grammar import Grammar
import os, shutil

def goGoPaparazzo():
    
    # time to archive the image and text
    # get a pretty date time string 
    timestamp = datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
    
    print "Activating Paparazzo at", timestamp
    
    # capture image to capture.jpg
    call(["./capture-image.sh"], shell=True)
    
    # stop here if image capture failed
    if not os.path.exists("capture.jpg"):
        print "Error - no capture.jpg recorded"
        return
    
    grammar = Grammar.from_file("demo-grammar.txt")
    message = grammar.generate()

    # post to twitter
    safeMessage = message.replace("\\", "\\\\").replace("\"", "\\\"")
    call(["./tweet.sh \"%s\"" % safeMessage], shell=True)
    
    # archive the image and text
    shutil.move("capture.jpg", "history/%s.jpg" % timestamp)
    with open("history/%s.txt" % timestamp, "w") as f:
        f.write("%s\n" % message)
    

watcher = GPIOWatcher(7, onChange=goGoPaparazzo, debounceSeconds=20)
while True:
    try:
        watcher.enter_loop()
    except Exception as e:
        print "Error:", e