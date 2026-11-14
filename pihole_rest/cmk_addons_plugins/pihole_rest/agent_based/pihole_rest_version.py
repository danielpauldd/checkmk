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
    # render,
    # check_levels
)
from .pihole_rest_common import parse_pihole_rest
import re


def version_tuple(version):
    # Entfernt führendes 'v' und wandelt die Version in ein Tupel aus Zahlen um
    version = str(version)
    version = version.lstrip('v')
    return tuple(int(x) for x in re.split(r'[.\-]', version) if x.isdigit())


def discover_pihole_rest_version(section):
    yield Service()


def check_pihole_rest_version(params, section) -> CheckResult:
    p_ignore_components = params.get("ignore_components", {})
    components = section['version'].keys()

    for component in components:
        component_state = State.OK
        component_local = section['version'][component].get('local')
        component_remote = section['version'][component].get('remote')
        if component_local:
            # prüfe ob ein weiteres dict zurückgegben wird, dann steht die version unter version
            # sonst steht die Version bereits in der component_(local|remote) Variable (bei docker z.B.)
            local_version = component_local.get('version') if isinstance(component_local, dict) else component_local
        if component_remote:
            remote_version = component_remote.get('version') if isinstance(component_remote, dict) else component_remote
        if component not in p_ignore_components:
            if version_tuple(remote_version) > version_tuple(local_version):
                component_state = State.WARN
        yield Result(state=component_state, summary="%s - current: %s remote: %s" % (
            component,
            local_version,
            remote_version)
        )
    return


agent_section_pihole_rest_version = AgentSection(
    name="pihole_rest_version",
    parse_function=parse_pihole_rest,
)


check_plugin_pihole_rest_version = CheckPlugin(
    name="pihole_rest_version",
    service_name="Pi-hole Version",
    sections=["pihole_rest_version"],
    discovery_function=discover_pihole_rest_version,
    check_ruleset_name="pihole_rest",
    check_default_parameters={"dbfilesize": {}, "messages": {}},
    check_function=check_pihole_rest_version,
)
