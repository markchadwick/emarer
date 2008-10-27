from google.appengine.api.urlfetch import fetch
import logging
def asset_size(url):
    response = fetch(
        url             = url,
        method          = 'HEAD',
        allow_truncated = True,
    )
    
    return int(response.headers['content-length'])
    
def fetch_chunk(url, start_byte, end_byte, total_length=357):
    headers    = {
        'Range':    'bytes=%i-%i' % (start_byte, end_byte)
    }

    response = fetch(
        url     = url,
        method  = 'GET',
        headers = headers
    )
    return response.content