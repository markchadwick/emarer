import os
from framework.root import APP_ROOT
from framework.routes import util
from google.appengine.ext.webapp import template

class AbstractController():
  def __init__(self, request, response, handler):
    """docstring for __init"""
    self.request  = request
    self.response = response
    self.handler   = handler
    self.view     = {}
    
  def render_view(self, file_name):
    """docstring for render"""
    path = (os.path.join(APP_ROOT, ('app/views/' + file_name) ))
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(template.render(path, self.view))
    
  def render_text(self, text):
    """docstring for render_text"""
    self.response.headers['Content-Type'] = 'text/text'
    self.response.out.write(text)
    
  def render_xml(self, xml):
    """docstring for render_xml"""
    path = (os.path.join(APP_ROOT, ('app/views/' + file_name) ))
    self.response.headers['Content-Type'] = 'text/xml'
    self.response.out.write(template.render(path, self.view))

  def _default_view(self):
    """Used interally to render a default view when render is called without any arguments so
       a request that maps to {controller="foos", action="show", id='10'} will render the file
       /app/views/foos/show.html
    """
    pass
  
  def redirect_to(self, url):
    """Redirects to a specified url"""
    self.handler.redirect(url)

# template.register_template_library('framework.filters.url_filters')
