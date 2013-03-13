"""
Stickies page controller.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'

import json
import logging
import pages
import webapp2

from authentication import auth

import models.sticky

PAGE_URI = '/stickies'

class StickyNotesHandler(webapp2.RequestHandler):
    def get(self):
        user = auth.require_login(self)
        stickies = models.sticky.get_stickies(user)
        view = pages.render_view(PAGE_URI, {'stickies': stickies})
        pages.render_page(self, view)

    def post(self):
        # Authenticate user
        user = auth.get_logged_in_user()
        if not user:
            return      # Should return error message here

        # Create sticky
        data = json.loads(self.request.get('data'))
        logging.info('Sticky Post: %s', data)
        sticky = models.sticky.create_sticky(user, data)

        # Respond
        data['id'] = str(sticky.key())
        self.response.out.write(json.dumps(data))


class GarbageHandler(webapp2.RequestHandler):
    def post(self):
        # Authenticate user
        user = auth.get_logged_in_user()
        if not user:
            return      # Should return error message here

        sticky_id = self.request.get('id')
        sticky = models.sticky.get_sticky(sticky_id)

        # Make sure the user is not trying to delete someone else's sticky
        assert sticky.user.key() == user.key()

        models.sticky.delete_sticky(sticky)
        self.response.out.write('Success!')