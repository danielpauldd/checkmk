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
    render,
    Result,
    # Metric,
    # RuleSetType,
    Service,
    # ServiceLabel,
    State,
    # StringTable,
)
# import time
from datetime import datetime, timezone

from .cryptospike_common import (
    parse_cryptospike,
    cryptospikeSection
)

_DAY = 24 * 60 * 60

#                                                          #
#             Agent Sektion & Parser-Funktionen            #
#                                                          #
agent_section_cryptospike_license = AgentSection(
    name="cryptospike_license",
    parse_function=parse_cryptospike,
)


#                                                          #
#                         Discovery                        #
#                                                          #
def discover_cryptospike_license(
    # params,
    section: cryptospikeSection
) -> DiscoveryResult:
    yield Service()


#                                                          #
#                           Check                          #
#                                                          #
def check_cryptospike_license(
    params,
    section: cryptospikeSection
) -> CheckResult:
    # Lizenzstatus
    state = State.OK
    if section.get('status', {'state': 'unknown'}).get('state') != "LICENSED":
        state = State.WARN
    yield Result(state=state, summary="Status: %s" % section.get('status', {'state': 'unknown'}).get('state'))

    # Lizenzinfos
    infotext = "SiteID: %s, Type: %s, Edition: %s" % (
        section.get('siteKey', "unknown"),
        section.get('type', "unknown"),
        section.get('edition', "unknown")
    )
    yield Result(state=State.OK, summary=infotext)

    # Nodes and expiration
    nodes = section.get('nodes', None)
    if nodes:
        for node in nodes:
            state = state.OK
            now = datetime.now(timezone.utc)
            expiration_dt = datetime.fromisoformat(node['expirationDate'])
            secondsremaining = int((expiration_dt - now).total_seconds())

            if secondsremaining > 0:
                result, metric = check_levels(
                    secondsremaining,
                    levels_lower=params.get("licensewarning"),
                    metric_name='time_remaining',
                    label='time remaining',
                    render_func=render.timespan,
                )
            else:
                result, metric = check_levels(
                    secondsremaining,
                    levels_lower=params.get("licensewarning"),
                    metric_name='time_remaining',
                    label='Expired',
                    render_func=lambda x: "%s ago" % render.timespan(abs(x)),
                )
            # yield metric
            yield Result(state=result.state, notice="SN %s: %s" % (node['sn'], result.summary))


#                                                          #
#                       Registration                       #
#                                                          #
check_plugin_cryptospike_license = CheckPlugin(
    name="cryptospike_license",
    service_name="Cryptospike License",
    sections=["cryptospike_license"],
    discovery_function=discover_cryptospike_license,
    # discovery_default_parameters={
    # },
    # discovery_ruleset_name="cryptospike_license_discovery",
    # discovery_ruleset_type=RuleSetType.MERGED,
    check_function=check_cryptospike_license,
    check_default_parameters={
        'licensewarning': ("fixed", (90 * _DAY, 60 * _DAY)),
    },
    check_ruleset_name="cryptospike"
)
