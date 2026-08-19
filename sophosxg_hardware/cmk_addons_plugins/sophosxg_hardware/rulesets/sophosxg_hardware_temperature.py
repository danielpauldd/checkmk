#!/usr/bin/env python3
"""Ruleset definition for SophosXG Hardware temperature check."""

# This script comes without warranty of any kind.
# Use it at your own risk.
# I assume no liability for the accuracy, correctness, completeness
# or usefulness nor for any sort of damages using this script may cause.
#
# 2026 - SHD System-Haus-Dresden GmbH - DPA


from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Float,
    LevelDirection,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


def _parameter_valuespec_sophosxg_hardware_temperature() -> Dictionary:
    return Dictionary(
        elements={
            "NPU": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("NPU temperature"),
                    help_text=Help("Upper warning and critical levels for the NPU temperature."),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol="°C"),
                    prefill_fixed_levels=DefaultValue((75.0, 85.0)),
                ),
                required=True,
            ),
            "CPU": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("CPU temperature"),
                    help_text=Help("Upper warning and critical levels for the CPU temperature."),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol="°C"),
                    prefill_fixed_levels=DefaultValue((75.0, 85.0)),
                ),
                required=True,
            ),
        },
    )


rule_spec_sophosxg_hardware_temperature = CheckParameters(
    name="sophosxg_hardware_temperature",
    title=Title("Sophos XG temperatures"),
    topic=Topic.NETWORKING,
    condition=HostCondition(),
    parameter_form=_parameter_valuespec_sophosxg_hardware_temperature,
)
