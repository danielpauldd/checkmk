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
    graphs,
    metrics,
    perfometers,
    Title,
)
from cmk.graphing.v1.metrics import (
    DecimalNotation,
    StrictPrecision
)
from cmk.graphing.v1.perfometers import (
    Stacked
)

UNIT_BYTES = metrics.Unit(metrics.IECNotation("B"))
UNIT_TIME = metrics.Unit(metrics.TimeNotation())
UNIT_PERCENTAGE = metrics.Unit(metrics.DecimalNotation("%"))
UNIT_TIME = metrics.Unit(metrics.Unit)
UNIT_COUNT = metrics.Unit(DecimalNotation(""), StrictPrecision(0))

metric_pihole_rest_dns_queries_today = metrics.Metric(
    name="dns_queries_today",
    title=Title("DNS Queries Today"),
    unit=UNIT_COUNT,
    color=metrics.Color.DARK_BLUE,
)

metric_pihole_rest_ads_blocked_today = metrics.Metric(
    name="ads_blocked_today",
    title=Title("Ads Blocked Today"),
    unit=UNIT_COUNT,
    color=metrics.Color.DARK_RED,
)

graph_pihole_rest_queries_today = graphs.Graph(
    name="queries_today",
    title=Title("Queries Today"),
    compound_lines=[
        "ads_blocked_today",
        "dns_queries_today",
    ],

)

metric_pihole_rest_ads_percentage_today = metrics.Metric(
    name="ads_percentage_today",
    title=Title("Ads Percentage Today"),
    unit=UNIT_PERCENTAGE,
    color=metrics.Color.DARK_YELLOW,
)

metric_pihole_rest_clients_ever_seen = metrics.Metric(
    name="clients_ever_seen",
    title=Title("Clients Ever Seen"),
    unit=UNIT_COUNT,
    color=metrics.Color.GREEN,
)

metric_pihole_rest_unique_clients = metrics.Metric(
    name="unique_clients",
    title=Title("Unique Clients"),
    unit=UNIT_COUNT,
    color=metrics.Color.CYAN,
)

graph_pihole_rest_clients = graphs.Graph(
    name="clients",
    title=Title("Clients"),
    compound_lines=["clients_ever_seen"],
    simple_lines=['unique_clients']
)

metric_pihole_rest_domains_being_blocked = metrics.Metric(
    name="domains_being_blocked",
    title=Title("Domains Being Blocked"),
    unit=UNIT_COUNT,
    color=metrics.Color.LIGHT_RED,
)

metric_pihole_rest_unique_domains = metrics.Metric(
    name="unique_domains",
    title=Title("Unique Domains"),
    unit=UNIT_COUNT,
    color=metrics.Color.CYAN,
)

metric_pihole_rest_queries_cached = metrics.Metric(
    name="queries_cached",
    title=Title("Queries Cached"),
    unit=UNIT_COUNT,
    color=metrics.Color.YELLOW,
)

metric_pihole_rest_queries_forwarded = metrics.Metric(
    name="queries_forwarded",
    title=Title("Queries Forwarded"),
    unit=UNIT_COUNT,
    color=metrics.Color.DARK_YELLOW,
)

graph_pihole_rest_queries_fowarded_cached = graphs.Graph(
    name="queries_fowarded_cached",
    title=Title("Queries Forwarded/Cached"),
    compound_lines=[
        "queries_forwarded",
        "queries_cached"
    ],
)

metric_pihole_rest_dns_queries_all_types = metrics.Metric(
    name="dns_queries_all_types",
    title=Title("DNS Queries all Types"),
    unit=UNIT_COUNT,
    color=metrics.Color.PURPLE,
)


metric_pihole_rest_reply_NODATA = metrics.Metric(
    name="reply_NODATA",
    title=Title("reply NODATA"),
    unit=UNIT_COUNT,
    color=metrics.Color.RED,
)

metric_pihole_rest_reply_NXDOMAIN = metrics.Metric(
    name="reply_NXDOMAIN",
    title=Title("reply NXDOMAIN"),
    unit=UNIT_COUNT,
    color=metrics.Color.ORANGE,
)

metric_pihole_rest_reply_CNAME = metrics.Metric(
    name="reply_CNAME",
    title=Title("reply CNAME"),
    unit=UNIT_COUNT,
    color=metrics.Color.GREEN,
)

metric_pihole_rest_reply_IP = metrics.Metric(
    name="reply_IP",
    title=Title("reply IP"),
    unit=UNIT_COUNT,
    color=metrics.Color.BLUE,
)

graph_pihole_rest_dns_query_types = graphs.Graph(
    name="dns_query_types",
    title=Title("DNS Query Types"),
    compound_lines=[
        # "dns_queries_all_types",
        "reply_NODATA",
        "reply_NXDOMAIN",
        "reply_CNAME",
        "reply_IP"
    ],
    simple_lines=['dns_queries_all_types']
)

perfometer_pihole_rest_ads_blocked_today = Stacked(
    name="ads_blocked_domains_blocked",
    upper=perfometers.Perfometer(
        name="domains_being_blocked",
        focus_range=perfometers.FocusRange(perfometers.Closed(0), perfometers.Open(50000)),
        segments=["domains_being_blocked"],
    ),
    lower=perfometers.Perfometer(
        name="ads_blocked_today",
        focus_range=perfometers.FocusRange(perfometers.Closed(0), perfometers.Open(50000)),
        segments=["ads_blocked_today"],
    ),
)
