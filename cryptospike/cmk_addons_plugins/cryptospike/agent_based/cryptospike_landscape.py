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
    Metric,
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
cryptospike_landscapeSection = Mapping[str, Any]


def parse_cryptospike_landscape(string_table: StringTable) -> cryptospike_landscapeSection:
    section = {}
    name = False
    for line in string_table:
        data = json.loads(line[0])
        for cluster in data:
            if ('status' in cluster and 'data' in cluster):
                name = cluster['data']['name']
                section[name] = cluster['data']
    return section


agent_section_cryptospike_landscape = AgentSection(
    name="cryptospike_landscape_tree",
    parse_function=parse_cryptospike_landscape,
)


#                                                          #
#                         Discovery                        #
#                                                          #
def discover_cryptospike_landscape(
    # params,
    section: cryptospike_landscapeSection
) -> DiscoveryResult:
    for cluster, data in section.items():
        yield Service(item=cluster)


#                                                          #
#                           Check                          #
#                                                          #
def check_cryptospike_landscape(
    item: str,
    # params,
    section: cryptospike_landscapeSection
) -> CheckResult:
    cluster = section[item]
    clusterName = cluster.get('name')
    clusterVersion = cluster.get('version')
    clusterNodes = cluster.get('nodes', [])

    infotext = "Cluster: %s (%s), %d Nodes" % (clusterName, clusterVersion, len(clusterNodes))
    details = infotext
    for node in clusterNodes:
        details += "\nNode: %s (%s) - %s" % (node.get('name'), node.get('type'), node.get('licensedTopic'))
    yield Result(state=State.OK, summary=infotext, details=details)

    vServer = cluster.get('children', [])

    running_vservers = [vs for vs in vServer if vs.get('status') == 'RUNNING']
    total_running_vserver = len(running_vservers)
    yield Metric(name="total_running_vserver", value=total_running_vserver)


#                                                          #
#                       Registration                       #
#                                                          #
check_plugin_cryptospike_landscape = CheckPlugin(
    name="cryptospike_landscape",
    service_name="Cryptospike Cluster %s",
    sections=["cryptospike_landscape_tree"],
    discovery_function=discover_cryptospike_landscape,
    # discovery_default_parameters={
    # },
    # discovery_ruleset_name="cryptospike_landscape_discovery",
    # discovery_ruleset_type=RuleSetType.MERGED,
    check_function=check_cryptospike_landscape,
    # check_default_parameters={
    # },
    # check_ruleset_name="cryptospike_landscape"
)
