# encoding: utf-8

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
            elif n == 'jcmsprof.py':
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

def tplFiles ():
    tpldirs = glob ('*/templates/*')
    l = []
    for d in sorted (tpldirs):
        l.append ((d, sorted (glob ('{}/*.*'.format (d)))))
    return l

def pxdFiles ():
    dirs = ['jcms']
    l = []
    for d in sorted (dirs):
        l.append ((d, sorted (glob ('{}/*.pxd'.format (d)))))
    return l

def installFiles ():
    l = [('', sorted (['LICENSE', 'README.rst']))]
    l.extend (pxdFiles ())
    l.extend (tplFiles ())
    return l

def extModules ():
    l = []
    for _, files in pxdFiles ():
        for fn in files:
            l.append (fn.replace ('.pxd', '.py', 1))
    return l

if __name__ == '__main__':
    print (string ())
