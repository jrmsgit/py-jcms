from django.test import TestCase
from django.http import HttpRequest

from jcms.response import JcmsResponse

class TestResponse (TestCase):
    req = None
    resp = None

    def setUp (t):
        t.req = HttpRequest ()
        t.req.path = '/'
        t.resp = JcmsResponse (t.req)

    def testSend (t):
        r = t.resp.send ({'data': 'testSend'}, tpl = 'jcms/test.html')
        t.assertEqual ('text/html; charset=utf-8', r.get ('content-type'))
        t.assertEqual ('OK', r.reason_phrase)
        t.assertEqual ('utf-8', r.charset)
        t.assertContains (r, 'testSend', count = 1)

    def testSendInvalidData (t):
        with t.assertRaises (RuntimeError) as cm:
            t.resp.send (tuple (), tpl = 'jcms/test.html')
        t.assertEqual ("invalid send data type: <class 'tuple'>",
                str (cm.exception))

    def testPlain (t):
        r = t.resp.send ('testPlain')
        t.assertEqual ('text/plain; charset=utf-8', r.get ('content-type'))
        t.assertEqual ('OK', r.reason_phrase)
        t.assertEqual ('utf-8', r.charset)
        t.assertEqual ('testPlain', r.content.decode ())
