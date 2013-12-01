

from subprocess import call
from datetime import datetime
from grammar import Grammar
import os, shutil

from twython import Twython
import sys

try:
    import settings
except ImportError:
    print "Could not import settings module, did you create one?"
    exit()

try:
    from gpio_watcher import GPIOWatcher
except ImportError:
    print "Import GPIOWatcher failed, the script will only work in test mode"


def goGoPaparazzo():
    
    # time to archive the image and text
    # get a pretty date time string 
    timestamp = datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
    
    print "Activating Paparazzo at", timestamp
    
    grammar = Grammar.from_file("grammar.txt")
    while True:
        message = grammar.generate()
        if len(message) < 140:
            break
    print "Message:", message
    
    # capture image to capture.jpg
    call(["./capture-image.sh"], shell=True)
    
    # stop here if image capture failed
    if not os.path.exists("capture.jpg"):
        print "Error - no capture.jpg recorded"
        return

    # post to twitter
    twitter = Twython(
        app_key = settings.app_key,
        app_secret = settings.app_secret,
        oauth_token = settings.oauth_token,
        oauth_token_secret = settings.oauth_token_secret
    )
    twitter.update_status_with_media(status=message, media=open("capture.jpg", 'rb'))

    # archive the image and text
    shutil.move("capture.jpg", "history/%s.jpg" % timestamp)
    with open("history/%s.txt" % timestamp, "w") as f:
        f.write("%s\n" % message)
    


if __name__ == "__main__":
    if "--test" in sys.argv:
        goGoPaparazzo()
    else:
        watcher = GPIOWatcher(7, onChange=goGoPaparazzo, debounceSeconds=20)
        while True:
            try:
                watcher.enter_loop()
            except Exception as e:
                print "Error:", e