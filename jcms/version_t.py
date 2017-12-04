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

    def testExtModules (t):
        l = [path.join ('jcms', 'version.py')]
        t.assertListEqual (l, version.extModules ())

    def testPackageData (t):
        d = {
            'jcindex': ['templates/jcms/*.*'],
            'jcms': ['*.pxd', 'lang/*/LC_MESSAGES/django.*'],
            'jcms.jcauth': ['templates/jcms/*.*', 'fixtures/*.*'],
        }
        t.assertDictEqual (d, version.packageData ())

    def testPackageDir (t):
        d = {
            'jcindex': 'jcindex',
            'jcindex.migrations': path.join ('jcindex', 'migrations'),
            'jcms': 'jcms',
            'jcms.cmd': path.join ('jcms', 'cmd'),
            'jcms.jcauth': path.join ('jcms', 'jcauth'),
        }
        t.assertDictEqual (d, version.packageDir ())

    def testPackages (t):
        l = [
            'jcindex',
            'jcindex.migrations',
            'jcms',
            'jcms.cmd',
            'jcms.jcauth',
        ]
        t.assertListEqual (l, version.packages ())
