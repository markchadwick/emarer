from google.appengine.ext import webapp
register = webapp.template.create_template_register()

# ------------------------------------------------------------------------------
# Javascript Utils
# ------------------------------------------------------------------------------

_js_escapes = (
    ('\\', '\\\\'), 
    ('"', '\\"'), 
    ("'", "\\'"), 
    ('\n', '\\n'), 
    ('\r', '\\r'), 
    ('\b', '\\b'), 
    ('\f', '\\f'), 
    ('\t', '\\t'), 
    ('\v', '\\v'), 
    ('</', '<\\/'), 
)
 
def escapejs(value): 
    """
    Backslash-escapes characters for use in JavaScript strings.
    """
    if not value or value == 'None':
        return ''
        
    for bad, good in _js_escapes:
        value = value.replace(bad, good) 
    return value 
escapejs = register.filter(escapejs)

# ------------------------------------------------------------------------------
# Routing Utils
# ------------------------------------------------------------------------------
import gaeo
from gaeo.dispatch import router

from django.template import Node, resolve_variable

class UrlNode(Node):
    def __init__(self, action, id=None):
        self.action = action
        self.id     = id
        self.router = router.Router()

    def render(self, context):
        action = resolve_variable(self.action, context)
    
        try:
            if self.id is None:
                return self.router.url_for(action)
            else:
                actual_id = resolve_variable(self.id, context)
                return self.router.url_for(action, id=actual_id)
                
        except:
            return "Horrible Death"

def url_for(parser, token):
    tokens = list(token.split_contents())
    return UrlNode(*tokens[1:])

register.tag(url_for)