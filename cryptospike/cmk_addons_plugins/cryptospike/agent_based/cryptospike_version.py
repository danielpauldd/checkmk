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
    # check_levels,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    # render,
    Result,
    # Metric,
    # RuleSetType,
    Service,
    # ServiceLabel,
    State,
    # StringTable,
)

from .cryptospike_common import (
    parse_cryptospike,
    cryptospikeSection
)

_DAY = 24 * 60 * 60


#                                                          #
#             Agent Sektion & Parser-Funktionen            #
#                                                          #
agent_section_cryptospike_version = AgentSection(
    name="cryptospike_version",
    parse_function=parse_cryptospike,
)


#                                                          #
#                         Discovery                        #
#                                                          #
def discover_cryptospike_version(
    # params,
    section: cryptospikeSection
) -> DiscoveryResult:
    yield Service()


#                                                          #
#                           Check                          #
#                                                          #
def check_cryptospike_version(
    params,
    section: cryptospikeSection
) -> CheckResult:
    infotext = "%s %s" % (section.get('application'), section.get('version'))
    yield Result(state=State.OK, summary=infotext)

    if section.get('status') == "OUTDATED" and section.get('update'):
        state = State(params.get('outdatedstate', 1))
        infotext = "available update: %s" % (section['update'].get('version', "unknown"))
        notice = "ChangeLog: %s" % section['update'].get('changelogLink', "n/a")
        yield Result(state=state, summary=infotext, details=notice)


#                                                          #
#                       Registration                       #
#                                                          #
check_plugin_cryptospike_version = CheckPlugin(
    name="cryptospike_version",
    service_name="Cryptospike Version",
    sections=["cryptospike_version"],
    discovery_function=discover_cryptospike_version,
    # discovery_default_parameters={
    # },
    # discovery_ruleset_name="cryptospike_version_discovery",
    # discovery_ruleset_type=RuleSetType.MERGED,
    check_function=check_cryptospike_version,
    check_default_parameters={
        'outdatedstate': 1,
    },
    check_ruleset_name="cryptospike"
)
