
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
  """Handler for serving external requests"""

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

class RobotFrontPageHandler(webapp.RequestHandler):
  """Handler for frontpage"""

  def __init__(self, robot):
    """Initializes this handler with a specific robot."""
    self._robot = robot

  def get(self):
    """Handles HTTP GET request."""
    html = """
              <html>
                <body>
                    <h1>waveomat</h1>
                    <p>Welcome to the waveomat, a robot for 
                    <a href="https://wave.google.com/wave/">Google Wave</a>
                    </p>
                    <h2>Usage:</h2>
                    <p>waveomat blogs into your wave whenever a 
                    <a href="http://google.about.com/od/b/g/google_wave_blip.htm">blip</a>
                    is submitted.
                    </p>
                    <p>To add waveomat to your wave, invite <b>waveomat@appspot.com</b> 
                    to your wave.
                    </p>
                    <p>You can change what waveomat says using this url:</p>
                    <pre>
                       http://waveomat.appspot.com/_wave/text?text=whateveryouwant
                    </pre>
                    <p>Currently, he says:</p>
                    <pre>
                    %s
                    </pre>
                    <h2>Who? How?</h2>
                    <p>waveomat was implemented at the <a href="http://code.google.com/p/snowsprint2010/">Snowsprint 2010</a>
                    <p>The code lives <a href="http://code.google.com/p/waveomat/">here</a>.
                    <p>Contributors:</p>
                    <ul>
                        <li>Hans-Peter Locher (Author) <a href="http://www.inquant.de">InQuant GmbH</a></li>
                    </ul>
                  </form>
                </body>
              </html>""" % TEXTS[-1]

    self.response.out.write(html)

# vim: set ft=python ts=4 sw=4 expandtab :
