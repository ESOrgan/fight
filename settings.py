REBIRTH = False

auto_save = False  # test function

PROPERTY_KEY = ["max_mana", "mana", "mana_reg"]
PROPERTY_EXPR = {
    "max_mana": "player_property['max_mana'] = player_property['lv'] * 10 + 20",
    "mana": "player_property['mana'] = player_property['max_mana']",
    "mana_reg": "player_property['mana_reg'] = int(player_property['lv'] / 5) + 1"
}
