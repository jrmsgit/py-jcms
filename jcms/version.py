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

def extModules ():
    l = []
    for fn in sorted (glob ('*/*.pxd')):
        l.append (fn.replace ('.pxd', '.py', 1))
    return l

def packages ():
    f = glob ('*/__init__.py')
    f.extend (glob ('*/*/__init__.py'))
    f.extend (glob ('jcms/*/__init__.py'))
    f.extend (glob ('jcms/*/*/__init__.py'))
    l = []
    for m in sorted (f):
        if m.endswith ('__init__.py'):
            n = path.dirname (m).replace (path.sep, '.')
            if n not in l:
                l.append (n)
    return l

def packageDir ():
    pd = {}
    for pkg in packages ():
        pd[pkg] = pkg.replace ('.', path.sep)
    return pd

def packageData ():
    pd = {}
    for pkgname, pkgdir in packageDir ().items ():
        pkgfiles = []
        if path.isdir (path.join (pkgdir, 'templates', 'jcms')):
            pkgfiles.append (r'templates/jcms/*.*')
        if path.isdir (path.join (pkgdir, 'fixtures')):
            pkgfiles.append (r'fixtures/*.*')
        if len (glob ("{}/*.pxd".format (pkgdir))) > 0:
            pkgfiles.append (r'*.pxd')
        if len (glob ("{}/lang/*/LC_MESSAGES/django.*".format (pkgdir))) > 0:
            pkgfiles.append (r'lang/*/LC_MESSAGES/django.*')
        if len (pkgfiles) > 0:
            pd[pkgname] = pkgfiles
    return pd

if __name__ == '__main__': # pragma: no cover
    print (string ())
