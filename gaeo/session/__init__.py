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
""" GAEO Session package """
import logging
from random import choice
from string import digits, letters

SESSIONID_LEN = 64
POOL = digits + letters

class Session(dict):
    """ Session is an abstract class that declares sessions basic
    operations. """

    def __init__(self, hnd, name, timeout):
        """The Session's constructor.

        @param hnd      The webapp.ReqeustHanlder object.
        @param name     The session name.
        @param timeout  The time interval (in sec) that the session expired.
        """

        dict.__init__(self)
        self._name = name
        self._hnd = hnd
        self._timeout = timeout
        self._id = ''.join([ choice(POOL) for i in range(SESSIONID_LEN) ])

        self._invalidated = False

    def save(self):
        pass

    def invalidate(self):
        pass
