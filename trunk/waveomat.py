# -*- coding: utf-8 -*-

from waveapi import events
from waveapi import model
from waveapi import robot

import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

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
    #if (randint(0,10) % 3 == 0):
    Notify(context)

def Notify(context):
    #text = TEXTS[randint(0,len(TEXTS)-1)]
    text = TEXTS[-1]

    root_wavelet = context.GetRootWavelet()
    root_wavelet.CreateBlip().GetDocument().SetText(text)

class RobotExternalHandler(webapp.RequestHandler):
  """Handler for serving extertnal requests"""

  def __init__(self, robot):
    """Initializes this handler with a specific robot."""
    self._robot = robot

  def get(self):
    """Handles HTTP GET request."""
    global TEXTS
    new_text = self.request.get("text", "default")
    logging.info("current text: %s, \n new text: %s" % (self._robot.text, new_text))
    TEXTS.append(self.request.get("text", "default"))
    print 'Content-Type: text/plain'
    print ''
    print TEXTS


class WaveomatRobot(robot.Robot):

  text = "initial text"

  def Run(self, debug=False):
    """Sets up the webapp handlers for this robot and starts listening.

    Args:
      debug: Optional variable that defaults to False and is passed through
          to the webapp application to determine if it should show debug info.
    """
    # App Engine expects to construct a class with no arguments, so we
    # pass a lambda that constructs the appropriate handler with
    # arguments from the enclosing scope.
    logging.info("robot is running")
    app = webapp.WSGIApplication([
        ('/_wave/capabilities.xml', lambda: robot.RobotCapabilitiesHandler(self)),
        ('/_wave/robot/profile', lambda: robot.RobotProfileHandler(self)),
        ('/_wave/robot/jsonrpc', lambda: robot.RobotEventHandler(self)),
        ('/_wave/text', lambda: RobotExternalHandler(self)),
    ], debug=debug)
    run_wsgi_app(app)


if __name__ == '__main__':
    logging.info("main neu")
    myRobot = WaveomatRobot('waveomat', 
        image_url='http://waveomat.appspot.com/icon.png',
        version='11',
        profile_url='http://waveomat.appspot.com/')
    myRobot.RegisterHandler(events.WAVELET_PARTICIPANTS_CHANGED, OnParticipantsChanged)
    myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)
    myRobot.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSubmitted)
    myRobot.Run()
