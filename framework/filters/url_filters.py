from google.appengine.ext.webapp import template
from django.template import Node
from django.template import resolve_variable
from framework.routes.util import url_for as route_for

import logging

register = template.create_template_register()
  
class UrlNode(Node):
    def __init__(self, controller, id=None, action=None):
        self.controller = controller
        self.id = id
        self.action = action
  
    def render(self, context):
        controller = resolve_variable(self.controller, context)
        
        params = {}
        if self.id is not None:
            id = resolve_variable(self.id, context)
            
            if self.action is not None:
                action = resolve_variable(self.action, context)
                return route_for(controller, action=action, id=id)
            else:
                return route_for(controller, id=id)
        else:
            return route_for(controller)
      
def url_for(parser, token):
    tokens = list(token.split_contents())
    
    return UrlNode(*tokens[1:])
  

register.tag(url_for)