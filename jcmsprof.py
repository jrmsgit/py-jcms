#!/usr/bin/env python3

import io
from os import path

SRCDIR = path.dirname (path.abspath (__file__)) + path.sep
STATENTRYNO = 6
ENTRY_FMT = '{0:>6} {1:>7} {2:>7} {3:>7} {4:>7} {5:<}'


class StatEntry (object):
    items = None

    def __init__ (self, items):
        self.items = items
        fn = self.items[STATENTRYNO - 1]
        self.items[STATENTRYNO - 1] = fn.replace (SRCDIR, '', 1)

    def __str__ (self):
        return ENTRY_FMT.format (*[i.strip () for i in self.items])


class ProfStats (object):
    headers = []
    eheader = None
    entries = {}

    def __init__ (self, filename):
        stats = pstats.Stats (filename)
        stats.sort_stats ('ncalls', 'cumtime')
        stats.stream = io.StringIO ()
        stats.print_stats (".*{}jcms{}.*".format (path.sep, path.sep))
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
                    fn = i[-1].replace (SRCDIR, '', 1).split (':')[0]
                    if fn != 'jcmstest.py' and not fn.endswith ('_t.py'):
                        self.entries[eno] = StatEntry (i)
                        eno += 1

    def _fmtHeaders (self, s):
        for h in self.headers:
            s.write (' '.join (h))
            s.write ('\n')

    def _fmtEntryHeader (self, s):
        s.write ('\n')
        # ~ s.write (' '.join (self.eheader))
        s.write (ENTRY_FMT.format (*[i.strip () for i in self.eheader]))
        s.write ('\n')

    def _fmtEntries (self, s):
        for eno in sorted (self.entries.keys ()):
            e = self.entries[eno]
            s.write (str (e))
            s.write ('\n')
        s.write ('\n')

    def __str__ (self):
        s = io.StringIO ()
        self._fmtEntryHeader (s)
        self._fmtEntries (s)
        self._fmtHeaders (s)
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
