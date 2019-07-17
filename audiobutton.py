#!/usr/bin/python
# coding: utf-8

import RPi.GPIO as GPIO
from subprocess import call
from datetime import datetime
import time
#import os

LanguageAll = ['uk', 'ru']
pathToConfig = '~/MagicMirror/config/config.js.sample'
pathToAudio = '~/btn_onoff/audio/'

# waking / powering up Raspberry Pi when button is pressed
shutdownPin = 3

# if button pressed for at least this long then reboot. if less then shut down.
rebootMinSeconds = 3

# button debounce time in seconds
debounceSeconds = 0.01

GPIO.setmode(GPIO.BCM)
GPIO.setup(shutdownPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

buttonPressedTime = None


if __name__ == '__main__':
    # subscribe to button presses
    GPIO.add_event_detect(shutdownPin, GPIO.BOTH, callback=buttonStateChanged)

    f = open(pathToConfig)
    language = 'language'
    line = f.readline()
    global find
    while line:
        if language in line:
            print(line)
            for i in LanguageAll:
                if i in line:
                    find = i
                    break
            print(find)
            break
        line = f.readline()

    while True:
        # sleep to reduce unnecessary CPU usage
        time.sleep(5)


def buttonStateChanged(pin):
    global buttonPressedTime

    if not (GPIO.input(pin)):
        # button is down
        if buttonPressedTime is None:
            buttonPressedTime = datetime.now()
    else:
        # button is up
        if buttonPressedTime is not None:
            elapsed = (datetime.now() - buttonPressedTime).total_seconds()
            buttonPressedTime = None
            if elapsed >= rebootMinSeconds:
                call(['omxplayer', '--adev',  'local', pathToAudio + find + '/reboot.wav'], shell=False)
                #os.system('omxplayer ' + pathToAudio + find + '/reboot.wav')
                call(['shutdown', '-r', 'now'], shell=False)
            elif elapsed >= debounceSeconds:
                call(['omxplayer', '--adev', 'local', pathToAudio + find + '/shutdown.wav'], shell=False)
                call(['shutdown', '-h', 'now'], shell=False)
