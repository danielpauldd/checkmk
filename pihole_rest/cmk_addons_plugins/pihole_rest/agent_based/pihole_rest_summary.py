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


from cmk.agent_based.v2 import (
    AgentSection,
    CheckResult,
    CheckPlugin,
    Service,
    Result,
    State,
    # Metric,
    render,
    check_levels
)
from .pihole_rest_common import parse_pihole_rest
from datetime import datetime


def discover_pihole_rest_summary(section):
    yield Service()


def check_pihole_rest_summary(params, section) -> CheckResult:
    gravity = section.get('gravity', None)
    queries = section.get('queries', None)
    clients = section.get('clients', None)

    if gravity:
        yield from check_levels(
            label="Blocked Domains",
            value=gravity["domains_being_blocked"],
            metric_name="domains_being_blocked",
            render_func=lambda v: str(v),
        )

    if queries:
        yield from check_levels(
            label="DNS Queries Today",
            value=queries["total"],
            metric_name="dns_queries_today",
            render_func=lambda v: str(v),
        )

        yield from check_levels(
            label="Ads Blocked Today",
            value=queries["blocked"],
            metric_name="ads_blocked_today",
            render_func=lambda v: str(v),
        )

        yield from check_levels(
            label="Ads Percentage Today",
            value=queries["percent_blocked"],
            metric_name="ads_percentage_today",
            boundaries=(0, 100),
            render_func=render.percent,
            notice_only=True,
        )

        yield from check_levels(
            label="Unique Domains",
            value=queries["unique_domains"],
            metric_name="unique_domains",
            render_func=lambda v: str(v),
            notice_only=True,
        )

        yield from check_levels(
            label="Queries Forwarded",
            value=queries["forwarded"],
            metric_name="queries_forwarded",
            render_func=lambda v: str(v),
            notice_only=True,
        )

        yield from check_levels(
            label="Queries Cached",
            value=queries["cached"],
            metric_name="queries_cached",
            render_func=lambda v: str(v),
            notice_only=True,
        )

        queries_replies = queries.get('replies', None)
        if queries_replies:
            yield from check_levels(
                label="DNS Queries All Types",
                value=queries["total"],
                metric_name="dns_queries_all_types",
                render_func=lambda v: str(v),
                notice_only=True,
            )

            yield from check_levels(
                label="reply NODATA",
                value=queries_replies["NODATA"],
                metric_name="reply_NODATA",
                render_func=lambda v: str(v),
                notice_only=True,
            )

            yield from check_levels(
                label="reply NXDOMAIN",
                value=queries_replies["NXDOMAIN"],
                metric_name="reply_NXDOMAIN",
                render_func=lambda v: str(v),
                notice_only=True,
            )

            yield from check_levels(
                label="reply CNAME",
                value=queries_replies["CNAME"],
                metric_name="reply_CNAME",
                render_func=lambda v: str(v),
                notice_only=True,
            )

            yield from check_levels(
                label="reply IP",
                value=queries_replies["IP"],
                metric_name="reply_IP",
                render_func=lambda v: str(v),
                notice_only=True,
            )

    if clients:
        yield from check_levels(
            label="Clients Ever Seen",
            value=clients["total"],
            metric_name="clients_ever_seen",
            render_func=lambda v: str(v),
            notice_only=True,
        )

        yield from check_levels(
            label="Unique Clients",
            value=clients["active"],
            metric_name="unique_clients",
            render_func=lambda v: str(v),
            notice_only=True,
        )

    return


agent_section_pihole_rest_summary = AgentSection(
    name="pihole_rest_summary",
    parse_function=parse_pihole_rest,
)


check_plugin_pihole_rest_summary = CheckPlugin(
    name="pihole_rest_summary",
    service_name="Pi-hole Summary",
    sections=["pihole_rest_summary"],
    discovery_function=discover_pihole_rest_summary,
    check_ruleset_name="pihole_rest",
    check_default_parameters={},
    check_function=check_pihole_rest_summary,
)


def discover_pihole_rest_gravity_update(section):
    yield Service()


def check_pihole_rest_gravity_update(params, section) -> CheckResult:
    lastUpdateTime = section['gravity']['last_update']
    dateA = datetime.now()
    dateB = datetime.fromtimestamp(lastUpdateTime)
    dateDiff = dateA - dateB
    result, metric = check_levels(
        value=dateDiff.total_seconds(),
        label="Age",
        levels_upper=params.get('gravity_last_update_age', ('fixed', (604800, 864000))),
        metric_name='gravity_last_updated',
        render_func=render.timespan,
    )
    yield metric
    yield Result(state=State.OK, summary=f"Last Gravity Update: {render.datetime(lastUpdateTime)}")
    yield result
    return


check_plugin_pihole_rest_gravity_update = CheckPlugin(
    name="pihole_rest_gravity_update",
    service_name="Pi-hole Gravity Last Update",
    sections=["pihole_rest_summary"],
    discovery_function=discover_pihole_rest_gravity_update,
    check_ruleset_name="pihole_rest",
    check_default_parameters={},
    check_function=check_pihole_rest_gravity_update,
)
