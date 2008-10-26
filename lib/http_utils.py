from google.appengine.api.urlfetch import fetch

def asset_size(url):
    response = fetch(
        url             = url,
        method          = 'HEAD',
        allow_truncated = True,
    )
    
    return int(response.headers['content-length'])