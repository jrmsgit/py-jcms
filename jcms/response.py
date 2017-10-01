from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

class JcmsResponse (object):
    _req = None

    def __init__ (r, req):
        r._req = req

    def send (r, data, _ctype = None):
        if r._req.path.startswith ('/api/'):
            return JsonResponse ({'jcms': data})
        else:
            return HttpResponse (data, content_type = _ctype)

    def plain (r, text):
        return r.send (text, _ctype = 'text/plain; charset=utf-8')

    def render (r, tpl, data):
        return render (r._req, tpl, data)
