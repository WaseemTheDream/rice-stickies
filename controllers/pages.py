"""
Controller for web app and page rendering tasks.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'

import os
import jinja2


CONTROLLERS_DIR = os.path.dirname(__file__)
VIEWS_DIR = os.path.join(CONTROLLERS_DIR, '../views')
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(VIEWS_DIR))


def render_view(view_uri, view_data={}):
    """
    Renders the specified view.

    Args:
        view_uri: the uri of the view without .html extension
        view_data: a dictionary containing the template values for the page
    """
    try:
        view = JINJA_ENV.get_template(view_uri + '.html').render(view_data)
    except jinja2.TemplateNotFound:
        view = JINJA_ENV.get_template('templates/not-found.html').render()
    return view


def render_page(handler, content):
    """
    Renders a page with the specified content.

    Args:
        handler: the webapp2 request handler used to request the page
        content: a rendered view
    """
    page = JINJA_ENV.get_template('templates/page.html')
    handler.response.out.write(page.render({'content': content}))