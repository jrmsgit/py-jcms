from django.test import TestCase

from .urls import urlpatterns

class TestUrls (TestCase):

    def testUrlPatterns (t):
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
