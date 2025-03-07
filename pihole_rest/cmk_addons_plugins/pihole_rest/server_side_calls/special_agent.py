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

# from pydantic import BaseModel
from collections.abc import Iterator, Sequence
from pydantic import BaseModel
from cmk.server_side_calls.v1 import (
        HostConfig,
        # noop_parser,
        Secret,
        SpecialAgentConfig,
        SpecialAgentCommand
)


class Params(BaseModel):
    """params validator"""
    protocol: tuple
    password: Secret | None = None
    port: int
    no_cert_check: bool | None = None


def _agent_arguments(params: Params, host_config: HostConfig) -> Iterator[SpecialAgentCommand]:
    # print(params)
    """build command line arguments"""

    args: Sequence[str] = [
        "--address",
        host_config.primary_ip_config.address or host_config.name,
        "--port",
        str(params.port),
        "--protocol",
        params.protocol[0],
        "--password",
        params.password.unsafe("%s"),
    ]

    yield SpecialAgentCommand(command_arguments=args)


special_agent_pihole_rest = SpecialAgentConfig(
    name="pihole_rest",
    parameter_parser=Params.model_validate,
    commands_function=_agent_arguments
)
