#!/usr/bin/env python3
"""Check for Sophos XG Hardware NPU and CPU temperatures."""

# This script comes without warranty of any kind.
# Use it at your own risk.
# I assume no liability for the accuracy, correctness, completeness
# or usefulness nor for any sort of damages using this script may cause.
#
# 2026 - SHD System-Haus-Dresden GmbH - DPA

# sample snmpwalk
#
# .1.3.6.1.4.1.2604.5.1.9.1.0 743   # sfosNPUTemperature; SYNTAX Integer32 (0..2000); UNITS "tenths of degrees Celsius"
# .1.3.6.1.4.1.2604.5.1.9.2.0 540   # sfosCPUTemperature; SYNTAX Integer32 (0..2000); UNITS "tenths of degrees Celsius"
#
# sample string_table
#
# [['743', '540']]

from dataclasses import dataclass
from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    StringTable,
    all_of,
    exists,
    check_levels,
    startswith,
)


@dataclass
class SophosXgHardwareTemp:
    NPU: float
    CPU: float


def parse_sophosxg_hardware_temperature(string_table: StringTable) -> SophosXgHardwareTemp | None:
    """Parse raw SNMP values from the Sophos XG system health OIDs."""
    try:
        npu, cpu = string_table[0]
    except IndexError:
        return None

    return SophosXgHardwareTemp(
        NPU=int(npu)/10,
        CPU=int(cpu)/10,
    )


snmp_section_sophosxg_hardware_temperature = SimpleSNMPSection(
    name="sophosxg_hardware_temperature",
    parse_function=parse_sophosxg_hardware_temperature,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.2604.5.1.9",
        oids=[
            "1",
            "2",
        ],
    ),
    detect=all_of(
        startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.2604.5"),
        exists(".1.3.6.1.4.1.2604.5.1.9.*"),
    ),
)


def discover_sophosxg_hardware_temperature(section: SophosXgHardwareTemp) -> DiscoveryResult:
    """Discover both temperature sensors if values are present."""
    for item in vars(section).keys():
        yield Service(item=item)


def check_sophosxg_hardware_temperature(item: str, params, section: SophosXgHardwareTemp) -> CheckResult:
    """Check the Sophos XG NPU and CPU temperature values."""
    if item not in vars(section).keys():
        return
    yield from check_levels(
        value=getattr(section, item),
        label='Temperature',
        levels_upper=params[item],
        render_func=lambda v: f'{v}°C',
        metric_name='temp',
        boundaries=(0, 100),
    )


check_plugin_sophosxg_hardware_temperature = CheckPlugin(
    name="sophosxg_hardware_temperature",
    service_name="Sophos %s Temperature",
    discovery_function=discover_sophosxg_hardware_temperature,
    check_function=check_sophosxg_hardware_temperature,
    check_default_parameters={'NPU': ('fixed', (80.0, 85.0)), 'CPU': ('fixed', (75.0, 85.0))},
    check_ruleset_name="sophosxg_hardware_temperature",
)
