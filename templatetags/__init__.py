from google.appengine.ext import webapp
register = webapp.template.create_template_register()

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