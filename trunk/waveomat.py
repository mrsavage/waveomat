# -*- coding: utf-8 -*-

from waveapi import events

import logging

from google.appengine.ext import webapp

from robot import WaveomatRobot
from robot import OnParticipantsChanged, OnRobotAdded, OnBlipSubmitted


if __name__ == '__main__':
    logging.debug("waveomat.py __main__")
    myRobot = WaveomatRobot('waveomat', 
        image_url='http://waveomat.appspot.com/icon.png',
        version='14',
        profile_url='http://waveomat.appspot.com/')
    myRobot.RegisterHandler(events.WAVELET_PARTICIPANTS_CHANGED, OnParticipantsChanged)
    myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)
    myRobot.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSubmitted)
    myRobot.Run()
