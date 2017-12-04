import os
import sys

def run ():
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
        raise

    print ('JCMS: migrate...')
    args = [sys.argv[0], 'migrate']
    execute_from_command_line (args)

    print ('JCMS: runserver...')
    args = [sys.argv[0], 'runserver']
    execute_from_command_line (args)
