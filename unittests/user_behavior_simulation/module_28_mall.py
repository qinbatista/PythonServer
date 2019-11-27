import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client
import secrets
import user_behavior_simulation




def purchase_success(world, token, pid, order_id, channel, user_name, currency):
    response = user_behavior_simulation.send_tcp_message({'world': world, 'function': 'purchase_success',
                                 'data': {'token': token, "pid": pid, "order_id": order_id, "channel": channel,
                                          "user_name": user_name, "currency": currency}})


def exchange_prop(world, token, game_id, exchange_id):
    response = user_behavior_simulation.send_tcp_message({'world': world, 'function': 'exchange_prop',
                                 'data': {'token': token, "game_id": game_id, "exchange_id": exchange_id}})

def mall_dialog(token, world, info):
    purchase_success(world, token, "VIP_CARD_NORMAL", f"{int(time.time())}{secrets.randbits(256)}"[:80], "apple", "name_0", "RMB")
    exchange_prop(world, token, "aliya", "11111")

    return ""
