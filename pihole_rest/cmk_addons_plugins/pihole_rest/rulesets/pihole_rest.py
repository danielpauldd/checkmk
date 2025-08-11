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

# from collections.abc import Mapping
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    ServiceState,
    SingleChoice,
    SingleChoiceElement,
    TimeSpan,
    TimeMagnitude,
    DataSize,
    IECMagnitude,
    SimpleLevels,
    LevelDirection,
    BooleanChoice,
    DictElement,
    DictGroup,
    List,
    # Float,
    # FixedValue,
    String,
    DefaultValue,
    InputHint,
    # Password,
    # Integer,
    validators,
    # migrate_to_password
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    HostCondition,
    Topic,
    Help,
    Title,
)
from cmk.rulesets.v1 import Label


def _formspec() -> Dictionary:
    return Dictionary(
        title=Title("Pi-hole"),
        help_text=Help("Pi-hole datasource program ""Pi-hole REST-API Special Agent"" must be configured."),
        elements={
            "blocking": DictElement(
                parameter_form=Dictionary(
                    title=Title("Blocking"),
                    elements={
                        "blocking_status": DictElement(
                            required=True,
                            parameter_form=SingleChoice(
                                title=Title("Status"),
                                prefill=DefaultValue("enabled"),
                                elements=[
                                    SingleChoiceElement(
                                        name="enabled",
                                        title=Title("enabled"),
                                    ),
                                    SingleChoiceElement(
                                        name="disabled",
                                        title=Title("disabled"),
                                    ),
                                ],
                            ),
                        ),
                        "blocking_non_permanent": DictElement(
                            parameter_form=ServiceState(
                                title=Title(
                                    "State when blocking status is not permanent"
                                ),
                                prefill=DefaultValue(ServiceState.WARN),
                            ),
                        ),
                    },
                )
            ),
            "gravity_last_update_age": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Gravity Last Update"),
                    help_text=Help("Define a age for the last Gravity update"),
                    form_spec_template=TimeSpan(
                        displayed_magnitudes=[
                            TimeMagnitude.MINUTE,
                            TimeMagnitude.HOUR,
                            TimeMagnitude.DAY
                        ]
                    ),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=InputHint((60 * 60 * 24 * 7, 60 * 60 * 24 * 10)),  # 7d, 10d
                )
            ),
            "dbfilesize": DictElement(
                required=True,
                parameter_form=Dictionary(
                    title=Title("Database File Size"),
                    elements={
                        "minimum": DictElement(
                            parameter_form=SimpleLevels(
                                title=Title("minimum DB File Size"),
                                help_text=Help("minimum size the file should have"),
                                form_spec_template=DataSize(
                                    displayed_magnitudes=[
                                        IECMagnitude.BYTE,
                                        IECMagnitude.KIBI,
                                        IECMagnitude.MEBI,
                                        IECMagnitude.GIBI,
                                    ]
                                ),
                                level_direction=LevelDirection.LOWER,
                                prefill_fixed_levels=InputHint(value=(0, 0))
                            )
                        ),
                        "maximum": DictElement(
                            parameter_form=SimpleLevels(
                                title=Title("maximum DB File Size"),
                                help_text=Help("maximum size the file should have"),
                                form_spec_template=DataSize(
                                    displayed_magnitudes=[
                                        IECMagnitude.BYTE,
                                        IECMagnitude.KIBI,
                                        IECMagnitude.MEBI,
                                        IECMagnitude.GIBI,
                                    ]
                                ),
                                level_direction=LevelDirection.UPPER,
                                prefill_fixed_levels=InputHint(value=(0, 0))
                            )
                        )
                    }
                )
            ),
            "messages": DictElement(
                required=True,
                parameter_form=Dictionary(
                    title=Title("Status Messages"),
                    help_text=Help("define some parameters for possible Pi-hole messages"),
                    elements={
                        "nohtml": DictElement(
                            # required=True,
                            parameter_form=BooleanChoice(
                                label=Label("html output disabled"),
                                title=Title("plaintext check output (no HTML)"),
                                help_text=Help(
                                    "if you prefer non HTML output or have HTML output disabled."
                                    "The non HTML output format still need some further improvement"
                                )
                            ),
                        ),
                        "default_state": DictElement(
                            parameter_form=ServiceState(
                                title=Title("default state (for message types not further defined below)"),
                                help_text=Help(
                                    "the default state effect for messages not explicitly defined as OK, WARN or CRIT"
                                ),
                                prefill=DefaultValue(ServiceState.WARN)
                            ),
                        ),
                        "msg_ok": DictElement(
                            parameter_form=List(
                                title=Title("always OK message types"),
                                help_text=Help(
                                    "Message Types which are allways OK (max messages will count these nevertheless)"
                                ),
                                element_template=String(),
                                custom_validate=(validators.LengthInRange(min_value=1),),
                            ),
                            group=DictGroup()
                        ),
                        "msg_warn": DictElement(
                            parameter_form=List(
                                title=Title("always WARN message types"),
                                help_text=Help(
                                    "Message Types which are allways WARN (max messages will count these nevertheless)"
                                ),
                                element_template=String(),
                                custom_validate=(validators.LengthInRange(min_value=1),),
                            ),
                            group=DictGroup()
                        ),
                        "msg_crit": DictElement(
                            parameter_form=List(
                                title=Title("always CRIT message types"),
                                help_text=Help(
                                    "Message Types which are allways CRIT (max messages will count these nevertheless)"
                                ),
                                element_template=String(),
                                custom_validate=(validators.LengthInRange(min_value=1),),
                            ),
                            group=DictGroup()
                        )
                    }
                )
            ),
            "ignore_components": DictElement(
                required=False,
                parameter_form=List(
                    title=Title("ignore version of component"),
                    help_text=Help(
                        "For all defined components, no version checks will be performed."
                    ),
                    element_template=String(),
                    custom_validate=(validators.LengthInRange(min_value=1),),
                ),
                group=DictGroup()
            ),
        },
    )


rule_spec_pihole_rest_datasource = CheckParameters(
    name="pihole_rest",
    title=Title("Pi-hole settings"),
    topic=Topic.NETWORKING,
    parameter_form=_formspec,
    condition=HostCondition(),
)
