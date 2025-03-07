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

from cmk.rulesets.v1.form_specs import (
    Dictionary,
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    BooleanChoice,
    DictElement,
    # Float,
    FixedValue,
    String,
    DefaultValue,
    Password,
    Integer,
    validators,
    migrate_to_password
)
from cmk.rulesets.v1.rule_specs import (
    SpecialAgent,
    Topic,
    Help,
    Title,
)


def _formspec():
    return Dictionary(
        title=Title("Pi-hole REST-API Special Agent"),
        help_text=Help("Pi-hole datasource program which talks to the new Pi-hole REST-API"),
        elements={
            "address": DictElement(
                required=False,
                parameter_form=String(
                    title=Title("use other hostname or IP Address for connection"),
                ),
            ),
            "port": DictElement(
                required=True,
                parameter_form=Integer(
                    title=Title("Port"),
                    help_text=Help(
                        "Port number for connection to the Pihole API."
                    ),
                    prefill=DefaultValue(80),
                    custom_validate=(
                        validators.NumberInRange(min_value=1, max_value=65535),
                    ),
                ),
            ),
            "protocol": DictElement(
                required=True,
                parameter_form=CascadingSingleChoice(
                    title=Title("Protocol"),
                    prefill=DefaultValue("http"),
                    help_text=Help(
                        "Protocol for the connection to the REST API."
                    ),
                    elements=[
                        CascadingSingleChoiceElement(
                            name="http",
                            title=Title("http"),
                            parameter_form=FixedValue(value="http", label=None),
                        ),
                        CascadingSingleChoiceElement(
                            name="https",
                            title=Title("https"),
                            parameter_form=FixedValue(value="https", label=None),
                        ),
                    ],
                ),
            ),
            "password": DictElement(
                required=True,
                parameter_form=Password(
                    title=Title("App-password for REST-API authentication."),
                    custom_validate=(validators.LengthInRange(min_value=1),),
                    migrate=migrate_to_password,
                    help_text=Help(
                        "Please see Settings > Web Interface/API > Advanced Settings > Configure app password"
                    )
                ),
            ),
            "no_cert_check": DictElement(
                parameter_form=BooleanChoice(
                    title=Title("Skip TLS certificate verification"),
                    prefill=DefaultValue(False),
                ),
                required=True,
            ),
        }
    )


rule_spec_pihole_rest_datasource = SpecialAgent(
    topic=Topic.NETWORKING,
    name="pihole_rest",
    title=Title("Pi-hole (Rest-API)"),
    parameter_form=_formspec
)
