#!/usr/bin/env python3

import pstats
import cProfile

import jcmstest

prof = cProfile.Profile (subcalls = False, builtins = False)
prof.run ('jcmstest.cmd()')
prof.dump_stats ('jcmstest.profile')

stats = pstats.Stats ('jcmstest.profile')
stats.sort_stats ('ncalls', 'cumtime')
stats.print_stats (r'.*jcms/.*')
