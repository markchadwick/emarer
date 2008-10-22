# -*- coding: utf-8 -*-
#
# Copyright 2008 GAEO Team
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
"""" GAEO view ajax helpers """

def link_to_function(title, script, html = {}):
    """ Return a link that contains onclick scripts """
    html_part = ''
    if html:
        for key, val in html.items():
            space = ' ' if html_part else ''
            html_part = '%s%s="%s"' % (space, key, val)
        
    return '<a href="#" %s onclick="%s;return false;">%s</a>' % (html_part, script, title)


def javascript_tag(scripts):
    """ Wraps scripts with <script> tag. """
    return '<script type="text/javascript">%s</script>' % scripts


def remote_script(url, **opts):
    """ Create a ajax request script """
    method = opts.get('method', 'get');
    # request parameters
    data = opts.get('data', '')
    # callback function
    callback = opts.get('callback', '')    
    dataType = opts.get('dataType', '')

    params = "'%s'" % data if data else ''
    if callback:
        cbf = 'function(data, textStatus){%s}' % callback
        params = params + ', %s' % cbf if params else cbf
    params = params + ", '%s'" % dataType if dataType else params
    if params:
        params = ', ' + params

    return """$.%s('%s'%s)""" % (method, url, params)

def link_to_remote(title, url, **opts):
    """ Create a link that request a remote action (jQuery-based) """
    # check if the title is specified
    if not title:
        raise Exception('Missing title of the link.')
    
    # remote action
    if not url:
        raise Exception('Missing remote action.')
    
    script = remote_script(url, **opts)    
    return link_to_function(title, script, opts.get('html', {}))


def load_from_remote(title, url, target, **opts):
    """ Create a link that load data from a remote action (jQuery-based) """
    # check if the title is specified
    if not title:
        raise Exception('Missing title of the link.')

    # remote action url
    if not url:
        raise Exception('Missing remote action.')
        
    # load target #id
    if not target:
        raise Exception('Missing the id of loaded data target.')
        
    data = opts.get('data', '')
    callback = opts.get('callback', '')    
    params = data
    if callback:
        cbf = 'function(){%s}' % callback
        params = '%s,%s' % (params, cbf) if params else cbf
    
    params = ', ' + params if params else ''
    script = """$('#%s').load('%s'%s);""" % (target, url, params)
    
    return link_to_function(title, script, opts.get('html', {}))


def periodically_call_remote(url, **opts):
    """ Periodically call a remote action. (jQuery-based) """
    if not url:
        raise Exception('Missing remote action url.')
    
    # frequency, default 1000 ms
    freq = opts.get('frequency', 1000)
    script = "setInterval(function(){%s}, %s)" % (remote_script(url, **opts), freq)
    return javascript_tag(script)
    
