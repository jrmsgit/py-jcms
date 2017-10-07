from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core import mail

class TestViews (TestCase):

    fixtures = ['users.json']

    def clientLogin (t, un = 'user1', pw = 'uvtbAE7A'):
        t.assertTrue (t.client.login (username = un, password = pw))

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
        t.clientLogin ()
        r = t.client.get ('/auth/logout/')
        t.assertRedirects (r, '/auth/login/', fetch_redirect_response = False)

    def testLogoutFollowRedirect (t):
        t.clientLogin ()
        r = t.client.post ('/auth/logout/', {})
        t.assertRedirects (r, '/auth/login/', fetch_redirect_response = True)

    def testPasswordChange (t):
        t.clientLogin ()
        r = t.client.get ('/auth/password_change/')
        t.assertContains (r, 'Please enter your old password')
        t.assertTemplateUsed (r, 'jcms/base.html')
        t.assertTemplateUsed (r, 'jcms/password_change_form.html')

    def testPasswordChangeNotLogged (t):
        r = t.client.get ('/auth/password_change/')
        t.assertRedirects (r, '/auth/login/?next=/auth/password_change/',
                fetch_redirect_response = False)

    def testPasswordChangePOST (t):
        u = User.objects.get (pk = 2)
        pw ='pbkdf2_sha256$36000$4gsR8CxwjFqB$53Rms6clRV+SPwkGCVw2Dl3paIKoHF/em3p7r2JNoj4='
        t.assertEqual (pw, u.password)
        t.assertTrue (t.client.login (username = 'user1', password = 'uvtbAE7A'))
        r = t.client.post ('/auth/password_change/', {
            'old_password': 'uvtbAE7A',
            'new_password1': 'uvtbAE7B',
            'new_password2': 'uvtbAE7B',
        })
        t.assertRedirects (r, '/auth/password_change/done/', fetch_redirect_response = True)
        u = User.objects.get (pk = 2)
        pw2 = u.password
        t.assertNotEqual (pw2, pw)

    def testPasswordChangePOSTInvalid (t):
        t.clientLogin ()
        r = t.client.post ('/auth/password_change/', {})
        t.assertContains (r, 'Please correct the errors below.')

    def testPasswordChangeDone (t):
        t.clientLogin ()
        r = t.client.get ('/auth/password_change/done/')
        t.assertContains (r, 'Your password was changed.')
        t.assertTemplateUsed (r, 'jcms/base.html')
        t.assertTemplateUsed (r, 'jcms/password_change_done.html')

    def testPasswordReset (t):
        r = t.client.get ('/auth/password_reset/')
        t.assertContains (r, 'Forgotten your password?')
        t.assertTemplateUsed (r, 'jcms/base.html')
        t.assertTemplateUsed (r, 'jcms/password_reset_form.html')

    def testPasswordResetPOST (t):
        t.assertListEqual ([], mail.outbox)
        r = t.client.post ('/auth/password_reset/', {
            'email': 'user1@jcms.local',
        })
        t.assertRedirects (r, '/auth/password_reset/done/',
            fetch_redirect_response = False)
        m = mail.outbox[0]
        t.assertListEqual (['user1@jcms.local'], m.to)
        t.assertEqual ('jcms@localhost', m.from_email)
        t.assertEqual ('Password reset on testserver', m.subject)
        t.assertIsInstance (m.body, str)
        t.assertEqual (29, m.body.find ('because you requested a password reset'))
        t.assertEqual (166, m.body.find ('http://testserver/auth/reset/Mg/4q3-75a577779083846c4512/'))
        t.assertEqual (255, m.body.find ('forgotten: user1'))

    def testPasswordResetPOSTEmptyEmail (t):
        r = t.client.post ('/auth/password_reset/', {'email': ''})
        t.assertContains (r, 'This field is required.')
        t.assertTemplateUsed (r, 'jcms/base.html')
        t.assertTemplateUsed (r, 'jcms/password_reset_form.html')

    def testPasswordResetDone (t):
        r = t.client.get ('/auth/password_reset/done/')
        t.assertContains (r, "We've emailed you instructions")
        t.assertTemplateUsed (r, 'jcms/base.html')
        t.assertTemplateUsed (r, 'jcms/password_reset_done.html')

    def testPasswordResetConfirm (t):
        u = User.objects.get (pk = 2)
        t.assertEqual (2, u.id)
        token = default_token_generator.make_token (u)
        uid = urlsafe_base64_encode (force_bytes (u.pk)).decode ()
        t.assertTrue (default_token_generator.check_token (u, token))
        r = t.client.get ('/auth/reset/{}/{}/'.format (uid, token))
        t.assertRedirects (r, '/auth/reset/{}/set-password/'.format (uid), fetch_redirect_response = False)

    def testPasswordResetConfirmInvalidLink (t):
        t.clientLogin ()
        r = t.client.get ('/auth/reset/b64/tok-en/')
        t.assertContains (r, 'The password reset link was invalid')
        t.assertTemplateUsed (r, 'jcms/base.html')
        t.assertTemplateUsed (r, 'jcms/password_reset_confirm.html')

    def testPasswordResetComplete (t):
        t.clientLogin ()
        r = t.client.get ('/auth/reset/done/')
        t.assertContains (r, 'Your password has been set.')
        t.assertTemplateUsed (r, 'jcms/base.html')
        t.assertTemplateUsed (r, 'jcms/password_reset_complete.html')
