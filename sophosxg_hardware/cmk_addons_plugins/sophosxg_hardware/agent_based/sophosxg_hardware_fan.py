#!/usr/bin/env python3
"""Check Sophos XG Hardware system fan speeds."""

# This script comes without warranty of any kind.
# Use it at your own risk.
# I assume no liability for the accuracy, correctness, completeness
# or usefulness nor for any sort of damages using this script may cause.
#
# 2026 - SHD System-Haus-Dresden GmbH - DPA

# sample snmpwalk
#
# .1.3.6.1.4.1.2604.5.1.9.3.1.2.1 5100   # sfosFanSpeed; fan 1 speed in RPM
# .1.3.6.1.4.1.2604.5.1.9.3.1.2.2 5100   # sfosFanSpeed; fan 2 speed in RPM
#
# sample string_table
#
# [['1', '5100'], ['2', '5100']]

from typing import Dict, Optional

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    OIDEnd,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    StringTable,
    all_of,
    check_levels,
    exists,
    startswith,
)

Section = Dict[str, str]


def parse_sophosxg_hardware_fan(string_table: StringTable) -> Optional[Section]:
    """Parse raw SNMP data into a dictionary keyed by fan index."""
    parsed = {}
    for index, speed in string_table:
        parsed[index] = speed
    return parsed


snmp_section_sophosxg_hardware_fan = SimpleSNMPSection(
    name="sophosxg_hardware_fan",
    parse_function=parse_sophosxg_hardware_fan,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.2604.5.1.9.3.1",
        oids=[
            OIDEnd(),
            "2",
        ],
    ),
    detect=all_of(
        startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.2604.5"),
        exists(".1.3.6.1.4.1.2604.5.1.9.3.*"),
    ),
)


def discover_sophosxg_hardware_fan(section: Section) -> DiscoveryResult:
    """Discover one service for every reported fan."""
    for index in section:
        yield Service(item=index)


def check_sophosxg_hardware_fan(item: str, params, section: Section) -> CheckResult:
    """Check the selected fan speed against lower limits."""
    speed_text = section.get(item)

    speed = int(speed_text)
    yield from check_levels(
        value=speed,
        levels_lower=params["levels_lower"],
        label=f"Fan {item} speed",
        metric_name="fan_speed",
        boundaries=(0, None),
        render_func=lambda value: f"{value:.0f} RPM",
    )


check_plugin_sophosxg_hardware_fan = CheckPlugin(
    name="sophosxg_hardware_fan",
    service_name="Sophos Fan %s",
    discovery_function=discover_sophosxg_hardware_fan,
    check_function=check_sophosxg_hardware_fan,
    check_default_parameters={"levels_lower": ("fixed", (4000, 2000))},
    check_ruleset_name="sophosxg_hardware_fan",
)
