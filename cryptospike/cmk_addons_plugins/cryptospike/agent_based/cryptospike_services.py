#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# This script comes without warranty of any kind.
# Use it at your own risk.
# I assume no liability for the accuracy, correctness, completeness
# or usefulness nor for any sort of damages using this script may cause.
#
# 2025 - SHD System-Haus-Dresden GmbH - DPA

from collections.abc import Mapping
from typing import Any

from cmk.agent_based.v2 import (
    AgentSection,
    # check_levels,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    # render,
    Result,
    Metric,
    RuleSetType,
    Service,
    # ServiceLabel,
    State,
    StringTable,
)
import json
import datetime, tzlocal  # noqa: E401


#                                                          #
#                      Hilfsfunktionen                     #
#                                                          #
def format_ready_since(value):
    local_tz = tzlocal.get_localzone()
    # ISO-8601-String
    if isinstance(value, str):
        try:
            dt = datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
            dt = dt.astimezone(local_tz)
        except ValueError:
            return value
    # Unix-Timestamp
    elif isinstance(value, (int, float)):
        dt = datetime.datetime.fromtimestamp(float(value), tz=local_tz)
    else:
        return str(value)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


#                                                          #
#             Agent Sektion & Parser-Funktionen            #
#                                                          #
cryptospike_servicesSection = Mapping[str, Any]


def parse_cryptospike_services(string_table: StringTable) -> cryptospike_servicesSection:
    section = {}
    for line in string_table:
        if line[0][0] == '{':
            name = False
            data = json.loads(line[0])

            if ('service' in data and 'result' in data):
                name = data['service']
                section[name] = data['result']
    return section


agent_section_cryptospike_services = AgentSection(
    name="cryptospike_services",
    parse_function=parse_cryptospike_services,
)


#                                                          #
#                         Discovery                        #
#                                                          #
def discover_cryptospike_services(
    params,
    section: cryptospike_servicesSection
) -> DiscoveryResult:
    for name, data in section.items():
        if (params.get('ignoreServices')):
            if (name in params.get('ignoreServices')):
                continue
        yield Service(item=name)


#                                                          #
#                           Check                          #
#                                                          #
def check_cryptospike_services(
    item: str,
    params,
    section: cryptospike_servicesSection
) -> CheckResult:

    if item in section:
        data = section[item]

        infotext = None
        if (data.get('status') == 'OK'):
            state = State.OK
        else:
            state = State.CRIT
        infotext = data['message'] if (data.get('message')) else ""
        yield Result(state=state, summary=infotext)

        infotext = "ready since: %s" % format_ready_since(data['readySince']) if data.get('readySince') else None
        state = State.OK
        if params.get('minimumServiceUptime') is not None:
            if (data.get('uptimeSeconds') <= params.get("minimumServiceUptime")):
                state = state.WARN
                infotext += " minimum service uptime not reached."
        yield Result(state=state, summary=infotext)
        yield Metric(name="uptime", value=data['uptimeSeconds'], levels=(params.get("minimumServiceUptime"), None))


#                                                          #
#                       Registration                       #
#                                                          #
check_plugin_cryptospike_services = CheckPlugin(
    name="cryptospike_services",
    service_name="Service %s",
    sections=["cryptospike_services"],
    discovery_function=discover_cryptospike_services,
    discovery_default_parameters={
        'ignoreServices': None,
    },
    discovery_ruleset_name="cryptospike_services_discovery",
    discovery_ruleset_type=RuleSetType.MERGED,
    check_function=check_cryptospike_services,
    check_default_parameters={
        'minimumServiceUptime': 0.0,
    },
    check_ruleset_name="cryptospike_services"
)
