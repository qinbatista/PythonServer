import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client
import secrets
import user_behavior_simulation

lukseun = tool_lukseun_client.LukseunClient('aliya', port=8880)
world = "0"
unique_id = "4"
token = ""


# random.getrandbits

def send_tcp_message(msg):
    return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))


def rmb_mall(world, token, pid, order_id, channel, user_name, currency):
    print_module("[rmb_mall]")
    response = send_tcp_message({'world': world, 'function': 'rmb_mall',
                                 'data': {'token': token, "pid": pid, "order_id": order_id, "channel": channel,
                                          "user_name": user_name, "currency": currency}})
    print_method(f"[rmb_mall]{response}")


def print_module(my_string):
    print(f"\033[0;37;41m\t{my_string}\033[0m")


def print_method(my_string):
    print(f"\033[0;37;44m\t{my_string}\033[0m")


def mall_dialog(token, world, info):
    rmb_mall(world, token, "VIP_CARD_NORMAL", f"{int(time.time())}{secrets.randbits(256)}"[:80], "apple", "name_0", "RMB")

    return ""
