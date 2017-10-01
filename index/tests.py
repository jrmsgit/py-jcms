from django.test import TestCase

class TestIndex (TestCase):

    def testIndex (t):
        #~ print (sorted ([k for k in dir (t) if not k.startswith ('_')]))
        #~ print (type (t.client), t.client)
        r = t.client.get ('/')
        #~ print (type (r), r)
        #~ print (sorted ([k for k in dir (r) if not k.startswith ('_')]))
        t.assertEqual (200, r.status_code)
