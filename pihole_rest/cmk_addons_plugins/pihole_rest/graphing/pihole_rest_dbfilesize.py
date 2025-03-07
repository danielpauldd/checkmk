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

from cmk.graphing.v1 import (
    # graphs,
    metrics,
    perfometers,
    Title
)

UNIT_BYTES = metrics.Unit(metrics.IECNotation("B"))

metric_pihole_rest_dbfilesize = metrics.Metric(
    name="getDBfilesize",
    title=Title("DB File Size"),
    unit=UNIT_BYTES,
    color=metrics.Color.LIGHT_GREEN,
)

perfometer_pihole_rest_dbfilesize = perfometers.Perfometer(
    name="getDBfilesize",
    focus_range=perfometers.FocusRange(perfometers.Closed(0), perfometers.Open(4 * (1024 * 1024 * 1024))),
    segments=["getDBfilesize"],
)
