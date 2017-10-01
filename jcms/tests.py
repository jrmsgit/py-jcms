from django.test import TestCase
from unittest.mock import Mock

from jcms.response import JcmsResponse

class TestJcmsResponse (TestCase):
    req = None
    resp = None

    def setUp (t):
        t.req = Mock ()
        t.req.path = '/'
        t.resp = JcmsResponse (t.req)

    def testSend (t):
        r = t.resp.send ('test1')
        t.assertEqual ('text/html; charset=utf-8', r.get ('content-type'))
        t.assertEqual ('OK', r.reason_phrase)
        t.assertEqual ('utf-8', r.charset)
        t.assertEqual ('test1', r.content.decode ())

    def testPlain (t):
        r = t.resp.plain ('test1')
        t.assertEqual ('text/plain; charset=utf-8', r.get ('content-type'))
        t.assertEqual ('OK', r.reason_phrase)
        t.assertEqual ('utf-8', r.charset)
        t.assertEqual ('test1', r.content.decode ())
