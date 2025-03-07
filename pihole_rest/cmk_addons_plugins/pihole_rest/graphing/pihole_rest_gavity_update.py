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

UNIT_TIME = metrics.Unit(metrics.TimeNotation())

metric_pihole_rest_gravity_last_updated = metrics.Metric(
    name="gravity_last_updated",
    title=Title("Gravity Last Updated"),
    unit=UNIT_TIME,
    color=metrics.Color.BLUE,
)

perfometer_pihole_rest_gravity_last_updated = perfometers.Perfometer(
    name="gravity_last_updated",
    focus_range=perfometers.FocusRange(perfometers.Closed(0), perfometers.Open(7 * (60 * 60 * 24))),
    segments=["gravity_last_updated"],
)
