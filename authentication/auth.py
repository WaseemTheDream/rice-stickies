"""
Application specific authentication module.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'


import logging
import re
import urllib
import webapp2

from gaesessions import get_current_session

CAS_SERVER  = "https://netid.rice.edu"


class LoginResponseHandler(webapp2.RequestHandler):
    """Receive the response from CAS after the user authentication."""

    def get(self):
        ticket = self.request.get('ticket')

        if not ticket:
            self.response.out.write('Ticket not specified.')
            return

        net_id = self.validate_cas_2()
        if not net_id:
            self.response.out.write('Invalid ticket. Credentials not verified.')
            return

        # Close any active session the user has since credentials have been freshly verified.
        session = get_current_session()
        if session.is_active():
            session.terminate()

        # Start a session for the user
        session['net_id'] = net_id

        destination_url = str(self.request.get('destination'))
        if not destination_url:
            self.response.out.write('User authenticated. However, no destination '
                              'url is provided.')
            return

        logging.info('Redirecting to %s', destination_url)
        self.redirect(destination_url)

    def validate_cas_2(self):
        """
        Validate the given ticket using CAS 2.0 protocol.

        Returns:
            net_id {String}: the id of the user. None if ticket invalid.
        """
        ticket = self.request.get('ticket')
        service_url = self.remove_parameter_from_url(self.request.url, 'ticket')        # Strip ticket parameter
        cas_validate = CAS_SERVER + '/cas/serviceValidate?ticket=' + ticket + '&service=' + service_url

        # Ask CAS server whether this ticket is valid
        f_validate = urllib.urlopen(cas_validate)

        # Get the first line - should be yes or no
        response = f_validate.read()
        net_id = self.parse_tag(response, 'cas:user')
        if not net_id:
            logging.info('Invalid ticket.')
            return None

        logging.info('Ticket validated for %s', net_id)
        return net_id

    @staticmethod
    def parse_tag(string, tag):
        """
        Used for parsing XML. Searches the string for first occurrence of <tag>...</tag>.

        Returns:
            The trimmed text between tags. "" if tag is not found.
        """
        tag1_pos1 = string.find("<" + tag)
        #  No tag found, return empty string.
        if tag1_pos1==-1: return ""
        tag1_pos2 = string.find(">",tag1_pos1)
        if tag1_pos2==-1: return ""
        tag2_pos1 = string.find("</" + tag,tag1_pos2)
        if tag2_pos1==-1: return ""
        return string[tag1_pos2+1:tag2_pos1].strip()

    @staticmethod
    def remove_parameter_from_url(url, parameter):
        """
        Removes the specified parameter from the url. Returns url as is if parameter doesn't exist.

        Args:
            url {String}: input url
            parameter {String}: parameter to remove.
        Returns:
            {String}: url with ticket parameter removed.
        """
        return re.sub('&%s(=[^&]*)?|%s(=[^&]*)?&?' % (parameter, parameter), '', url)


class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        """Logs out the user from CAS."""
        session = get_current_session()
        if session.has_key('net_id'):
            session.terminate()
        else:
            self.response.out.write('You weren\'t logged in.')
            return
        app_url = self.request.headers.get('host', 'no host')    # URL of the app itself
        destination = self.request.get('destination')
        logging.info(destination)
        if not destination:
            service = 'http://%s/authenticate/logout-response' % app_url
        else:
            service = str('http://%s/%s' % (app_url, destination))
        self.redirect(CAS_SERVER + '/cas/logout?service=' + service)


class LogoutResponseHandler(webapp2.RequestHandler):
    def get(self):
        """Logs out the user."""
        self.response.out.write('You\'ve been logged out. See you again soon!')
        


def require_login(request_handler):
    """
    Requires the user to be logged in through NetID authentication.

    Args:
        request_handler: webapp2 request handler of the user request
    """
    destination_url = request_handler.request.url
    app_url = request_handler.request.headers.get('host', 'no host')    # URL of the app itself
    service_url = 'http://%s/authenticate/login-response' % app_url
    cas_url = CAS_SERVER + '/cas/login?service=' + service_url + '?destination=' + destination_url
    request_handler.redirect(cas_url, abort=True)

app = webapp2.WSGIApplication([
    ('/authenticate/login-response', LoginResponseHandler),
    ('/authenticate/logout', LogoutHandler),
    ('/authenticate/logout-response', LogoutResponseHandler)
], debug=True)

