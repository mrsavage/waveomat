# -*- coding: utf-8 -*-

from waveapi import events
from waveapi import model
from waveapi import robot

from random import randint

TEXTS = [u"Da krieg ich Puls!",
         u"Geht nich, ich hab gleich Telko.",
         u"Ist der Rundel da?",
         u"Ich kann so nicht arbeiten...",
         u"Deine Leistung könnte besser"]


def OnParticipantsChanged(properties, context):
    """Invoked when any participants have been added/removed."""
    added = properties['participantsAdded']
    for p in added:
        Notify(context)

def OnRobotAdded(properties, context):
    """Invoked when the robot has been added."""
    Notify(context)

def OnBlipSubmitted(properties, context):
    """Invoked when the document has been changed."""
    if randint(0,1):
        Notify(context)

def Notify(context):
    text = TEXTS[randint(0,len(TEXTS)-1)]
    root_wavelet = context.GetRootWavelet()
    root_wavelet.CreateBlip().GetDocument().SetText(text)

if __name__ == '__main__':
    myRobot = robot.Robot('waveomat', 
        image_url='http://waveomat.appspot.com/icon.png',
        version='7',
        profile_url='http://waveomat.appspot.com/')
    myRobot.RegisterHandler(events.WAVELET_PARTICIPANTS_CHANGED, OnParticipantsChanged)
    myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)
    myRobot.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSubmitted)
    myRobot.Run()
