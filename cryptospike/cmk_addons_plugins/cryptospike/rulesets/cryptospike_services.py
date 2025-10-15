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
    # Integer,
    # InputHint,
    # LevelDirection,
    List,
    # migrate_to_lower_float_levels,
    # SimpleLevels,
    String,
    TimeMagnitude,
    TimeSpan,
    validators,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    DiscoveryParameters,
    HostAndItemCondition,
    Topic,
)


#                                                          #
#                      Check-Parameter                     #
#                                                          #
def _parameter_valuespec_cryptospike_services() -> Dictionary:
    return Dictionary(
        elements={
            'minimumServiceUptime': DictElement(
                parameter_form=TimeSpan(
                    title=Title("Minimal service uptime"),
                    migrate=float,
                    prefill=DefaultValue(600.0),
                    displayed_magnitudes=[TimeMagnitude.HOUR, TimeMagnitude.MINUTE],
                ),
                required=True,
            ),
        },
    )


rule_spec_cryptospike_services = CheckParameters(
    name="cryptospike_services",
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_valuespec_cryptospike_services,
    title=Title("ProLion CryptoSpike Services"),
    condition=HostAndItemCondition(
        item_title=Title("Cryptospike Service"),
        item_form=String(
            help_text=Help("The name of the Cryptospike Service"),
        )
    ),
)


#                                                          #
#                    Discovery-Parameter                   #
#                                                          #
def _valuespec_cryptospike_services_discovery() -> Dictionary:
    return Dictionary(
        elements={
            "ignoreServices": DictElement(
               parameter_form=List(
                   title=Title("List of services that should not be monitored."),
                   element_template=String(
                       field_size=80,
                       custom_validate=[
                           validators.MatchRegex(
                               regex=r"[\w\ \-]{3,}",
                               error_msg="Servicename must have at least 3 letters. Wildcards are not supported.",
                           ),
                       ],
                   ),
                   editable_order=False,
               )
            ),
        },
    )


rule_spec_cryptospike_services_discovery = DiscoveryParameters(
    name="cryptospike_services_discovery",
    topic=Topic.GENERAL,
    title=Title("ProLion Cryptospike service discovery"),
    parameter_form=_valuespec_cryptospike_services_discovery,
)
