#!/usr/bin/env python3
"""Ruleset definition for Sophos XG Hardware fan speed monitoring."""

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
    Integer,
    LevelDirection,
    LevelsType,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_valuespec_sophosxg_hardware_fan() -> Dictionary:
    return Dictionary(
        elements={
            "levels_lower": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Minimum fan speed"),
                    help_text=Help(
                        "Warning and critical levels for a fan speed that is too low."
                    ),
                    level_direction=LevelDirection.LOWER,
                    form_spec_template=Integer(unit_symbol="RPM"),
                    prefill_fixed_levels=DefaultValue((4000, 2000)),
                    prefill_levels_type=DefaultValue(value=LevelsType.FIXED),
                ),
                required=True,
            ),
        },
    )


rule_spec_sophosxg_hardware_fan = CheckParameters(
    name="sophosxg_hardware_fan",
    title=Title("Sophos XG fan speed"),
    topic=Topic.NETWORKING,
    condition=HostAndItemCondition(item_title=Title("Fan")),
    parameter_form=_parameter_valuespec_sophosxg_hardware_fan,
)
