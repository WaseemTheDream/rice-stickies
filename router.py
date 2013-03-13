"""
Module for routing web requests to the correct controllers.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'


import webapp2
from controllers import main, stickies


app = webapp2.WSGIApplication([
    ('/stickies', stickies.StickyNotesHandler),
    ('/stickies/delete', stickies.GarbageHandler),
    ('/.*', main.MainHandler)
], debug=True)