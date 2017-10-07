from django.conf.urls import url
from django.contrib.auth import views as authv

urlpatterns = [
    url ('^login/$',
            authv.LoginView.as_view (template_name = 'jcms/login.html'),
            name = 'login'),
    url ('^logout/$',
            authv.LogoutView.as_view (template_name = 'jcms/logged_out.html'),
            name = 'logout'),
    url ('^password_change/$',
            authv.PasswordChangeView.as_view (template_name = 'jcms/password_change_form.html'),
            name = 'password_change'),
    url ('^password_change/done/$',
            authv.PasswordChangeDoneView.as_view (template_name = 'jcms/password_change_done.html'),
            name = 'password_change_done'),
    url ('^password_reset/$',
            authv.PasswordResetView.as_view (
                template_name = 'jcms/password_reset_form.html',
                email_template_name = 'jcms/password_reset_email.txt',
                subject_template_name = 'jcms/password_reset_subject.txt',
            ),
            name = 'password_reset'),
    url ('^password_reset/done/$',
            authv.PasswordResetDoneView.as_view (template_name = 'jcms/password_reset_done.html'),
            name = 'password_reset_done'),
    url ('^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            authv.PasswordResetConfirmView.as_view (template_name = 'jcms/password_reset_confirm.html'),
            name = 'password_reset_confirm'),
    url ('^reset/done/$',
            authv.PasswordResetCompleteView.as_view (template_name = 'jcms/password_reset_complete.html'),
            name = 'password_reset_complete'),
]
