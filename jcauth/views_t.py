from django.test import TestCase

from jcauth.urls import urlpatterns

class TestViews (TestCase):

    fixtures = ['users.json']

    def testURLPatterns (t):
        l = []
        for p in urlpatterns:
            l.append (p.describe ())
        t.assertListEqual ([
            "'^login/$' [name='login']",
            "'^logout/$' [name='logout']",
            "'^password_change/$' [name='password_change']",
            "'^password_change/done/$' [name='password_change_done']",
            "'^password_reset/$' [name='password_reset']",
            "'^password_reset/done/$' [name='password_reset_done']",
            "'^reset/(?P<uidb64>[0-9A-Za-z_\\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$' [name='password_reset_confirm']",
            "'^reset/done/$' [name='password_reset_complete']",

        ], sorted (l))

    def testLogin (t):
        r = t.client.get ('/auth/login/')
        t.assertContains (r, '<h2>Login</h2>')
        t.assertTemplateUsed (r, 'jcms/base.html')
        t.assertTemplateUsed (r, 'jcms/login.html')

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
        t.assertTrue (t.client.login (username = 'user1', password = 'uvtbAE7A'))
        r = t.client.get ('/auth/logout/')
        t.assertRedirects (r, '/auth/thanks/', fetch_redirect_response = False)

    def testPasswordChange (t):
        t.assertTrue (t.client.login (username = 'user1', password = 'uvtbAE7A'))
        r = t.client.get ('/auth/password_change/')
        t.assertContains (r, 'Please enter your old password')
        t.assertTemplateUsed (r, 'jcms/base.html')
        t.assertTemplateUsed (r, 'jcms/password_change_form.html')

    def testPasswordChangeNotLogged (t):
        r = t.client.get ('/auth/password_change/')
        t.assertRedirects (r, '/auth/login/?next=/auth/password_change/',
                fetch_redirect_response = False)

    def testPasswordChangeDone (t):
        t.assertTrue (t.client.login (username = 'user1', password = 'uvtbAE7A'))
        r = t.client.get ('/auth/password_change/done/')
        t.assertContains (r, 'Your password was changed.')
        t.assertTemplateUsed (r, 'jcms/base.html')
        t.assertTemplateUsed (r, 'jcms/password_change_done.html')

    def testPasswordReset (t):
        r = t.client.get ('/auth/password_reset/')
        t.assertContains (r, 'Forgotten your password?')
        t.assertTemplateUsed (r, 'jcms/base.html')
        t.assertTemplateUsed (r, 'jcms/password_reset_form.html')

    def testPasswordResetDone (t):
        r = t.client.get ('/auth/password_reset/done/')
        t.assertContains (r, "We've emailed you instructions")
        t.assertTemplateUsed (r, 'jcms/base.html')
        t.assertTemplateUsed (r, 'jcms/password_reset_done.html')

    def testPasswordResetConfirm (t):
        from django.contrib.auth.models import User
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        u = User.objects.get (pk = 2)
        t.assertEqual (2, u.id)
        token = default_token_generator.make_token (u)
        uid = urlsafe_base64_encode (force_bytes (u.pk)).decode ()
        t.assertTrue (default_token_generator.check_token (u, token))
        r = t.client.get ('/auth/reset/{}/{}/'.format (uid, token))
        t.assertRedirects (r, '/auth/reset/{}/set-password/'.format (uid), fetch_redirect_response = False)

    def testPasswordResetConfirmInvalidLink (t):
        t.assertTrue (t.client.login (username = 'user1', password = 'uvtbAE7A'))
        r = t.client.get ('/auth/reset/b64/tok-en/')
        t.assertContains (r, 'The password reset link was invalid')
        t.assertTemplateUsed (r, 'jcms/base.html')
        t.assertTemplateUsed (r, 'jcms/password_reset_confirm.html')

    def testPasswordResetComplete (t):
        t.assertTrue (t.client.login (username = 'user1', password = 'uvtbAE7A'))
        r = t.client.get ('/auth/reset/done/')
        t.assertContains (r, 'Your password has been set.')
        t.assertTemplateUsed (r, 'jcms/base.html')
        t.assertTemplateUsed (r, 'jcms/password_reset_complete.html')
