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

import re
from copy import copy
import logging

class RuleError(Exception):
    """Base Error"""

class RuleNoControllerError(RuleError):
    """No controller"""

class Rule(object):
    """ Handles each routing rule. """
    def __init__(self, pattern, **param):
        super(Rule, self).__init__()

        self.pattern = pattern[:-1] if pattern.endswith('/') else pattern
        self.regex = self.pattern
        self.param = param
        self.matches = re.findall(':([^/\.]+)', self.pattern)

        for i in range(len(self.matches)):
            self.regex = self.regex.replace(':' + self.matches[i], '([^/\.]+)')
            self.param[self.matches[i]] = i
        self.validate()

    def __eq__(self, other):
        return self.regex == other.regex

    def __getattr__(self, attr):
        try:
            return getattr(self, 'param')[attr]
        except KeyError:
            raise AttributeError, attr

    def __str__(self):
        from operator import itemgetter
        return ', '.join(['%s: %s' % (k, v) for k, v in \
            sorted(self.param.items(), key = itemgetter(1))])

    def match_url(self, url):
        if url.endswith('/'):
            url = url[:-1]
        try:
            mat = re.findall(self.regex, url)[0]
        except IndexError:
            return None

        param = copy(self.param)
        if isinstance(mat, basestring):
            if self.matches:
                param[self.matches[0]] = mat
        elif isinstance(mat, tuple):
            for i in range(len(mat)):
                param[self.matches[i]] = mat[i]

        return param

    def url_for(self, controller, **param):
        param['controller'] = controller
        url = self.pattern
        for match in self.matches:
            if match not in param:
                return None
            url = url.replace(':' + match, str(param[match]))
            del param[match]

        # extra parameters
        ep = '&'.join(['%s=%s' % (k, v) for k, v in param.items() if k not in self.param])

        return url + '?' + ep if ep else url

    def validate(self):
        if 'controller' not in self.param:
            raise RuleNoControllerError

        if 'action' not in self.param:
            self.param['action'] = 'index'

        if not self.regex.startswith('^'):
            self.regex = '^' + self.regex
        if not self.regex.endswith('$'):
            self.regex = self.regex + '$'


class Router:
    """ Handles the url routing... """

    class __impl:
        def __init__(self):
            self.__routing_root = {
                'controller': 'welcome',
                'action': 'index',
            }
            self.__routing_table = []
            # used to store default pattern (but match last)
            self.__routing_table_fallback = [
                Rule('/:controller/:action'),
                Rule('/:controller')
            ]

        def connect(self, pattern, **tbl):
            """ Add routing pattern """

            rule = Rule(pattern, **tbl)
            if rule not in self.__routing_table:
                self.__routing_table.append(rule)

        def disconnect(self, pattern):
            rule = Rule(pattern)
            if rule in self.__routing_table:
                self.__routing_table.remove(rule)

        def root(self, **map):
            """ Set the root (/) routing... """
            self.__routing_root['controller'] = \
                map.get('controller', self.__routing_root['controller'])
            self.__routing_root['action'] = \
                map.get('action', self.__routing_root['action'])

        def resolve(self, url):
            """ Resolve the url to the correct mapping """

            if url == '/':
                return self.__routing_root

            ret = self.__resolve_by_table(url, self.__routing_table)
            if ret is None: # fallback
                ret = self.__resolve_by_table(url, self.__routing_table_fallback)
            return ret

        def __resolve_by_table(self, url, rules):
            """ Resolve url by the given table """
            for r in rules:
                ret = r.match_url(url)
                if ret:
                    return ret
            return None

        def url_for(self, controller, **param):
            for r in self.__routing_table:
                ret = r.url_for(controller, **param)
                if ret:
                    return ret
            return None

    __instance = None

    def __init__(self):
        if Router.__instance is None:
            Router.__instance = Router.__impl()
        self.__dict__['_Router__instance'] = Router.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)

