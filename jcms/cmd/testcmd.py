import os
import sys
from os import path
from jcms import version

def run (chdir = True):
    if chdir:
        oldcwd = os.getcwd ()
        os.chdir (path.dirname (path.dirname (path.dirname (path.realpath (__file__)))))
        print (os.getcwd ())

    os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "jcms.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError (
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        if chdir:
            os.chdir (oldcwd)
        raise

    args = [sys.argv[0], 'test', '--failfast', '--pattern', '*_t.py']
    args.extend (sys.argv[1:])

    print (version.string ())
    execute_from_command_line (args)
    if chdir:
        os.chdir (oldcwd)
