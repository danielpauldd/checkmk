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
    InputHint,
    LevelDirection,
    # List,
    # migrate_to_lower_float_levels,
    ServiceState,
    SimpleLevels,
    # String,
    TimeMagnitude,
    TimeSpan,
    # validators,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    # DiscoveryParameters,
    # HostAndItemCondition,
    HostCondition,
    Topic,
)

_DAYS = (24.0 * 60 * 60)


#                                                          #
#                      Check-Parameter                     #
#                                                          #
def _parameter_valuespec_cryptospike() -> Dictionary:
    return Dictionary(
        elements={
            'blockedUserCount': DictElement(
                parameter_form=SimpleLevels(
                    title=Title('Blocked User'),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(
                        unit_symbol="blocked users"
                    ),
                    prefill_fixed_levels=InputHint(
                        value=(1, 1),
                    )
                )
            ),
            'licensewarning': DictElement(
                parameter_form=SimpleLevels(
                    title=Title('License Warning'),
                    help_text=Help("Days until expiry of license"),
                    level_direction=LevelDirection.LOWER,
                    form_spec_template=TimeSpan(
                        displayed_magnitudes=[TimeMagnitude.DAY],
                    ),
                    prefill_fixed_levels=InputHint(
                        value=(90 * _DAYS, 60 * _DAYS),
                    )
                )
            ),
            'outdatedstate': DictElement(
                parameter_form=ServiceState(
                    title=Title("Cryptospike Version state when new updates are available"),
                    prefill=DefaultValue(ServiceState.WARN),
                )
            ),
        }
    )


rule_spec_cryptospike = CheckParameters(
    name="cryptospike",
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_valuespec_cryptospike,
    title=Title("ProLion CryptoSpike"),
    condition=HostCondition(),
)
