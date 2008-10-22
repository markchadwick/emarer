import logging
import os
import re
import sys
import wsgiref.handlers

from google.appengine.ext import webapp
from google.appengine.ext.webapp.template import register_template_library

# use zipped gaeo
try:
    import os
    if os.path.exists("gaeo.zip"):
        import sys
        sys.path.insert(0, 'gaeo.zip')
except:
    print "use normal gaeo folder"

import gaeo
from gaeo.dispatch import router

def initRoutes():
    r = router.Router()

    r.connect('/:controller/:action/:id')

def initTemplateLibraries():
    register_template_library('templatetags')

def initPlugins():
    """
    Initialize the installed plugins
    """
    plugins_root = os.path.join(os.path.dirname(__file__), 'plugins')
    if os.path.exists(plugins_root):
        plugins = os.listdir(plugins_root)
        for plugin in plugins:
            if not re.match('^__', plugin):
                try:
                    exec('from plugins import %s' % plugin)
                except ImportError:
                    logging.error('Unable to import %s' % (plugin))
                except SyntaxError:
                    logging.error('Unable to import name %s' % (plugin))

def main():
    # add the project's directory to the import path list.
    sys.path.append(os.path.dirname(__file__))
    sys.path.append(os.path.join(os.path.dirname(__file__), 'application'))

    # get the gaeo's config (singleton)
    config = gaeo.Config()
    # setup the templates' location
    config.template_dir = os.path.join(
        os.path.dirname(__file__), 'application', 'templates')

    initRoutes()
    initTemplateLibraries()
    
    # initialize the installed plugins
    initPlugins()

    app = webapp.WSGIApplication([
                (r'.*', gaeo.MainHandler),
            ], debug=True)
    wsgiref.handlers.CGIHandler().run(app)

if __name__ == '__main__':
    main()
