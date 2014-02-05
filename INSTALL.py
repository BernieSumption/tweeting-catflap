# Lines starting '>' are unix commands

# EXPAND SD CARD SIZE
#
> raspi-config
(In raspi-config, expand the disk to use the full SD card)

# INSTALL DEPENDENCIES
#
> sudo apt-get install python-pip mercurial fswebcam
> sudo pip install twitter requests requests_oauthlib RPi.GPIO argparse

# GET SOURCE CODE
#
> cd ~/Desktop
> hg clone https://bitbucket.org/berniecode/rpi-paparazzo
> cd rpi-paparazzo


# AUTHORISE TWITTER
#
> twitter set foo
# ^ this leads you through the OAuth dance in your browser
> cat ~/.twitter_oauth
# ^ this prints out two lines. The first line is the OAuth token, the second the OAuth secret

# now create the file settings.py, with this content:

app_key = 'uS6hO2sV6tDKIOeVjhnFnQ'
app_secret = 'MEYTOS97VvlHX7K1rwHPEqVpTSqZ71HtvoK4sVuYk'
oauth_token = 'paste first line here'
oauth_token_secret = 'paste second line here'

# INSTALL THE ALARM SENSOR
#
# Connect the burglar alarm to the high, low and pin 7 GPIO pins. The sensor should use
# resistors to prevent excessive current flow, and should pull pin 7 low when the door is
# closed and high when it's open.

# TEST IT.
#

./capture.sh
# ^ this should capture an image from the webcam and save it as capture.jpg.
# If it doesn't, figure out why. You're on your own here, webcams on linux are tricksome

sudo python main.py --test
# ^ this should post a single message to twitter with a photo

sudo python main.py
# ^ this should enter a loop, posting a message whenever the door sensor is opened

# INSTALL A CRON SCRIPT
#
> crontab -e
# then add this line:
@reboot /path to rpi-paparazzo folder/startup.sh
