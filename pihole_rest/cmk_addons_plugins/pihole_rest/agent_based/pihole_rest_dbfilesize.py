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
    render,
    check_levels
)
from .pihole_rest_common import parse_pihole_rest


def discover_pihole_rest_dbfilesize(section):
    yield Service()


def check_pihole_rest_dbfilesize(params, section) -> CheckResult:
    p_dbfilesize = params.get("dbfilesize", {})

    result, metric = check_levels(
        value=section['size'],
        label="/etc/pihole/pihole-FTL.db",
        levels_lower=(p_dbfilesize.get('minimum', ('no_levels', None))),
        levels_upper=(p_dbfilesize.get('maximum', ('no_levels', None))),
        metric_name='getDBfilesize',
        render_func=render.bytes,
    )
    yield metric
    yield result
    return


agent_section_pihole_rest_dbfilesize = AgentSection(
    name="pihole_rest_dbfilesize",
    parse_function=parse_pihole_rest,
)


check_plugin_pihole_rest_dbfilesize = CheckPlugin(
    name="pihole_rest_dbfilesize",
    service_name="Pi-hole DB File Size",
    sections=["pihole_rest_dbfilesize"],
    discovery_function=discover_pihole_rest_dbfilesize,
    check_ruleset_name="pihole_rest",
    check_default_parameters={"dbfilesize": {}, "messages": {}},
    check_function=check_pihole_rest_dbfilesize,
)
