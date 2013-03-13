#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import datetime
import os
import jinja2
import json
import logging
import webapp2

from google.appengine.ext import db
from authentication import auth
from authentication.gaesessions import get_current_session

JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))




class StickyNotesHandler(webapp2.RequestHandler):
    def get(self):
        session = get_current_session()
        if not session.has_key('net_id'):
            auth.require_login(self)
        user = get_user(session['net_id'], create=True)
        stickies = Sticky.gql('WHERE user=:1', user)
        stickies_data = []
        for sticky in stickies:
            stickies_data.append({
                    'id': str(sticky.key()),
                    'title': sticky.title,
                    'note': sticky.note
                })


        page_data = {'stickies': stickies_data}
        template = JINJA_ENV.get_template('stickies.html')
        self.response.out.write(template.render(page_data))

    def post(self):
        session = get_current_session()
        if not session.has_key('net_id'):
            return
        user = get_user(session['net_id'])
        data = json.loads(self.request.get('json'))
        logging.info(data)
        sticky = Sticky(user=user.key(),
                        title=data['title'],
                        note=data['note'])
        sticky.put()
        data['id'] = str(sticky.key())
        self.response.out.write(json.dumps(data))

class GarbageHandler(webapp2.RequestHandler):
    def post(self):
        session = get_current_session()
        if not session.has_key('net_id'):
            return
        user = get_user(session['net_id'])
        logging.info(user)
        sticky_id = self.request.get('id')
        logging.info(sticky_id)
        sticky = Sticky.get(sticky_id)
        logging.info(sticky.user)
        assert sticky.user.key() == user.key()
        sticky.delete()
        self.response.out.write('Success!')
