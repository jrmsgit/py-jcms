#!/usr/bin/env python3

import io
from os import path

STATENTRYNO = 6
SRCDIR = path.dirname (path.abspath (__file__))


class StatEntry (object):
    items = None

    def __init__ (self, items):
        self.items = items
        fn = self.items[STATENTRYNO - 1]
        self.items[STATENTRYNO - 1] = fn.replace (SRCDIR+'/', '', 1)

    def __str__ (self):
        return ' '.join (self.items)


class ProfStats (object):
    headers = []
    eheader = None
    entries = {}

    def __init__ (self, filename):
        stats = pstats.Stats (filename)
        stats.sort_stats ('ncalls', 'cumtime')
        stats.stream = io.StringIO ()
        stats.print_stats (r'.*jcms/.*')
        stats.stream.seek (0, 0)
        eno = 0
        readheader = True
        for sl in stats.stream.readlines ():
            i = sl.strip ().split ()
            ilen = len (i)
            if ilen > 0:
                if readheader:
                    if ilen == STATENTRYNO and i[-1] == 'filename:lineno(function)':
                        readheader = False
                        self.eheader = i
                    else:
                        self.headers.append (i)
                else:
                    # read entry
                    fn = i[-1].replace (SRCDIR+'/', '', 1).split (':')[0]
                    if fn != 'jcmstest.py' and not fn.endswith ('_t.py'):
                        self.entries[eno] = StatEntry (i)
                        eno += 1

    def __str__ (self):
        s = io.StringIO ()
        s.write ('\n')
        s.write (' '.join (self.eheader))
        s.write ('\n')
        for eno in sorted (self.entries.keys ()):
            e = self.entries[eno]
            s.write (str (e))
            s.write ('\n')
        s.write ('\n')
        for h in self.headers:
            s.write (' '.join (h))
            s.write ('\n')
        s.seek (0, 0)
        return s.read ()


if __name__ == '__main__':
    import pstats
    import cProfile
    import jcmstest
    prof = cProfile.Profile (subcalls = False, builtins = False)
    prof.run ('jcmstest.cmd()')
    prof.dump_stats ('jcmstest.profile')
    stats = ProfStats ('jcmstest.profile')
    print (stats)
