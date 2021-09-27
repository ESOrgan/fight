REBIRTH = False

PROPERTY_KEY = ["max_mana", "mana", "mana_reg", "str", "max_str", "str_reg", "place", "km", "sm1", "sm2", "sm3", "sm4",
                "miner", "miner_max", "last_login", "miner_tier", "base_atk", "cheating", "nether", "nether_dlc",
                "inscriptions", "inscription_num", "inscription_buff", "kills"]
PROPERTY_EXPR = {
    "max_mana": "player_property['max_mana'] = player_property['lv'] * 10 + 20",
    "mana": "player_property['mana'] = player_property['max_mana']",
    "mana_reg": "player_property['mana_reg'] = int(player_property['lv'] / 5) + 1",
    "str": 'player_property["str"] = player_property["lv"] * 35 + 15',
    "max_str": 'player_property["max_str"] = player_property["str"]',
    "str_reg": 'player_property["str_reg"] = int(player_property["lv"] * 0.1) + 1',
    "place": "player_property['place'] = 1",
    "km": "player_property['km'] = 0.0",
    "sm1": "player_property['sm1'] = False",
    "sm2": "player_property['sm2'] = False",
    "sm3": "player_property['sm3'] = False",
    "sm4": "player_property['sm4'] = False",
    "miner": "player_property['miner'] = False",
    "miner_max": "player_property['miner_max'] = 1000",
    "last_login": "player_property['last_login'] = None",
    "miner_tier": "player_property['miner_tier'] = 1",
    "base_atk": 'player_property["base_atk"] = int(player_property["lv"] * 0.1)',
    "cheating": "player_property['cheating'] = False",
    "nether": "player_property['nether'] = False",
    "nether_dlc": "player_property['nether_dlc'] = False",
    "inscriptions": "player_property['inscriptions'] = ['空符文槽', '空符文槽']",
    "inscription_num": """
player_property['inscription_num'] = 2 + int(player_property['lv'] / 10)
if player_property["inscription_num"] > 11:
    player_property["inscription_num"] = 11
while len(player_property["inscriptions"]) < player_property["inscription_num"]:
    player_property["inscriptions"].append("空符文槽")
    """,
    "inscription_buff": "player_property['inscription_buff'] = {\"ht\": 0, \"atk\": 0, \"atk_p\": 0, \"def\": 0,"
                        "\"def_p\": 0, \"crit\": 0, \"miss\": 0}",
    "kills": 'player_property["kills"] = {41: 0, 42: 0, 43: 0, 44: 0, 45: 0, 46: 0, 47: 0}',
}
