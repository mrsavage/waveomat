# -*- coding: utf-8 -*-
#
# File: .py
#
# Copyright (c) InQuant GmbH
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

__author__ = """Hans-Peter Locher <hans-peter.locher@inquant.de>"""
__docformat__ = 'plaintext'


TEXTS = ["""Hi, I'm the waveomat.
          To change what I'm saying use following url: 
          http://waveomat.appspot.com/_wave/text?text=whateveryouwant
         """,
         ]


import logging
from waveapi import robot
import web

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


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
    Notify(context)

def Notify(context):
    text = TEXTS[-1]

    root_wavelet = context.GetRootWavelet()
    root_wavelet.CreateBlip().GetDocument().SetText(text)

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
        ('/_wave/text', lambda: web.RobotExternalHandler(self)),
    ], debug=debug)
    run_wsgi_app(app)


# vim: set ft=python ts=4 sw=4 expandtab :
