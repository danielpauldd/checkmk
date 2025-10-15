#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# This script comes without warranty of any kind.
# Use it at your own risk.
# I assume no liability for the accuracy, correctness, completeness
# or usefulness nor for any sort of damages using this script may cause.
#
# 2025 - Daniel Paul


from cmk.rulesets.v1 import (
    Help,
    # Label,
    Title,
    # Message,
)
from cmk.rulesets.v1.form_specs import (
    # BooleanChoice,
    DefaultValue,
    DictElement,
    Dictionary,
    # FieldSize,
    Integer,
    # InputHint,
    # LevelDirection,
    # List,
    # migrate_to_lower_float_levels,
    # SimpleLevels,
    SingleChoice,
    SingleChoiceElement,
    String,
    # TimeMagnitude,
    # TimeSpan,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    # DiscoveryParameters,
    HostAndItemCondition,
    Topic,
)


#                                                          #
#                      Check-Parameter                     #
#                                                          #
def _parameter_valuespec_cryptospike_landscape_assignments() -> Dictionary:
    return Dictionary(
        elements={
            'engineType': DictElement(
                parameter_form=SingleChoice(
                    title=Title("Engine Type"),
                    elements=[
                        SingleChoiceElement(name="ACTIVE", title=Title("ACTIVE")),
                        SingleChoiceElement(name="PASSIVE", title=Title("PASSIVE")),
                        SingleChoiceElement(name="OFF", title=Title("OFF")),
                    ],
                    prefill=DefaultValue("ACTIVE"),
                ),
            ),
            'percent_minimum_connected': DictElement(
                parameter_form=Integer(
                    title=Title("minimum working engine connections"),
                    unit_symbol="%",
                    prefill=DefaultValue(50),
                )
            )
        },
    )


rule_spec_cryptospike_landscape_assignments = CheckParameters(
    name="cryptospike_landscape_assignments",
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_valuespec_cryptospike_landscape_assignments,
    title=Title("Cryptospike Server"),
    condition=HostAndItemCondition(
        item_title=Title("Cryptospike Server"),
        item_form=String(
            help_text=Help("The name of the Cryptospike Server"),
        )
    ),
)
