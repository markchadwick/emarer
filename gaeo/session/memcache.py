# -*- coding: utf-8 -*-
#
# Copyright 2008 Lin-Chieh Shangkuan & Liang-Heng Chen
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
""" GAEO Session - memcache store """
import random
import pickle
import logging

from google.appengine.api import memcache

from gaeo import session

class MemcacheSession(session.Session):
    """ session that uses memcache """

    def __init__(self, hnd, name = 'gaeo_session', timeout = 60 * 60):
        super(MemcacheSession, self).__init__(hnd, name, timeout)

        # check from cookie
        if name in hnd.request.cookies:
            self._id = hnd.request.cookies[name]
            session_data = memcache.get(self._id)
            if session_data:
                self.update(pickle.loads(session_data))
                memcache.set(self._id, session_data, timeout)
        else:   # not in the cookie, set it
            cookie = '%s=%s' % (name, self._id)
            hnd.response.headers.add_header('Set-Cookie', cookie)

    def put(self):
        if not self._invalidated:
            memcache.set(self._id, pickle.dumps(self.copy()), self._timeout)

    def invalidate(self):
        """Invalidates the session data"""
        self._hnd.response.headers.add_header(
            'Set-Cookie',
            '%s=; expires=Thu, 1-Jan-1970 00:00:00 GMT;' % self._name
        )
        memcache.delete(self._id)
        self.clear()
        self._invalidated = True
