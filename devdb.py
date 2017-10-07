#!/usr/bin/env python3

import os

os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "jcms.settings")

from django.core.management import execute_from_command_line

args = ['devdb', 'migrate']
execute_from_command_line (args)

args = ['devdb', 'createsuperuser', '--noinput', '--username', 'superuser',
        '--email', 'superuser@jcms.local']
execute_from_command_line (args)

from django.contrib.auth.models import User

su = User.objects.get (pk = 1)
su.set_password ('uvtbAE7A')
su.save ()

u1 = User.objects.create (username = 'user1')
u1.set_password ('uvtbAE7A')
u1.save ()
print ('User created:', u1.username)

u2 = User.objects.create (username = 'user2')
u2.set_password ('uvtbAE7A')
u2.save ()
print ('User created:', u2.username)
