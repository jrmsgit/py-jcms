# -*- encoding: utf-8 -*-

from os import path
from glob import glob

VMAJOR = 0
VMINOR = 0
VPATCH = 0

AUTHOR = 'Jeremías Casteglione'
AUTHOR_EMAIL = 'jrmsdev@gmail.com'

APPNAME = 'jcms'
DESC = 'python3 + django cms'

LICENSE = 'BSD'
URL = 'https://github.com/jrmsdev/jcms'

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 3',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX :: BSD',
    'Operating System :: POSIX :: Linux',
    'Operating System :: Microsoft :: Windows',
]

def get ():
    v = '{}.{}'.format (VMAJOR, VMINOR)
    if VPATCH > 0:
        v = '{}.{}'.format (v, VPATCH)
    return v

def string ():
    return '{} v{}'.format (APPNAME, get ())

def catfile (fpath):
    with open (fpath, 'r') as fh:
        blob = fh.read ()
        fh.close ()
    return blob
