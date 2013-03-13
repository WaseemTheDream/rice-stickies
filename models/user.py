"""
Model definition and functions for users.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'

from google.appengine.ext import db

class User(db.Model):
    net_id = db.StringProperty(required=True)


def get_user(net_id, create=False):
    user = User.gql('WHERE net_id=:1', net_id).get()
    if not user and create:
        user = User(net_id=net_id).put()
    return user