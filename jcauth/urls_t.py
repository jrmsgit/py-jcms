from django.test import TestCase

from .urls import urlpatterns

class TestUrls (TestCase):

    def testUrlPatterns (t):
        l = []
        for p in urlpatterns:
            # ~ print ('URLPATT:', type (p), repr (p), p.lookup_str)
            desc = "{} {}".format (
                    ' '.join (repr (p).replace (']>', ']', 1).split ()[1:3]),
                    p.lookup_str)
            # ~ print ('URLPATT DESC:', desc)
            l.append (desc)
        t.assertListEqual ([
            "'^login/$' [name='login'] django.contrib.auth.views.LoginView",
            "'^logout/$' [name='logout'] django.contrib.auth.views.LogoutView",
            "'^password_change/$' [name='password_change'] django.contrib.auth.views.PasswordChangeView",
            "'^password_change/done/$' [name='password_change_done'] django.contrib.auth.views.PasswordChangeDoneView",
            "'^password_reset/$' [name='password_reset'] django.contrib.auth.views.PasswordResetView",
            "'^password_reset/done/$' [name='password_reset_done'] django.contrib.auth.views.PasswordResetDoneView",
            "'^reset/(?P<uidb64>[0-9A-Za-z_\\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$' [name='password_reset_confirm'] django.contrib.auth.views.PasswordResetConfirmView",
            "'^reset/done/$' [name='password_reset_complete'] django.contrib.auth.views.PasswordResetCompleteView",
        ], sorted (l))
