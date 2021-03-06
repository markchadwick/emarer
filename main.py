# autogenerated by the framework. Don't edit this file unless you undestand what is going on.
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os, glob, sys, logging

# set a gloabl APP_ROOT
from framework.root import APP_ROOT

# add the framework, congiuration, and application folders as places to look for modules
sys.path.append(APP_ROOT + '/framework')
sys.path.append(APP_ROOT + '/config')
sys.path.append(APP_ROOT + '/app/models')
sys.path.append(APP_ROOT + '/app/controllers')

import framework
import framework.routes
import config.routes
import app.controllers

# Create a new routing mapper and give it the contents of config/routes.py
m = framework.routes.Mapper()
m = config.routes.routing(m)

# Routes needs to know all the controllers to generate the 
# regular expressions.
controllers = []
for file in glob.glob(os.path.join((globals()['APP_ROOT'] + '/app/controllers'), '*_controller.py')):
  controllers.append(os.path.basename(file).replace('_controller.py',''))
m.create_regs(controllers)

class Router(webapp.RequestHandler):
  def route(self):
    # match the route
    m.environ = self.request.environ
    
    controller = m.match(self.request.path)
    # add the route information as request parameters
    for param, value in controller.iteritems():
      self.request.GET[param] = value
    
    logging.error(controller)
    # import and instantiate the correct controller and call the action/method
    __import__('app.controllers.' + controller['controller'] + '_controller')
    eval("app.controllers." + controller['controller'] +"_controller." + controller['controller'].capitalize() + "Controller(self.request, self.response, self)." + controller['action'] + '()')

  def post(self):
    if self.request.POST.has_key('_method'):
      if self.request.POST['_method'] == 'put':
       self.request.environ['REQUEST_METHOD'] = 'PUT'
      elif self.request.POST['_method'] == 'delete':
        self.request.environ['REQUEST_METHOD'] = 'DELETE'
        
    self.route()
  
  def get(self):
    self.route()
    
  def put(self):
    self.route()

  def delete(self):
    self.route()
  
#
# Register local template tags
#
from  google.appengine.ext.webapp.template import register_template_library
register_template_library('templatetags')
register_template_library('framework.filters.url_filters')

# send all requests to the better Router
application = webapp.WSGIApplication([('.*', Router)], debug=True)


def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
