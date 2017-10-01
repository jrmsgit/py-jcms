#!/usr/bin/env python3

from setuptools import setup, find_packages
import version

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

    py_modules = [],
    data_files = [
        ('', ['LICENSE', 'README.rst']),
    ],

    zip_safe = False,

    packages = find_packages (),
    include_package_data = True,

    #~ entry_points = {
        #~ 'console_scripts': [
            #~ 'jcms=jcms:cmd',
        #~ ],
    #~ },

    #~ test_suite = 'test.suite',
)
