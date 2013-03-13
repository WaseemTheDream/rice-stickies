"""
Model definition and functions for stickies.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'

from google.appengine.ext import db
from users import User

class Sticky(db.Model):
    user = db.ReferenceProperty(User,
                                required=True)
    time_added = db.DateTimeProperty(auto_now=True)
    title = db.StringProperty(required=True)
    note = db.TextProperty()

    def to_json():
        return {
            'id': str(self.key()),
            'title': self.title,
            'note': self.note
        }


def create_sticky(user, sticky):
    sticky = Sticky(
        user=user.key(),
        title=sticky['title'],
        note=sticky['note'])
    sticky.put()
    return sticky

def get_sticky(key):
    return Sticky.get(key)

def delete_sticky(sticky):
    # Refactored into this method incase there are other things to be done
    # before deleting a sticky
    sticky.delete()

def get_stickies(user):
    return [sticky.to_json() for sticky in Sticky.gql('WHERE user=:1', user)]