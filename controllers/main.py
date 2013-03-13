"""
Main page controller.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'

import pages
import webapp2

PAGE_URI = '/main'

class MainHandler(webapp2.RequestHandler):
    def get(self):
        view = pages.render_view(PAGE_URI)
        pages.render_page(self, view)