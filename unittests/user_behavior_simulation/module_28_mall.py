import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client
import secrets
import user_behavior_simulation

PID = [
    "VIP_CARD_NORMAL",
    "VIP_CARD_ULTIMATE",
    "VIP_CARD_PERMANENT",
    "DIAMOND_MIN",
    "DIAMOND_SMALL",
    "DIAMOND_LARGE",
    "DIAMOND_PLENTY",
    "DIAMOND_BAG",
    "EXPERIENCE_POTION_MIN",
    "EXPERIENCE_POTION_SMALL",
    "EXPERIENCE_POTION_LARGE",
    "EXPERIENCE_POTION_PLENTY",
    "EXPERIENCE_POTION_BAG",
    "ENERGY_POTION_MIN",
    "ENERGY_POTION_SMALL",
    "ENERGY_POTION_LARGE",
    "ENERGY_POTION_PLENTY",
    "ENERGY_POTION_BAG",
    "IRON_MIN",
    "IRON_SMALL",
    "IRON_LARGE",
    "IRON_PLENTY",
    "IRON_BAG",
    "SKILL_SCROLL_10_MIN",
    "SKILL_SCROLL_10_SMALL",
    "SKILL_SCROLL_10_LARGE",
    "SKILL_SCROLL_10_PLENTY",
    "SKILL_SCROLL_10_BAG",
    "SKILL_SCROLL_30_MIN",
    "SKILL_SCROLL_30_SMALL",
    "SKILL_SCROLL_30_LARGE",
    "SKILL_SCROLL_30_PLENTY",
    "SKILL_SCROLL_30_BAG",
    "SKILL_SCROLL_100_MIN",
    "SKILL_SCROLL_100_SMALL",
    "SKILL_SCROLL_100_LARGE",
    "SKILL_SCROLL_100_PLENTY",
    "SKILL_SCROLL_100_BAG",
    "SUMMON_SCROLL_BASIC_MIN",
    "SUMMON_SCROLL_BASIC_SMALL",
    "SUMMON_SCROLL_BASIC_LARGE",
    "SUMMON_SCROLL_BASIC_PLENTY",
    "SUMMON_SCROLL_BASIC_BAG",
    "SUMMON_SCROLL_PRO_MIN",
    "SUMMON_SCROLL_PRO_SMALL",
    "SUMMON_SCROLL_PRO_LARGE",
    "SUMMON_SCROLL_PRO_PLENTY",
    "SUMMON_SCROLL_PRO_BAG",
    "SUMMON_SCROLL_PROPHET_MIN",
    "SUMMON_SCROLL_PROPHET_SMALL",
    "SUMMON_SCROLL_PROPHET_LARGE",
    "SUMMON_SCROLL_PROPHET_PLENTY",
    "SUMMON_SCROLL_PROPHET_BAG",
    "FORTUNE_WHEEL_BASIC_MIN",
    "FORTUNE_WHEEL_BASIC_SMALL",
    "FORTUNE_WHEEL_BASIC_LARGE",
    "FORTUNE_WHEEL_BASIC_PLENTY",
    "FORTUNE_WHEEL_BASIC_BAG",
    "FORTUNE_WHEEL_PRO_MIN",
    "FORTUNE_WHEEL_PRO_SMALL",
    "FORTUNE_WHEEL_PRO_LARGE",
    "FORTUNE_WHEEL_PRO_PLENTY",
    "FORTUNE_WHEEL_PRO_BAG",
    "COIN_CARD_MIN",
    "COIN_CARD_SMALL",
    "COIN_CARD_LARGE",
    "COIN_CARD_PLENTY",
    "COIN_CARD_BAG",
    "EXP_CARD_MIN",
    "EXP_CARD_SMALL",
    "EXP_CARD_LARGE",
    "EXP_CARD_PLENTY",
    "EXP_CARD_BAG",
    "FOOD_CARD_MIN",
    "FOOD_CARD_SMALL",
    "FOOD_CARD_LARGE",
    "FOOD_CARD_PLENTY",
    "FOOD_CARD_BAG",
    "MINE_CARD_MIN",
    "MINE_CARD_SMALL",
    "MINE_CARD_LARGE",
    "MINE_CARD_PLENTY",
    "MINE_CARD_BAG",
    "CRYSTAL_CARD_MIN",
    "CRYSTAL_CARD_SMALL",
    "CRYSTAL_CARD_LARGE",
    "CRYSTAL_CARD_PLENTY",
    "CRYSTAL_CARD_BAG",
    "DIAMOND_CARD_MIN",
    "DIAMOND_CARD_SMALL",
    "DIAMOND_CARD_LARGE",
    "DIAMOND_CARD_PLENTY",
    "DIAMOND_CARD_BAG"
]


def purchase_success(world, token, pid, order_id, channel, user_name, currency):
    response = user_behavior_simulation.send_tcp_message({'world': world, 'function': 'purchase_success',
                                 'data': {'token': token, "pid": pid, "order_id": order_id, "channel": channel,
                                          "user_name": user_name, "currency": currency}})


def exchange_prop(world, token, game_id, exchange_id):
    response = user_behavior_simulation.send_tcp_message({'world': world, 'function': 'exchange_prop',
                                 'data': {'token': token, "game_id": game_id, "exchange_id": exchange_id}})

def mall_dialog(token, world, info,unique_id):
    for pid in PID:
        purchase_success(world, token, pid, f"{int(time.time())}{secrets.randbits(256)}"[:80], "apple", "name_"+unique_id, "RMB")
    exchange_prop(world, token, "aliya", "11111")

    return ""
