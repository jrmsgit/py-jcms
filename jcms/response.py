from django.http import HttpResponse, JsonResponse

class JcmsResponse (object):
    _req = None

    def __init__ (r, req):
        r._req = req

    def send (r, data):
        if r._req.path.startswith ('/api/'):
            return JsonResponse ({'jcms': data})
        else:
            return HttpResponse (data)

    def render (r, tpl, data):
        return None
