#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# This script comes without warranty of any kind.
# Use it at your own risk.
# I assume no liability for the accuracy, correctness, completeness
# or usefulness nor for any sort of damages using this script may cause.
#
# 2025 - SHD System-Haus-Dresden GmbH - DPA

from collections.abc import Mapping
from typing import Any

from cmk.agent_based.v2 import (
    StringTable,
)
import json


#                                                          #
#                     Parser-Funktionen                    #
#                                                          #
cryptospikeSection = Mapping[str, Any]


def parse_cryptospike(string_table: StringTable) -> cryptospikeSection:
    for line in string_table:
        if line[0][0] == '{':
            data = json.loads(line[0])
    return data
