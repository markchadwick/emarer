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

""" The gaeo library package. """

import re

from google.appengine.ext import webapp

from gaeo.dispatch import dispatcher


class Config:
    """ The singleton of GAEO's configuration """

    class __impl:
        def __init__(self):
            self.template_dir = ''
            self.session_store = 'memcache'
            self.app_name = ''

    __instance = None

    def __init__(self):
        if Config.__instance is None:
            Config.__instance = Config.__impl()

        self.__dict__['_Config__instance'] = Config.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)


class MainHandler(webapp.RequestHandler):
    """Handles all requests
    """
    def get(self, *args):
        self.__process_request()

    def post(self, *args):
        self.__process_request()
        
    def head(self, *args):
        self.__process_request()
        
    def options(self, *args):
        self.__process_request()
        
    def put(self, *args):
        self.__process_request()
        
    def delete(self, *args):
        self.__process_request()
        
    def trace(self, *args):
        self.__process_request()

    def __process_request(self):
        """dispatch the request"""
        dispatcher.dispatch(self)

