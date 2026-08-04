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
    StringTable,
)

from collections.abc import Mapping
from typing import Any
import json


#                                                          #
#             Agent Sektion & Parser-Funktionen            #
#                                                          #
cryptospike_landscape_assignmentsSection = Mapping[str, Any]


def parse_cryptospike_landscape_assignments(string_table: StringTable) -> cryptospike_landscape_assignmentsSection:
    section = {}
    # name = False
    for line in string_table:
        data = json.loads(line[0])
        if ('status' in data and 'data' in data):
            section = data['data']
    return section


agent_section_cryptospike_landscape_assignments = AgentSection(
    name="cryptospike_landscape_assignments",
    parse_function=parse_cryptospike_landscape_assignments,
)


#                                                          #
#                         Discovery                        #
#                                                          #
def discover_cryptospike_landscape_assignments(
    # params,
    section: cryptospike_landscape_assignmentsSection
) -> DiscoveryResult:
    for cluster, data in section.items():
        for server in data:
            if server.get('engineType', "OFF") == "OFF":
                continue
            else:
                serviceName = "%s:%s" % (cluster, server['serverName'])
                yield Service(item=serviceName)


#                                                          #
#                           Check                          #
#                                                          #
def check_cryptospike_landscape_assignments(
    item: str,
    params,
    section: cryptospike_landscape_assignmentsSection
) -> CheckResult:
    cluster = item.split(":")[0]
    volume = item.split(":")[1]

    voldetails = [vol for vol in section[cluster] if vol.get('serverName') == volume][0]

    if voldetails.get('healthy', False):
        state = State.OK
    else:
        state = State.CRIT
    yield Result(state=state, summary="Health Status: %s" % voldetails.get('healthyStatus', "unknown"))

    if voldetails['engineType'] == params.get('engineType', "ACTIVE"):
        state = State.OK
    elif voldetails['engineType'] == "PASSIVE":
        state = State.WARN
    else:
        state = State.CRIT
    yield Result(state=state, summary="Engine: %s" % voldetails['engineType'])

    def _percent(count):
        return round((count / total) * 100, 2) if total else 0

    ipv4_statuses = voldetails.get('ipv4Statuses', [])
    total = 0
    connected = []
    disconnected_good = []
    disconnected_bad = []
    for status in ipv4_statuses:
        if not isinstance(status, dict):
            continue
        # Some entries (for example unassigned "Server") contain no nested
        # per-node details keyed by ipv4.
        ipv4 = status.get('ipv4')
        node_statuses = status.get(ipv4) if ipv4 else None
        if not isinstance(node_statuses, dict):
            continue

        for connections in node_statuses.values():
            if not isinstance(connections, list):
                continue

            total += len(connections)
            connected += [conn for conn in connections if conn.get('connected')]
            disconnected_good += [conn for conn in connections if not conn.get('connected') and conn.get('disconnectedForGoodReason')]  # noqa: E501
            disconnected_bad += [conn for conn in connections if not conn.get('connected') and not conn.get('disconnectedForGoodReason')]  # noqa: E501

    connected_percent = _percent(len(connected))

    if len(disconnected_bad) > 0 or connected_percent == 0:
        state = State.CRIT
    elif connected_percent < params.get('percent_minimum_connected', 50):
        state = State.WARN
    else:
        state = State.OK

    infotext = []
    infotext.append("connected=%s (%s %%)" % (
        len(connected), connected_percent)
    )
    infotext.append("disconnected (good reason)=%s (%s %%)" % (
        len(disconnected_good), _percent(len(disconnected_good)))
    )
    infotext.append("disconnected (no good reason)=%s (%s %%)" % (
        len(disconnected_bad), _percent(len(disconnected_bad)))
    )
    infotext_text = ", ".join(infotext)

    details = infotext

    def extract_details(entries, status):
        for entry in entries:
            ip = entry.get('ipv4', 'Unknown')
            node = entry.get('node', 'Unknown')
            policy = entry.get('policyName', 'Unknown')
            reason = entry.get('disconnectReason', 'Unknown')
            details.append(
                "Status: %s - CS Agent (%s), Node %s, Policy: %s, Disconnect Reason: %s" % (
                    status, ip, node, policy, reason
                )
            )

    extract_details(disconnected_bad,  "Disconnected (No good reason)")
    extract_details(disconnected_good, "Disconnected")
    details_text = "\n".join(details) if details else ""

    yield Result(
        state=state,
        notice=infotext_text,
        details=details_text
    )


#                                                          #
#                       Registration                       #
#                                                          #
check_plugin_cryptospike_landscape_assignments = CheckPlugin(
    name="cryptospike_landscape_assignments",
    service_name="Cryptospike Server %s",
    sections=["cryptospike_landscape_assignments"],
    discovery_function=discover_cryptospike_landscape_assignments,
    # discovery_default_parameters={
    # },
    # discovery_ruleset_name="cryptospike_landscape_assignments_discovery",
    # discovery_ruleset_type=RuleSetType.MERGED,
    check_function=check_cryptospike_landscape_assignments,
    check_default_parameters={
        'engineType': "ACTIVE",
        'percent_minimum_connected': 50,
    },
    check_ruleset_name="cryptospike_landscape_assignments"
)
