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
    # check_levels
)
from .pihole_rest_common import parse_pihole_rest


def discover_pihole_rest_state(section):
    yield Service()


def check_pihole_rest_state(params, section) -> CheckResult:
    param_blocking = params.get('blocking', {'blocking_status': 'enabled'})
    param_blocking_state = param_blocking.get('blocking_status')
    param_blocking_non_permanent = State(param_blocking.get('blocking_non_permanent', State.WARN))
    current_state = section['blocking']
    if current_state != param_blocking_state:
        if section['timer']:
            yield Result(
                state=param_blocking_non_permanent,
                notice="%s (will reset in %.0f seconds)" % (current_state, section['timer']),
            )
        else:
            yield Result(state=State.CRIT, summary="%s" % current_state)
    else:
        if section['timer']:
            yield Result(
                state=param_blocking_non_permanent,
                notice="%s (will reset in %.0f seconds)" % (current_state, section['timer'])
            )
        else:
            yield Result(state=State.OK, summary="%s" % current_state)
    return


agent_section_pihole_rest_state = AgentSection(
    name="pihole_rest_state",
    parse_function=parse_pihole_rest,
)


check_plugin_pihole_rest_state = CheckPlugin(
    name="pihole_rest_state",
    service_name="Pi-hole State",
    sections=["pihole_rest_state"],
    discovery_function=discover_pihole_rest_state,
    check_ruleset_name="pihole_rest",
    check_default_parameters={},
    check_function=check_pihole_rest_state,
)
