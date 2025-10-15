#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# This script comes without warranty of any kind.
# Use it at your own risk.
# I assume no liability for the accuracy, correctness, completeness
# or usefulness nor for any sort of damages using this script may cause.
#
# 2025 - SHD System-Haus-Dresden GmbH - DPA

from cmk.agent_based.v2 import (
    AgentSection,
    check_levels,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    # render,
    # Result,
    Metric,
    # RuleSetType,
    Service,
    # ServiceLabel,
    # State,
    # StringTable,
)
from .cryptospike_common import (
    parse_cryptospike,
    cryptospikeSection
)


#                                                          #
#             Agent Sektion & Parser-Funktionen            #
#                                                          #
agent_section_cryptospike_blockedusers = AgentSection(
    name="cryptospike_blockedusers",
    parse_function=parse_cryptospike,
)


#                                                          #
#                         Discovery                        #
#                                                          #
def discover_cryptospike_blockedusers(
    # params,
    section: cryptospikeSection
) -> DiscoveryResult:
    yield Service()


#                                                          #
#                           Check                          #
#                                                          #
def check_cryptospike_blockedusers(
    params,
    section: cryptospikeSection
) -> CheckResult:
    result, metric = check_levels(
        value=section['totalItems'],
        label="Blocked Users",
        levels_upper=params.get("blockedUserCount"),
        metric_name='blockeduser',
    )
    yield metric
    yield result
    yield Metric(name="totaluser", value=section['totalUnfilteredItems'])


#                                                          #
#                       Registration                       #
#                                                          #
check_plugin_cryptospike_blockedusers = CheckPlugin(
    name="cryptospike_blockedusers",
    service_name="Cryptospike Blocked Users",
    sections=["cryptospike_blockedusers"],
    discovery_function=discover_cryptospike_blockedusers,
    # discovery_default_parameters={
    # },
    # discovery_ruleset_name="cryptospike_blockedusers_discovery",
    # discovery_ruleset_type=RuleSetType.MERGED,
    check_function=check_cryptospike_blockedusers,
    check_default_parameters={
        'blockedUserCount': ("fixed", (1, 1)),
    },
    check_ruleset_name="cryptospike"
)
