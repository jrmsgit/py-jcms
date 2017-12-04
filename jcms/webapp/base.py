from os import path, environ
from jcms.cmd import maincmd

class Webapp (object):
    __fn = None
    __srcdir = None
    __name = None
    # ~ __cfg = None

    def __init__ (self, filename):
        self.__checkFilename (filename)
        self.__fn = path.realpath (filename)
        self.__srcdir = path.dirname (self.__fn)
        self.__name = path.basename (self.__srcdir)
        # ~ self.__loadCfg ()

    def __checkFilename (self, filename):
        if not path.isfile (filename):
            raise RuntimeError ('{}: jcms webapp filename not found!')

    # ~ def __loadCfg (self):
        # ~ cf = path.join (self.__srcdir, 'jcms.cfg')
        # ~ if not path.isfile (cf):
            # ~ raise RuntimeError ('{}: config file not found!'.format (cf))
        # ~ # FIXME: self.__cfg = ...

    def run (self):
        environ.setdefault ('DJANGO_SETTINGS_MODULE', '{}.settings'.format (self.__name))
        print ('webapp:', self.__name)
        maincmd.run ()
