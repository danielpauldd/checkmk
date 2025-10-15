#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# This script comes without warranty of any kind.
# Use it at your own risk.
# I assume no liability for the accuracy, correctness, completeness
# or usefulness nor for any sort of damages using this script may cause.
#
# 2025 - Daniel Paul


from collections.abc import Iterator, Sequence
from pydantic import BaseModel
from cmk.server_side_calls.v1 import (
        HostConfig,
        Secret,
        SpecialAgentConfig,
        SpecialAgentCommand
)


#                                                          #
#                     Params-Validator                     #
#                                                          #
class AuthParams(BaseModel):
    username: str | None = None
    password: Secret | None = None


class Params(BaseModel):
    address: str | None = None
    auth: AuthParams | None = None
    no_cert_check: bool | None = None


#                                                          #
#                     Argument-Builder                     #
#                                                          #
def _agent_arguments(
    params: Params,
    host_config: HostConfig
) -> Iterator[SpecialAgentCommand]:
    args: Sequence[str] = []
    if params.address is not None:
        args += ["--hostname", str(params.address)]
    else:
        if ((host_config.primary_ip_config.address is not None) and
           (host_config.primary_ip_config.address != "0.0.0.0")):
            args += ["--hostname", host_config.primary_ip_config.address]
        else:
            args += ["--hostname", host_config.name]
    if params.auth is not None:
        args += ["--username", str(params.auth.username)]
        # args += ["--password", params.auth.password.unsafe("%s")]
        args += ["--pwstore", params.auth.password]

    if params.no_cert_check:
        args += ["--no-cert-check"]

    yield SpecialAgentCommand(command_arguments=args)


special_agent_cryptospike = SpecialAgentConfig(
    name="cryptospike",
    parameter_parser=Params.model_validate,
    commands_function=_agent_arguments
)
