from django.test import TestCase

class TestViews (TestCase):

    def testIndex (t):
        r = t.client.get ('/')
        t.assertEqual (200, r.status_code)
        t.assertEqual ('text/html; charset=utf-8', r.get ('content-type'))
        t.assertEqual ('OK', r.reason_phrase)
        t.assertEqual ('utf-8', r.charset)
        t.assertListEqual ([], r.templates)

    def testApiIndex (t):
        r = t.client.get ('/api/')
        t.assertEqual (200, r.status_code)
        t.assertEqual ('application/json', r.get ('content-type'))
        t.assertEqual ('OK', r.reason_phrase)
        t.assertEqual ('utf-8', r.charset)
        t.assertListEqual ([], r.templates)
