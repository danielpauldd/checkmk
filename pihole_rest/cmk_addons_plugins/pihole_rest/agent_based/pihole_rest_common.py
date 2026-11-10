#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# This script comes without warranty of any kind.
# Use it at your own risk.
# I assume no liability for the accuracy, correctness, completeness
# or usefulness nor for any sort of damages using this script may cause.
#
# 2025 - Daniel Paul
#
# based on pihole special agent
# from Florian Dille

from pprint import pprint
import itertools
import json

# The global debug flag is not part of the Agent Based API and has moved
# between Checkmk versions: cmk.utils.debug (2.3), cmk.ccc.debug (2.4/2.5),
# removed entirely in 3.0. Never let it break plugin loading.
try:
    from cmk.ccc import debug as _debug
except ImportError:
    try:
        from cmk.utils import debug as _debug
    except ImportError:
        _debug = None


def _debug_enabled():
    return _debug is not None and _debug.enabled()


def parse_pihole_rest(string_table):
    flatlist = list(itertools.chain.from_iterable(string_table))
    parsed = json.loads(" ".join(flatlist).replace("'", "\""))
    if _debug_enabled():
        pprint(string_table)
        pprint(parsed)
    return parsed
