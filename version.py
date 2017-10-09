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

def installModules (tests = False):
    l = []
    p = glob ('*.py')
    p.extend (glob ('*/*.py'))
    p.extend (glob ('*/*/*.py'))
    for n in p:
        if not tests:
            if n.endswith ('_t.py'):
               continue
            elif n == 'jcmstest.py':
                continue
        if n == 'setup.py':
            continue
        elif n == 'devcli.py':
            continue
        elif n == 'devdb.py':
            continue
        elif n == 'manage.py':
            continue
        n = n.replace ('.py', '').replace (path.sep, '.')
        l.append (n)
    return sorted (l)

def installFiles ():
    tpldirs = sorted ([d for d in glob ('*/templates/*') if not d.endswith ('jcmstest')])
    l = [
        ('', sorted (['LICENSE', 'README.rst'])),
    ]
    for d in tpldirs:
        l.append ((d, sorted (glob ('{}/*.*'.format (d)))))
    return l
