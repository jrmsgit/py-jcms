#!/usr/bin/env python3

import os
from setuptools import setup
from Cython.Build import cythonize
from jcms import version

os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "jcms.settings")

setup (
    name = version.APPNAME,
    version = version.get (),

    description = version.DESC,
    long_description = version.DESC,

    license = version.LICENSE,
    url = version.URL,

    author = version.AUTHOR,
    author_email = version.AUTHOR_EMAIL,

    classifiers = version.CLASSIFIERS,

    install_requires = version.catfile ('requirements.txt').split (),

    ext_modules = cythonize ('jcms/version.py'),
    py_modules = version.installModules (),
    data_files = version.installFiles (),

    zip_safe = False,

    entry_points = {
        'console_scripts': [
            'jcms=jcmsmain:cmd',
        ],
    },

    test_suite = 'jcmstest',
)
