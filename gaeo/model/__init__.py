# -*- coding: utf-8 -*-
#
# Copyright 2008 GAEO Team.
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
"""GAEO model package
"""
import re

from google.appengine.ext import db

def pluralize(noun):
    if re.search('[sxz]$', noun):
        return re.sub('$', 'es', noun)
    elif re.search('[^aeioudgkprt]h$', noun):
        return re.sub('$', 'es', noun)
    elif re.search('[^aeiou]y$', noun):
        return re.sub('y$', 'ies', noun)
    else:
        return noun + 's'

class BaseModel(db.Model):
    """BaseModel is the base class of data model."""

    @classmethod
    def belongs_to(cls, ref_cls):
        """ Declare a many-to-one relationship """
        if ref_cls is None:
            raise Exception('No referenced class')
        
        ref_name = ref_cls.__name__.lower()
        if ref_name not in cls._properties:
            attr = db.ReferenceProperty(ref_cls, collection_name=pluralize(cls.__name__.lower()))
            cls._properties[ref_name] = attr
            attr.__property_config__(cls, ref_name)

    @classmethod
    def has_and_belongs_to_many(cls, ref_cls):
        if ref_cls is None:
            raise Exception('No referenced class')
        
        f_name = pluralize(cls.__name__.lower())
        t_name = pluralize(ref_cls.__name__.lower())
        
        if t_name not in cls._properties:
            attr = db.ListProperty(db.Key)
            cls._properties[t_name] = attr
            attr.__property_config__(cls, t_name)
        if f_name not in ref_cls._properties:
            attr = property(lambda self: cls.gql('WHERE %s = :1' % t_name, self.key()))
            ref_cls._properties[f_name] = attr
            attr.__property_config__(ref_cls, f_name)
    
    @classmethod
    def named_scope(cls, name, order_by=None, **conds):
        if name not in cls._properties:
            cond_str = "WHERE "
            for cond in conds.iterkeys():
                if len(cond_str) > 6:
                    cond_str += ' AND '
                cond_str += '%s %s' % (cond, conds[cond])
                
            if order_by:
                cond_str += ' ORDER BY %s' % order_by
                
            attr = property(lambda self: cls.gql(cond_str))
            cls._properties[name] = attr
            attr.__property_config__(cls, name)
    
    def update_attributes(self, kwd_dict = {}, **kwds):
        """Update the specified properties"""
        need_change = False
        
        # if user passed a dict, merge to kwds (Issue #3)
        if kwd_dict:
            kwd_dict.update(kwds)
            kwds = kwd_dict
        
        props = self.properties()
        for prop in props.values():
            if prop.name in kwds:
                if not need_change:
                    need_change = True
                prop.__set__(self, kwds[prop.name])
        
        if need_change:
            self.update()

    def set_attributes(self, kwd_dict = {}, **kwds):
        """set the specified properties, but not update"""
        
        # Issue #3
        if kwd_dict:
            kwd_dict.update(kwds)
            kwds = kwd_dict
        
        props = self.properties()
        for prop in props.values():
            if prop.name in kwds:
                prop.__set__(self, kwds[prop.name])
        
    def save(self):
        self.put()
        
    def update(self):
        self.put()
        
