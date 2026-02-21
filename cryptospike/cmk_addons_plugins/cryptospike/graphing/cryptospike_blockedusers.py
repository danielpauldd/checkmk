#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# This script comes without warranty of any kind.
# Use it at your own risk.
# I assume no liability for the accuracy, correctness, completeness
# or usefulness nor for any sort of damages using this script may cause.
#
# 2025 - SHD System-Haus-Dresden GmbH - DPA

from cmk.graphing.v1 import Title
# from cmk.graphing.v1.graphs import Bidirectional as BidirectionalGraph
# from cmk.graphing.v1.graphs import Graph
from cmk.graphing.v1.metrics import Color, DecimalNotation, Metric, Unit, StrictPrecision
# from cmk.graphing.v1.perfometers import Bidirectional as BidirectionalPerfometer
from cmk.graphing.v1.perfometers import (
    Closed,
    FocusRange,
    Open,
    Perfometer
)

# UNIT_BYTES = Unit(IECNotation("B"))
# UNIT_TIME = Unit(TimeNotation())
# UNIT_PERCENTAGE = Unit(DecimalNotation("%"))
UNIT_COUNT = Unit(DecimalNotation(""), StrictPrecision(0))


#                                                          #
#                       Metrik-Konfig                      #
#                                                          #
metric_cryptospike_blockeduser = Metric(
    name="blockeduser",
    title=Title("Blocked Users"),
    unit=UNIT_COUNT,
    color=Color.BLUE,
)
metric_cryptospike_quarantineduser = Metric(
    name="quarantineduser",
    title=Title("Quarantined Users"),
    unit=UNIT_COUNT,
    color=Color.YELLOW,
)
metric_cryptospike_activeuser = Metric(
    name="activeuser",
    title=Title("Active Users"),
    unit=UNIT_COUNT,
    color=Color.GREEN,
)
metric_cryptospike_totaluser = Metric(
    name="totaluser",
    title=Title("Total audited Users"),
    unit=UNIT_COUNT,
    color=Color.DARK_GREEN,
)


#                                                          #
#                     Perfometer-Konfig                    #
#                                                          #
perfometer_cryptospike_blockeduser = Perfometer(
    name="blockeduser",
    focus_range=FocusRange(Closed(0), Open(10)),
    segments=["blockeduser"],
)
