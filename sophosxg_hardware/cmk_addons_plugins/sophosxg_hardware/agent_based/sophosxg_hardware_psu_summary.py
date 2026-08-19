#!/usr/bin/env python3
"""Check for SophosXG Hardware power supply state"""

# This script comes without warranty of any kind.
# Use it at your own risk.
# I assume no liability for the accuracy, correctness, completeness
# or usefulness nor for any sort of damages using this script may cause.
#
# 2026 - SHD System-Haus-Dresden GmbH - DPA

# sample snmpwalk
#
# .1.3.6.1.4.1.2604.5.1.9.4.1.2.1 2   # sfosPSUStatus; PSU 1 is down
# .1.3.6.1.4.1.2604.5.1.9.4.1.2.2 1   # sfosPSUStatus; PSU 2 is up
#
# sample string_table
#
# [['1', '2'], ['2', '1']

from typing import Dict, Optional

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    OIDEnd,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    StringTable,
    all_of,
    exists,
    startswith,
)

Section = Dict[str, str]


def parse_sophosxg_hardware_psu_summary(string_table: StringTable) -> Optional[Section]:
    """parse raw snmp data to dictionary keyed by power supply index"""
    parsed = {}
    for index, state in string_table:
        parsed[index] = state
    return parsed


snmp_section_sophosxg_hardware_psu_summary = SimpleSNMPSection(
    name="sophosxg_hardware_psu_summary",
    parse_function=parse_sophosxg_hardware_psu_summary,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.2604.5.1.9.4.1",
        oids=[
            OIDEnd(),
            "2",
        ],
    ),
    detect=all_of(
        startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.2604.5"),
        exists(".1.3.6.1.4.1.2604.5.1.9.4.*"),
    ),
)


def discover_sophosxg_hardware_psu_summary(section: Section) -> DiscoveryResult:
    """if data is present return a single service"""
    if section:
        yield Service()


def check_sophosxg_hardware_psu_summary(params, section: Section) -> CheckResult:
    """check the state of all power supplies, CRIT if at least one is down"""
    if not section:
        return

    psu_state: Dict[str, str] = {
        "1": "up",
        "2": "down",
    }

    for index, state in section.items():
        summarytext = f"PSU {index} is {psu_state.get(state, 'unknown')}"
        if index in params.get("ignore_psus", []):
            yield Result(state=State.OK, summary=f"{summarytext} (ignored)")
            continue
        if state != "1":
            serviceState = State.CRIT
        else:
            serviceState = State.OK
        yield Result(state=serviceState, summary=summarytext)


check_plugin_sophosxg_hardware_psu_summary = CheckPlugin(
    name="sophosxg_hardware_psu_summary",
    service_name="Sophos Power Supply Summary",
    discovery_function=discover_sophosxg_hardware_psu_summary,
    check_function=check_sophosxg_hardware_psu_summary,
    check_default_parameters={"ignore_psus": []},
    check_ruleset_name="sophosxg_hardware_psu_summary",
)
