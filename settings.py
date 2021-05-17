REBIRTH = False

auto_save = False  # test function

PROPERTY_KEY = ["max_mana", "mana", "mana_reg", "str", "max_str", "str_reg", "place", "km", "sm1", "sm2", "sm3"]
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
}
