from django.test import TestCase

from jcauth.urls import urlpatterns

class TestViews (TestCase):

    fixtures = ['users.json']

    def testURLPatterns (t):
        l = []
        for p in urlpatterns:
            l.extend (sorted ([k for k in p.reverse_dict.keys () if isinstance (k, str)]))
        t.assertListEqual ([
            'login',
            'logout',
            'password_change',
            'password_change_done',
            'password_reset',
            'password_reset_complete',
            'password_reset_confirm',
            'password_reset_done',
        ], l)

    def testLogin (t):
        r = t.client.get ('/auth/login/')
        t.assertContains (r, '<h2>Login</h2>')

    def testLoginPOST (t):
        r = t.client.post ('/auth/login/', {
            'username': 'superuser',
            'password': 'uvtbAE7A',
        })
        t.assertRedirects (r, '/user/', fetch_redirect_response = False)

    def testLoginPOSTError (t):
        r = t.client.post ('/auth/login/', {
            'username': 'invaliduser',
            'password': 'invalidpw',
        })
        t.assertContains (r, 'Please try again.')

    def testLogout (t):
        r = t.client.get ('/auth/logout/')
        t.assertRedirects (r, '/auth/thanks/', fetch_redirect_response = False)
