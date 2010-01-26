
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


import logging
from google.appengine.ext import webapp
from robot import TEXTS

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



# vim: set ft=python ts=4 sw=4 expandtab :
