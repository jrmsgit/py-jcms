from jcms.response import JcmsResponse

def index (req):
    resp = JcmsResponse (req)
    return resp.send ({}, tpl = 'jcms/index.html')
