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

try:
    from cmk.utils import debug
except ImportError:
    from cmk.ccc import debug
from pprint import pprint
import itertools
import json


def parse_pihole_rest(string_table):
    flatlist = list(itertools.chain.from_iterable(string_table))
    parsed = json.loads(" ".join(flatlist).replace("'", "\""))
    if debug.enabled():
        pprint(string_table)
        pprint(parsed)
    return parsed
