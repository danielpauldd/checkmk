#!/usr/bin/env python3
"""Ruleset definition for SophosXG Hardware power supplies."""

# This script comes without warranty of any kind.
# Use it at your own risk.
# I assume no liability for the accuracy, correctness, completeness
# or usefulness nor for any sort of damages using this script may cause.
#
# 2026 - SHD System-Haus-Dresden GmbH - DPA

from cmk.rulesets.v1 import Help, Title, Message, Label
from cmk.rulesets.v1.form_specs import DictElement, Dictionary, List, String, InputHint, FieldSize
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic
from cmk.rulesets.v1.form_specs.validators import MatchRegex


def _parameter_valuespec_sophosxg_hardware_psu_summary() -> Dictionary:
    return Dictionary(
        elements={
            "ignore_psus": DictElement(
                parameter_form=List(
                    title=Title("Power supplies to ignore"),
                    help_text=Help(
                        "Enter the PSU index value that should not be checked."
                    ),
                    element_template=String(
                        label=Label('PSU'),
                        prefill=InputHint("2"),
                        custom_validate=[MatchRegex(
                            '^[0-1][0-9]$|^[1-9]$',
                            error_msg=Message('Please enter a number between 1 and 19')
                        )],
                        field_size=FieldSize.SMALL
                    ),
                ),
            ),
        },
    )


rule_spec_sophosxg_hardware_psu_summary = CheckParameters(
    name="sophosxg_hardware_psu_summary",
    title=Title("Sophos XG Power Supplies"),
    topic=Topic.NETWORKING,
    condition=HostCondition(),
    parameter_form=_parameter_valuespec_sophosxg_hardware_psu_summary,
)
