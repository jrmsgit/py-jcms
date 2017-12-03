from os import write, close, unlink, path
from unittest import TestCase
from tempfile import mkstemp

from jcms import version


class TestVersion (TestCase):
    _version = None
    _versionString = None

    def setUpClass ():
        TestVersion._version = '{}.{}'.format (version.VMAJOR, version.VMINOR)
        if version.VPATCH > 0:
            TestVersion._version = '{}.{}'.format (TestVersion._version, version.VPATCH)
        TestVersion._versionString = '{} v{}'.format (version.APPNAME, TestVersion._version)

    def testGet (t):
        t.assertEqual (t._version, version.get ())

    def testGetVPATCH (t):
        oldVPATCH = version.VPATCH
        try:
            version.VPATCH = 999
            t.assertTrue (version.get ().endswith ('.999'))
        finally:
            version.VPATCH = oldVPATCH

    def testString (t):
        t.assertEqual (t._versionString, version.string ())

    def testCatfile (t):
        fd, fn = mkstemp (suffix = '-jcmstestversion')
        try:
            write (fd, b'L1\n')
            write (fd, b'L2\n')
            write (fd, b'L3\n')
            close (fd)
        except Exception as e:
            unlink (fn)
            raise e
        try:
            t.assertListEqual (['L1', 'L2', 'L3'], version.catfile (fn).split ())
        finally:
            unlink (fn)

    def testLangFiles (t):
        pass

    def testExtModules (t):
        pass

    def testPackages (t):
        pass

    def testPackageDir (t):
        pass

    def testPackageData (t):
        pass


if __name__ == '__main__':
    missingOK = []
    missing = []
    for m in mods:
        if m.endswith ('.__init__'):
            # ignore __init__.py files (they don't have code on them)
            continue
        n = m + '_t'
        if n not in testmods and n not in missingOK:
            missing.append (n)
    if len (missing) > 0:
        print ('missing test files:')
        for n in sorted (missing):
            print (' ', n)
