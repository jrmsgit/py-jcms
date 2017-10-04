from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

class JcmsResponse (object):
    _req = None
    _charset = None

    def __init__ (r, req, charset = 'utf-8'):
        r._req = req
        r._charset = charset

    def _apirequest (r):
        return r._req.path.startswith ('/api/')

    def _plain (r, text):
        ctype = 'text/plain; charset={}'.format (r._charset)
        return HttpResponse (text, content_type = ctype)

    def _json (r, data):
        return JsonResponse ({'jcms': data})

    def _render (r, tpl, data):
        return render (r._req, tpl, data)

    def send (r, data, tpl = None):
        if isinstance (data, str):
            return r._plain (data)
        if not isinstance (data, dict):
            raise RuntimeError ('invalid send data type: {}'.format (type (data)))
        if r._apirequest ():
            return r._json (data)
        return r._render (tpl, data)
