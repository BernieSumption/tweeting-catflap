

from gpio_watcher import GPIOWatcher
from subprocess import call
from datetime import datetime
from grammar import Grammar
import os

from twython import Twython
import sys

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
	twitter = Twython(
		app_key = 'uS6hO2sV6tDKIOeVjhnFnQ',
		app_secret = 'MEYTOS97VvlHX7K1rwHPEqVpTSqZ71HtvoK4sVuYk',
		oauth_token = '1334844578-z3Ju3FUAQKZKogQnK7kbqngeeSQxX1wkeGwRiey',
		oauth_token_secret = 'HD1w0jh2x2nxAcgPI6Cux1SKbxI0VxaQYHvNZn8dGxQ'
	)
	twitter.update_status_with_media(status=message, media=open("capture.jpg", 'rb'))

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