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

from cmk.agent_based.v2 import (
    AgentSection,
    CheckResult,
    CheckPlugin,
    Service,
    Result,
    State,
    # Metric,
    render,
    # check_levels
)
from .pihole_rest_common import parse_pihole_rest


def discover_pihole_rest_messages(section):
    yield Service()


def check_pihole_rest_messages(params, section) -> CheckResult:
    p_messages = params.get("messages", {})
    # data = section.get('messages')

    data = section
    msg_count = len(data.get("messages", ""))

    if msg_count > 0:
        i = 1
        # define some empty vars for later use...
        l_types = []
        l_messages = []
        l_messages_types_ok = []
        l_messages_types_warn = []
        l_messages_types_crit = []
        l_messages_types_undef = []
        summary_appendix = []

        type_state_ok = 0
        type_state_warn = 0
        type_state_crit = 0
        type_state_undef = 0

        # for every message... in this case to fill up some lists before the real iteration
        for message in data["messages"]:
            # add loop elements to certain lists...
            l_types.append(message["type"])
            l_messages.append(message["plain"])
            l_messages_types_ok.append(message["type"]) if message["type"] in p_messages.get("msg_ok", []) else ""
            l_messages_types_warn.append(message["type"]) if message["type"] in p_messages.get("msg_warn", []) else ""
            l_messages_types_crit.append(message["type"]) if message["type"] in p_messages.get("msg_crit", []) else ""
            if (
                message["type"] not in p_messages.get("msg_crit", []) and
                message["type"] not in p_messages.get("msg_warn", []) and
                message["type"] not in p_messages.get("msg_ok", [])
            ):
                l_messages_types_undef.append(message["type"])

        # get more detailed output for the diffent type to state definitions via rule
        if len(l_messages_types_ok) > 0:
            type_state_ok = 0
            summary_appendix.append(f"ok message type count: {len(l_messages_types_ok)}")
        if len(l_messages_types_warn) > 0:
            type_state_warn = 1
            summary_appendix.append(f"warn message type count: {len(l_messages_types_warn)}")
        if len(l_messages_types_crit) > 0:
            type_state_crit = 2
            summary_appendix.append(f"crit message type count: {len(l_messages_types_crit)}")
        if len(l_messages_types_undef) > 0:
            type_state_undef = p_messages.get('default_state', 1)  # Defaults to WARN
            summary_appendix.append(f"other message type count: {len(l_messages_types_undef)}")

        details = []
        if not p_messages.get("nohtml"):
            # HTML Output header
            details.append("<table style='border-collapse:collapse'>")
            details.append("<style type='text/css' scoped> .pihole_td { border:1px solid #888; padding:5px; padding-right:10px; } </style>")  # noqa: E501
            details.append("<tr><td class='pihole_td' style='text-align:right; padding:5px;'>#</td><td class='pihole_td'>Time</td><td class='pihole_td'>Type</td><td class='pihole_td'>Message</td><td class='pihole_td'>Message Type Category</td></tr>")  # noqa: E501
        else:
            # get the max length for the certain columns (for non html output)
            # TODO: is there a way to change the font for non html output for better alignment of the rows to columns
            padding = {}
            padding["time"] = 20
            padding["type"] = len(max(l_types, key=len))+5
            padding["plain"] = len(max(l_messages, key=len))+5
            # non html output header
            details.append(f"\n| {'#'.ljust(5)}| {'Time'.ljust(padding['time']-2)}| {'Type'.ljust(padding['type'])}| {'Message'.ljust(padding['plain'])}| {'Message Type Category'.ljust(22)}".replace(" ", "_"))  # noqa: E501

        # for every message... now the concrete message handling
        for message in data["messages"]:

            # additional field for the table view
            if message["type"] in l_messages_types_crit:
                thisMsgTypeState = "CRIT"
            elif message["type"] in l_messages_types_warn:
                thisMsgTypeState = "WARN"
            elif message["type"] in l_messages_types_ok:
                thisMsgTypeState = "OK"
            else:
                thisMsgTypeState = "undef"

            # HTML or nonHTML for every message
            if not p_messages.get("nohtml"):
                details.append(f"<tr><td class='pihole_td' style='text-align:right; padding:5px;'>{i}.</td><td class='pihole_td'>{render.datetime(message['timestamp'])}</td><td class='pihole_td'>{message['type']}</td><td class='pihole_td'>{message['html']}</td><td class='pihole_td'>{thisMsgTypeState}</td></tr>")  # noqa: E501
            else:
                details.append(f"\n| {str(i).ljust(5)}| {(render.datetime(message['timestamp'])).ljust(padding['time'])}| {message['type'].ljust(padding['type'])}| {message['plain'].ljust(padding['plain'])}| {thisMsgTypeState.ljust(22)}".replace(" ", "_"))  # noqa: E501
            if i == 50:
                # limit output to max 50 lines
                # TODO: perhaps as a parameter?!
                if not p_messages.get("nohtml"):
                    details.append(f"<tr><td colspan='4' class='pihole_td'>output limited to 50 there are {msg_count-i} more ...</td></tr>")  # noqa: E501
                else:
                    details.append(f"output limited to 50 there are {msg_count-i} more ...")
                break
            i = i+1

        # close table output HTML or nonHTML
        if not p_messages.get("nohtml"):
            details.append("</table>")
        else:
            details.append("\n")

        yield Result(
            state=State(type_state_undef),
            # summary=f"there are pending status messages ({', '.join(summary_appendix)})",
            summary="there are pending status messages, see details.",
            details=f"{''.join(details)}"
        )
        # TODO: is there a better way?
        yield Result(state=State(type_state_ok),   notice=f"ok message type count: {len(l_messages_types_ok)}",)
        yield Result(state=State(type_state_warn), notice=f"warn message type count: {len(l_messages_types_warn)}",)
        yield Result(state=State(type_state_crit), notice=f"crit message type count: {len(l_messages_types_crit)}",)
    else:
        yield Result(state=State.OK, summary="no pending messages")

    return


agent_section_pihole_rest_summary = AgentSection(
    name="pihole_rest_messages",
    parse_function=parse_pihole_rest,
)


check_plugin_pihole_rest_messages = CheckPlugin(
    name="pihole_rest_messages",
    service_name="Pi-hole Status Messages",
    sections=["pihole_rest_messages"],
    discovery_function=discover_pihole_rest_messages,
    check_ruleset_name="pihole_rest",
    check_default_parameters={"dbfilesize": {}, "messages": {}},
    check_function=check_pihole_rest_messages,
)
