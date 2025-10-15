#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# This script comes without warranty of any kind.
# Use it at your own risk.
# I assume no liability for the accuracy, correctness, completeness
# or usefulness nor for any sort of damages using this script may cause.
#
# 2025 - Daniel Paul


from cmk.rulesets.v1.form_specs import (
    Dictionary,
    BooleanChoice,
    DictElement,
    String,
    DefaultValue,
    Password,
    validators,
    migrate_to_password
)
from cmk.rulesets.v1.rule_specs import (
    SpecialAgent,
    Topic,
    Help,
    Title,
)


#                                                          #
#                   Datasource-Parameter                   #
#                                                          #
def _formspec():
    return Dictionary(
        title=Title("ProLion Cryptospike Special Agent"),
        help_text=Help(
            "ProLion Cryptospike datasource program to get service status and "
            "additional information when username and password are provided."
        ),
        elements={
            "address": DictElement(
                required=False,
                parameter_form=String(
                    title=Title("use other hostname or IP Address for connection"),
                    help_text=Help(
                        "this hostname is used instead of the Hostname / IP-Adress stored in Checkmk"
                        "(e.g. useful to avoid certificate errors because of name mismatch)."
                    ),
                ),
            ),
            "auth": DictElement(
                required=False,
                parameter_form=Dictionary(
                    title=Title("Authenticaion"),
                    help_text=Help(
                        "configure authentication to get detailed information additional to the services state"
                    ),
                    elements={
                        "username": DictElement(
                            required=True,
                            parameter_form=String(
                                title=Title("Username"),
                                help_text=Help("Username of a user with at least read-only permissions"),
                            ),
                        ),
                        "password": DictElement(
                            required=True,
                            parameter_form=Password(
                                title=Title("Password"),
                                custom_validate=(validators.LengthInRange(min_value=1),),
                                migrate=migrate_to_password,
                            ),
                        ),
                    },
                )
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


rule_spec_cryptospike_datasource = SpecialAgent(
    topic=Topic.APPLICATIONS,
    name="cryptospike",
    title=Title("ProLion Cryptospike"),
    parameter_form=_formspec
)
