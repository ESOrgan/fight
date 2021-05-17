# version <dv-006>
# lines: 1414 + 4 (project description: 2; start blank: 1; end blank: 1) = 1418

import easygui as g
import random
import settings
import os
import base64
import collections

item_namespaces = {
    0: "无",

    # weapon
    10: "手", 11: "木棍", 12: "波克棒", 13: "石板波克棒", 14: "桃木剑", 15: "莫力布林棍", 16: "石板莫力布林棍", 17: "木剑",
    18: "骑士之剑", 19: "灵木剑", 110: "自然法杖I", 111: "自然法杖II", 112: "龙骨波克棒", 113: "精英骑士之剑", 114: "荣誉骑士之剑",
    115: "铂金骑士之剑", 116: "钻石骑士之剑",
    # armor
    21: "石板甲", 22: "士兵之甲", 23: "骑士之甲",

    # medicine
    30: "绷带", 31: "医用绷带", 32: "小型法力回复剂", 33: "小型体力回复剂", 34: "木之灵", 35: "木之心", 36: "仙人掌果",

    # mobs
    41: "波布克林", 42: "蓝色波布克林", 43: "丘丘", 44: "莫力布林", 45: "蓝色莫力布林",

    # skill
    50: "普通攻击",
    51: "跳劈重击（攻击）",
    52: "治愈神木（治疗）",
    53: "桃木斩（攻击）",
    54: "跳劈重击II（攻击）",
    55: "跳劈重击III（攻击）",
    56: "横扫攻击（攻击）",
    57: "快速搏击（攻击）",
    58: "横扫攻击II（攻击）",
    59: "横扫攻击III（攻击）",
    510: "骑士之魂（治疗）",
    511: "桃木斩II（攻击）",
    512: "治愈神木II（治疗）",
    513: "春光，降临人间！（终极技能）（治疗/回体力）",
    514: "树叶的洗礼（终极技能）（伤害/治疗）",
    515: "树叶炸弹（攻击）",
    516: "灵木的洗礼（攻击）",
    517: "树 叶 大 伊 万（攻击）",
    518: "自然之灵的祝福（治疗）",
    519: "树叶镖（攻击）",
    520: "跳劈重击IV（攻击）",
    521: "精英骑士之魂（治疗）",
    522: "金属骑士之魂（治疗）",

    # materials
    61: "小石子",
    62: "不完整的木板合成工具（P1）",
    63: "不完整的木板合成工具（P2）",
    64: "木板合成工具",
    65: "木板",
    66: "石板",
    67: "破旧的木板",
    68: "铁矿",
    69: "生铁",
    610: "生铁加工工具",
    611: "铁板",
    612: "致密铁板",
    613: "铁柄",
    614: "空魔法杖",
    615: "一级科学机器碎片",
    616: "二级科学机器碎片",
    617: "铜矿",
    618: "生铜",
    619: "铜板",
    620: "铜线",
    621: "一级科学机器",
    622: "二级科学机器",
    623: "电路板",
    624: "锡矿",
    625: "生锡",
    626: "锡线",
    627: "铜铁合金",
    628: "铜铁合金板",
    629: "致密铜铁合金板",
    630: "中级电路板",
    631: "三级科学机器碎片",
    632: "三级科学机器",
    633: "铜锡合金",
    634: "铜锡合金版",

    # events
    70: "随机怪物",
    71: "需要帮助的神秘人",

    # boss
    80: "岩石巨人", 81: "棕色波布克林",

    # boss skill
    91: "岩石重击",
    92: "岩石炮",
}
pocket = {"equip": {"weapon": 10, "armor": 0}, "inventory": [30]}
item_property = {
    # weapon
    10: {"atk": [1, 1], "type": "wep", "skill": [57], "description": "你无敌的手"},
    11: {"atk": [1, 3], "type": "wep", "skill": [56],
         "description": "一根普通的木棍，没有什么特别之处", "sell": 25},
    12: {"atk": [2, 4], "type": "wep", "skill": [51], "description": "经常能从波布克林身上找到的一个笨重的武器", "sell": 40,
         "craft": 0},
    13: {"atk": [4, 7], "type": "wep", "skill": [54], "description": "蓝色波布克林使用的武器，和普通波克棒不同，它的上方"
                                                                     "附有石板以增强攻击力", "sell": 60, "craft": 0},
    14: {"atk": [2, 3], "type": "wep", "skill": [52, 53], "description": "用神木制成的剑，有很强的灵气", "sell": 1320,
         "craft": 0},
    15: {"atk": [10, 20], "type": "wep", "skill": [54], "description": "莫力布林随身携带的武器，笨重但有效", "sell": 90},
    16: {"atk": [15, 30], "type": "wep", "skill": [54, 55], "description": "附有石板的莫力布林棍，以重量碾压对手",
         "sell": 190, "craft": 0},
    17: {"atk": [2, 3], "type": "wep", "skill": [56], "description": "普通的木剑", "sell": 180, "craft": 0},
    18: {"atk": [10, 26], "type": "wep", "skill": [54, 59, 510], "description": "海拉鲁王国的骑士所用的单手剑", "sell": 2500
        , "craft": 1},
    19: {"atk": [5, 9], "type": "wep", "skill": [511, 512, 513, 514],
         "description": "更强的桃木剑，更强的灵气！", "sell": 7800, "craft": 0},
    110: {"atk": [4, 6], "type": "wep", "skill": [515, 516], "description": "自然系的一级法杖，法杖核心是木之灵",
          "sell": 1300, "craft": 0},
    111: {"atk": [5, 8], "type": "wep", "skill": [517, 518, 519], "description": "自然系的二级法杖，法杖核心是木之心",
          "sell": 4500, "craft": 0},
    112: {"atk": [20, 25], "type": "wep", "skill": [520, 55], "description": "棕色波克布林所使用的武器，龙骨很尖锐",
          "sell": 1000},
    113: {"atk": [16, 26], "type": "wep", "skill": [54, 59, 521], "description": "海拉鲁王国的精英骑士所用的单手剑",
          "sell": 4000, "craft": 2},
    114: {"atk": [20, 30], "type": "wep", "skill": [520, 59, 521], "description": "海拉鲁王国的荣誉骑士所用的单手剑",
          "craft": 2, "sell": 9000},
    115: {"atk": [26, 30], "type": "wep", "skill": [520, 59, 521], "description": "海拉鲁王国的铂金骑士所用的单手剑",
          "craft": 3, "sell": 11000},
    116: {"atk": [35, 50], "type": "wep", "skill": [520, 59, 522], "description": "海拉鲁王国的钻石骑士所用的单手剑",
          "craft": 3, "sell": 22000},
    # armor
    21: {"def": 100, "miss": 50, "skill": [0], "type": "arm", "sell": 80,
         "description": "蓝色波克布林所使用的防具，十分简陋，但防御有效", "craft": 0},
    22: {"def": 200, "miss": 100, "skill": [0], "type": "arm", "description": "海拉鲁王国的士兵用的防具", "sell": 3500,
         "craft": 1},
    23: {"def": 450, "miss": 70, "skill": [0], "type": "arm", "description": "海拉鲁王国的骑士所用的防具", "sell": 7200,
         "craft": 1},
    # medicine
    30: {"heal": 2, "type": "med", "buff": [0],
         "description": "普通的布质绷带，能包裹你的伤口", "sell": 10},
    31: {"heal": 5, "type": "med", "buff": [0],
         "description": "洒上酒精的绷带，这使它的治疗效果增加了3", "sell": 50},
    32: {"heal": 30, "type": "mr",
         "description": "非常普通的法力回复剂", "sell": 10},
    33: {"heal": 100, "type": "sr",
         "description": "非常普通的体力回复剂, 因为制作材料很常见，所以很便宜", "sell": 5},
    34: {"heal": 40, "type": "med", "buff": [0],
         "description": "帮助神秘人后神秘人回赠的礼物，是一个发光的绿色小球，似乎与桃木剑有什么关系，非常珍贵", "sell": 1000},
    35: {"heal": 120, "type": "med", "buff": [0],
         "description": "由木之灵合成的绿色小球，似乎更有生命力了，有时能感受到小球在跳动，价值连城", "sell": 4200, "craft": 0},
    36: {"heal": 7, "type": "med", "buff": [0], "description": "在沙漠能找到的果子", "sell": 60},

    # mobs
    41: {"hp": 13, "atk": [1, 2], "type": "mob",
         "description": "一个浑身通红的怪物，四肢发达，头脑简单，还特别弱",
         "miss": 0, "define": 0, "gear": [11, 12], "gold": [5, 10], "exp": 5},
    42: {"hp": 25, "atk": [3, 4], "type": "mob",
         "description": "波布克林的一级加强版，聪明了些，武器也更加精良，甚至还有盔甲",
         "miss": 2, "define": 10, "gear": [13, 21], "gold": [18, 30], "exp": 12},
    43: {"hp": 5, "atk": [0, 1], "type": "mob",
         "description": "一个极弱的怪物，甚至有可能打出0点伤害...",
         "miss": 0, "define": 0, "gear": [11], "gold": [3, 7], "exp": 3},
    44: {"hp": 70, "atk": [5, 10], "type": "mob",
         "description": "波克布林的亲戚，更加强壮了，因此攻击力增强",
         "miss": 0, "define": 15, "gear": [15], "gold": [40, 85], "exp": 40},
    45: {"hp": 180, "atk": [10, 20], "type": "mob",
         "description": "莫力布林的一级加强版，武器更加精良，因为体型太大没有适合的盔甲",
         "miss": 1, "define": 18, "gear": [16], "gold": [90, 155], "exp": 100},

    # skill
    51: {"final": False, "type": "a", "atk": 10, "cost_mana": 20},
    52: {"final": False, "type": "c", "heal": 40, "cost_mana": 40},
    53: {"final": False, "type": "a", "atk": 28, "cost_mana": 35},
    54: {"final": False, "type": "a", "atk": 30, "cost_mana": 30},
    55: {"final": False, "type": "a", "atk": 45, "cost_mana": 40},
    56: {"final": False, "type": "a", "atk": 7, "cost_mana": 15},
    57: {"final": False, "type": "a", "atk": 5, "cost_mana": 30},
    58: {"final": False, "type": "a", "atk": 10, "cost_mana": 30},
    59: {"final": False, "type": "a", "atk": 20, "cost_mana": 25},
    510: {"final": False, "type": "c", "heal": 30, "cost_mana": 40},
    511: {"final": False, "type": "a", "atk": 60, "cost_mana": 35},
    512: {"final": False, "type": "c", "heal": 70, "cost_mana": 40},
    513: {"final": True, "type": "c;s", "heal": "all", "heal_s": "all", "cost_mana": 120},
    514: {"final": True, "type": "a;c", "heal": 40, "atk": 60, "cost_mana": 140},
    515: {"final": False, "type": "a", "atk": 35, "cost_mana": 25},
    516: {"final": False, "type": "a", "atk": 50, "cost_mana": 45},
    517: {"final": False, "type": "a", "atk": 60, "cost_mana": 35},
    518: {"final": False, "type": "c", "heal": 10, "cost_mana": 20},
    519: {"final": False, "type": "a", "atk": 30, "cost_mana": 10},
    520: {"final": False, "type": "a", "atk": 60, "cost_mana": 55},
    521: {"final": False, "type": "c", "heal": 45, "cost_mana": 40},
    522: {"final": False, "type": "c", "heal": 60, "cost_mana": 40},

    # materials
    61: {"type": "m", "description": "普通的石子", "sell": 1},
    62: {"type": "m", "description": "木板合成工具里的粘合剂部分", "sell": 25},
    63: {"type": "m", "description": "木板合成工具里的锯子及其他工具部分", "sell": 10},
    64: {"type": "m", "description": "完整的木板合成工具，可以加工出一块木板", "sell": 40, "craft": 0},
    65: {"type": "m", "description": "崭新的木板，由木板合成工具制成", "sell": 80, "craft": 0},
    66: {"type": "m", "description": "一块大石板，很重", "sell": 20, "craft": 0},
    67: {"type": "m", "description": "破旧的木板，没法使用", "sell": 30},
    68: {"type": "m", "description": "不纯的铁矿，无法使用", "sell": 100},
    69: {"type": "m", "description": "经过加工的铁矿，可以使用了", "sell": 200, "craft": 0},
    610: {"type": "m", "description": "完好的生铁加工工具，可以加工出一块生铁", "sell": 70},
    611: {"type": "m", "description": "一块铁板", "sell": 450, "craft": 1},
    612: {"type": "m", "description": "二重压缩的铁板", "sell": 950, "craft": 1},
    613: {"type": "m", "description": "铁制的握把，广泛用于制作各种铁质工具中", "sell": 500, "craft": 1},
    614: {"type": "m", "description": "空的一级魔法杖，可以放入灵或心来变为元素法杖", "sell": 220, "craft": 0},
    615: {"type": "m", "description": "一级科学机器的碎片", "sell": 240},
    616: {"type": "m", "description": "二级科学机器的碎片", "sell": 600},
    617: {"type": "m", "description": "不纯的铜矿，无法使用", "sell": 150},
    618: {"type": "m", "description": "经过加工的铜矿，可以使用了", "sell": 400, "craft": 1},
    619: {"type": "m", "description": "铜板，导电性很好", "sell": 500, "craft": 1},
    620: {"type": "m", "description": "铜线，导电性很好", "sell": 500, "craft": 1},
    621: {"type": "m", "craft": 0},
    622: {"type": "m", "craft": 1},
    623: {"type": "m", "description": "普通的电路板", "sell": 3000, "craft": 1},
    624: {"type": "m", "description": "不纯的锡矿, 无法使用", "sell": 200},
    625: {"type": "m", "description": "经过加工的锡矿, 可以使用了", "sell": 500, "craft": 2},
    626: {"type": "m", "description": "锡质导线，电能损耗降低了", "sell": 700, "craft": 2},
    627: {"type": "m", "description": "铜与铁的合金，更加坚硬", "sell": 700, "craft": 2},
    628: {"type": "m", "description": "铜与铁的合金做成的板，质地十分坚硬", "sell": 1600, "craft": 2},
    629: {"type": "m", "description": "二重压缩的铜铁合金板", "sell": 3500, "craft": 2},
    630: {"type": "m", "description": "可以处理更多数据和进行更多计算的电路板", "sell": 7000, "craft": 2},
    631: {"type": "m", "description": "三级科学机器的碎片", "sell": 1000},
    632: {"type": "m", "craft": 2},
    633: {"type": "m", "description": "铜与锡的合金", "sell": 1000, "craft": 3},
    634: {"type": "m", "description": "铜锡合金压制成的板", "sell": 2500, "craft": 3},
    635: {"type": "m", "description": "二重压缩的铜锡合金版", "sell": 5500, "craft": 3},

    # events
    70: {"type": "e", "*description": "summon a random mob"},
    71: {"type": "e", "*description": "a mystery man that need gold to help"},

    # boss
    80: {"type": "boss", "hp": 50, "atk": [5, 10], "skill": [50, 91, 92], "gear": [66, 66, 66, 68, 68],
         "gold": [80, 210], "exp": 90, "define": 20, "miss": 0, "description": "浑身是岩石的大块头"},
    81: {"type": "boss", "hp": 260, "atk": [25, 35], "skill": [520, 55], "gear": [21, 112], "gold": [300, 630],
         "exp": 210, "define": 10, "miss": 10, "description": "波布克林的二级加强版，超强"},

    # boss skill
    91: {"type": "a", "atk": 28},
    92: {"type": "a", "atk": 32},

    0: {"def": 0, "miss": 0},
}
player_property = {"lv": 1, "hp": 20, "max_hp": 20, "gold": 20, "miss": 5, "define": 0, "exp": 0, "km": 0.0, "place": 1,
                   "need exp": 10, "mana": 30, "max_mana": 30, "mana_reg": 1, "str": 50, "max_str": 50, "str_reg": 3,
                   "sm1": False, "sm2": False, "sm3": False}

craft_expr = {
    "一级科学机器碎片 * 4 + 生铁 * 2 -> 一级科学机器": "4 * 615; 2 * 69 -> 621",
    "二级科学机器碎片 * 10 + 电路板（需要一级科学机器）-> 二级科学机器": "10 * 616; 1 * 619; 4 * 620 -> 622",
    "三级科学机器碎片 * 15 + 中级电路板 -> 三级科学机器": "15 * 631; 1 * 630",
    "====================手====================": None,  # craft: 0
    "木棍 * 5 -> 波克棒": "5 * 11 -> 12", "小石子 * 9 -> 石板": "5 * 61 -> 66",
    "不完整的木板合成工具（P1）+ 不完整的木板合成工具（P2）-> 木板合成工具": "1 * 62; 1 * 63 -> 64",
    "木板合成工具 + 木棍 * 4 -> 木板": "1 * 64; 4 * 11 -> 65", "石板 * 4 -> 石板甲": "4 * 66 -> 21",
    "波克棒 + 石板 * 2 -> 石板波克棒": "1 * 12; 2 * 66 -> 13", "莫力布林棍 + 石板 * 6 -> 石板莫力布林棍": "1 * 15; 6 * 66 -> 16",
    "木板 * 2 + 木棍 * 1 -> 木剑": "2 * 65; 1 * 11 -> 17", "木板 * 4 + 木棍 * 2 -> 波克棒": "4 * 65; 2 * 11 -> 12",
    "破旧的木板 * 2 -> 木板": "2 * 67 -> 65", "木之灵 + 木剑 -> 桃木剑": "1 * 34; 1 * 17 -> 14",
    "铁矿 + 生铁加工工具 + 木棍 * 2 -> 生铁": "1 * 68; 1 * 610; 2 * 11 -> 69", "木之灵 * 4 -> 木之心": "4 * 34 -> 35",
    "桃木剑 * 2 + 木之心 -> 灵木剑": "2 * 14; 1 * 35 -> 19", "木板 * 2 + 木棍 * 2 -> 空魔法杖": "2 * 65; 1 * 11 -> 614",
    "空魔法杖I + 木之灵 -> 自然法杖I": "1 * 614; 1 * 34 -> 110", "空魔法杖 + 木之心 -> 自然法杖II": "1 * 614; 1 * 35 -> 111",
    "====================一级科学机器====================": None,  # craft: 1
    "生铁 * 2 -> 铁板": "2 * 69 -> 611", "铜矿 * 2 -> 生铜": "2 * 617 -> 618", "生铜 * 2 -> 铜板": "2 * 618 -> 619",
    "生铜 * 2 -> 铜线": "2 * 618 -> 620", "铜板 + 铜线 * 4 + 生铁 * 2 -> 电路板": "1 * 619; 4 * 620; 2 * 69 -> 623",
    "铁板 * 2 -> 致密铁板": "2 * 611 -> 612", "铁板 * 1 + 木棍 * 1 -> 铁柄": "1 * 611; 1 * 11 -> 613",
    "致密铁板 * 2 + 铁柄 -> 骑士之剑": "2 * 612; 1 * 613 -> 18",
    "铁板 * 7 -> 士兵之甲": "7 * 611 -> 22", "致密铁板 * 7 -> 骑士之甲": "7 * 612 -> 23",
    "====================二级科学机器====================": None,  # craft: 2
    "锡矿 * 2 -> 生锡": "2 * 624 -> 625", "生锡 -> 锡线": "1 * 625 -> 626", "生铁 * 2 + 生铜 * 2 -> 铜铁合金":
        "2 * 69; 2 * 618 -> 627", "铜铁合金 * 2 -> 铜铁合金板": "2 * 627 -> 628",
    "铜铁合金板 * 2 -> 致密铜铁合金板": "2 * 628 -> 629", "铜铁合金板 * 2 + 铁柄 -> 精英骑士之剑": "2 * 628; 1 * 613 -> 113",
    "致密铜铁合金板 * 2 + 铁柄 -> 荣誉骑士之剑": "2 * 629; 1 * 613 -> 114",
    "铜板 + 锡线 * 8 + 生锡 * 3 -> 中级电路板": "1 * 619; 8 * 626; 3 * 625 -> 630",
    "====================三级科学机器====================": None,  # craft: 3
    "生铜 * 3 + 生锡 * 3 -> 铜锡合金": "3 * 618; 3 * 625 -> 633", "铜锡合金 * 3 -> 铜锡合金板": "3 * 633 -> 634",
    "铜锡合金板 * 3 -> 致密铜锡合金版": "3 * 634 -> 635", "铜锡合金板 * 4 + 铁柄 -> 铂金骑士之剑": "4 * 634; 1 * 613 -> 115",
    "致密铜锡合金板 * 4 + 铁柄 -> 钻石骑士之剑": "4 * 635; 1 * 613 -> 116",
}

inventory_display = []

mobs = []

bosses = []

places = {1: "海拉鲁台地", 2: "海拉鲁山脉", 3: "哈特尔平原", 4: "南哈特尔山脉",
          5: "西哈特诺高原", 6: "中哈特诺盆地", 7: "东哈特尔雪山", 8: "南哈特尔山脉",
          9: "雷之台地", 10: "漂流物岬角", 11: "南海拉鲁平原", 12: "东努克尔沙漠",
          13: "中努克尔沙漠", 14: "北努克尔沙漠", 15: "南哈尔里丛林", 16: "哈尔里丛林深部", 17: "咕隆地区", 18: "死亡火山脚",
          19: "死亡火山腰", 20: "死亡火山口"}

explore_list = []

place_display = []
for i in places.keys():
    place_display.append(places[i])

breaking = False


# classes
class Mob:
    def __init__(self, namespace, max_hp, atk, description, miss, define, gear, gold, exp):
        self.namespace = namespace
        self.max_hp = max_hp
        self.hp = max_hp
        self.atk = atk
        self.description = description
        self.miss = miss
        self.define = define
        self.gear = gear
        self.gold = gold
        self.exp = exp


class Boss:
    def __init__(self, namespace, hp, skill, gear, gold, exp, atk, miss, define, description):
        self.namespace = namespace
        self.max_hp = hp
        self.hp = hp
        self.skill = skill
        self.gear = gear
        self.gold = gold
        self.exp = exp
        self.atk = atk
        self.miss = miss
        self.define = define
        self.description = description

    def random_skill(self):
        return random.choice(self.skill)

    def random_atk(self):
        return random.randint(self.atk[0], self.atk[1])


# functions
def die_detect():
    if player_property["hp"] <= 0:
        g.msgbox("你 死 了")
        if not settings.REBIRTH:
            g.msgbox("游戏退出中")
            exit()
        g.msgbox("某种神秘的力量将你从死亡拉了回来，不过他似乎抽取了一些费用")
        player_property["hp"] = 1
        player_property["gold"] -= int(player_property["gold"] * 0.2)


def add_explore(item, p, place):
    for time in range(p):
        explore_list[place - 1].append(item)


def get_key(value, dict_obj=None):
    if dict_obj is None:
        dict_obj = item_namespaces
    for key, val in dict_obj.items():
        if val == value:
            return key


def set_inventory_display(item_filter: list = None, pocket_yn: bool = False, selling: bool = False):
    """
    set up the display of the inventory for various modules, there is a filter to choose types
    :param selling: bool; if selling is true, then add the item's sell price to the item name's end
    :param pocket_yn: bool; if pocket is True, then add "合成界面" to inventory_display
    :param item_filter: list; a filter, list can only contain types
    """
    global inventory_display, pocket
    inventory_display = []
    if pocket_yn:
        inventory_display.append("合成界面")
    if item_filter is None:
        for i in pocket["inventory"]:
            if selling:
                inventory_display.append(item_namespaces[i] + f" {int(item_property[i]['sell'] / 4)}$")
            else:
                inventory_display.append(item_namespaces[i])
        while len(inventory_display) < 2:
            inventory_display.append("无")
    else:
        for i in pocket["inventory"]:
            if item_property[i]["type"] in item_filter:
                if selling:
                    inventory_display.append(item_namespaces[i] + f" {int(item_property[i]['sell'] / 4)}$")
                else:
                    inventory_display.append(item_namespaces[i])
        while len(inventory_display) < 2:
            inventory_display.append("无")


def mana_display(item_checking):
    """
    a function using at display
    """
    if item_property[item_checking]["heal"] == "all":
        player_property["hp"] = player_property["max_hp"]
        g.msgbox("你的HP回满了！")
    else:
        player_property["mana"] += item_property[item_checking]["heal"]
        g.msgbox("你回复了" + str(item_property[item_checking]["heal"]) + "点法力")
        if player_property["mana"] > player_property["max_mana"]:
            g.msgbox(f"你的法力溢出了\n可惜的是，{item_namespaces[item_checking]}似乎"
                     "不会帮你保存溢出的法力")
            player_property["mana"] = player_property["max_mana"]
        elif player_property["mana"] == player_property["max_mana"]:
            g.msgbox("你的法力满了")
        pocket["inventory"].remove(item_checking)


def cure_display(item_checking, skill=False):
    if item_property[item_checking]["heal"] == "all":
        player_property["hp"] = player_property["max_hp"]
        g.msgbox("你的HP回满了！")
    else:
        player_property["hp"] += item_property[item_checking]["heal"]
        g.msgbox("你回复了" + str(item_property[item_checking]["heal"]) + "点HP")
        if player_property["hp"] > player_property["max_hp"]:
            g.msgbox(f"你的HP溢出了\n可惜的是，{item_namespaces[item_checking]}似乎"
                     "不会帮你保存溢出的HP")
            player_property["hp"] = player_property["max_hp"]
        elif player_property["hp"] == player_property["max_hp"]:
            g.msgbox("你的HP满了")
    if not skill:
        pocket["inventory"].remove(item_checking)


def strength_display(item_checking):
    if item_property[item_checking]["heal"] == "all":
        player_property["hp"] = player_property["max_hp"]
        g.msgbox("你的HP回满了！")
    else:
        player_property["str"] += item_property[item_checking]["heal"]
        g.msgbox("你回复了" + str(item_property[item_checking]["heal"]) + "点体力")
        if player_property["str"] > player_property["max_str"]:
            g.msgbox(f"你的体力溢出了\n可惜的是，{item_namespaces[item_checking]}似乎"
                     "不会帮你保存溢出的体力")
            player_property["str"] = player_property["max_str"]
        elif player_property["str"] == player_property["max_str"]:
            g.msgbox("你的体力满了")
        pocket["inventory"].remove(item_checking)


def fight_ui():
    def attack_response():
        if random.randint(1, 100) < mob.miss:
            g.msgbox(f"{item_namespaces[mob.namespace]}似乎躲开了这次攻击")
        else:
            damage_current_value = item_property[skill_num]["atk"]
            damage = int(damage_current_value * (1 - mob.define * 0.01))
            mob.hp -= damage
            g.msgbox(f"你对{item_namespaces[mob.namespace]}造成了{damage}点伤害")

    mob_object = item_property[random.choice(mobs)]
    mob = Mob(get_key(mob_object, item_property), mob_object["hp"],
              mob_object["atk"], mob_object["description"], mob_object["miss"], mob_object["define"],
              mob_object["gear"], mob_object["gold"], mob_object["exp"])
    g.msgbox(f"{item_namespaces[mob.namespace]}出现了！")
    while True:
        die_detect()
        if mob.hp <= 0:
            gear = random.choice(mob.gear)
            gold = random.randint(mob.gold[0], mob.gold[1])
            g.msgbox("你胜利了")
            g.msgbox(f"你获得了{item_namespaces[gear]} * 1和{gold}$以及{mob.exp}点经验")
            pocket["inventory"].append(gear)
            player_property["gold"] += gold
            player_property["exp"] += mob.exp
            return 0
        fight_choose = g.indexbox(f"{item_namespaces[mob.namespace]} HP: {mob.hp}/{mob.max_hp}\n"
                                  f"“{player}”的HP: {player_property['hp']}/{player_property['max_hp']} "
                                  f"法力: {player_property['mana']}/{player_property['max_mana']} "
                                  f"体力: {player_property['str']}/{player_property['max_str']}",
                                  choices=["战斗", "查看", "物品", "逃跑"])
        if fight_choose == 0:
            skill_list_display = ["普通攻击"]
            for i in item_property[pocket["equip"]["weapon"]]["skill"]:
                skill_list_display.append(item_namespaces[i])
            skill_choose = g.choicebox("请选择使用的技能", choices=skill_list_display)
            if skill_choose == "无" or skill_choose is None:
                continue
            skill_num = get_key(skill_choose)
            if skill_num == 50:
                str_need = range_avg()
                if player_property["str"] < str_need:
                    g.msgbox("你没有足够的体力")
                    continue
                g.msgbox(f"你消耗了{str_need}点体力")
                player_property["str"] -= str_need
                if random.randint(1, 100) < mob.miss:
                    g.msgbox(f"{item_namespaces[mob.namespace]}似乎躲开了这次攻击")
                else:
                    if item_property[pocket["equip"]["weapon"]]["atk"][0] != \
                            item_property[pocket["equip"]["weapon"]]["atk"][1]:
                        damage_current_value = random.randint(
                            item_property[pocket["equip"]["weapon"]]["atk"][0],
                            item_property[pocket["equip"]["weapon"]]["atk"][1])
                    else:
                        damage_current_value = item_property[pocket["equip"]["weapon"]]["atk"][0]
                    damage = int(damage_current_value * (1 - mob.define * 0.01))
                    mob.hp -= damage
                    g.msgbox(f"你对{item_namespaces[mob.namespace]}造成了{damage}点伤害")
            else:
                if player_property["mana"] >= item_property[skill_num]["cost_mana"]:
                    player_property["mana"] -= item_property[skill_num]["cost_mana"]
                    g.msgbox(f"{player}消耗了{item_property[skill_num]['cost_mana']}点法力使出了“{skill_choose}”！")
                    if item_property[skill_num]["final"]:
                        skill_types = item_property[skill_num]["type"].split(";")
                        for skill_type in skill_types:
                            if skill_type == "a":
                                attack_response()
                            elif skill_type == "c":
                                cure_display(skill_num)
                            elif skill_type == "m":
                                mana_display(skill_num)
                            else:
                                strength_display(skill_num)

                    else:
                        if item_property[skill_num]["type"] == "a":
                            attack_response()
                        elif item_property[skill_num]["type"] == "c":
                            cure_display(skill_num)
                        elif item_property[skill_num]["type"] == "m":
                            mana_display(skill_num)
                        else:
                            strength_display(skill_num)
                else:
                    g.msgbox("你没有足够的法力！")
                    continue

        elif fight_choose == 1:
            g.msgbox(f"""
                    {item_namespaces[mob.namespace]}
                    HP: {mob.hp}/{mob.max_hp}
                    ATK: {mob.atk[0]}~{mob.atk[1]}
                    DEF: {mob.define}%
                    MISS: {mob.miss}%
                    “{mob.description}”
                    """)
        elif fight_choose == 2:
            quit_yn = False
            while True:
                set_inventory_display(["med", "mr", "sr"])
                item_using = g.choicebox("请选择你要使用的物品（只有药物）", choices=inventory_display)
                if item_using is None:
                    quit_yn = True
                    break
                item_using = get_key(item_using)
                if item_using == 0:
                    g.msgbox("你想使用空气吗？")
                else:
                    if item_property[item_using]["type"] == "med":
                        cure_display(item_using)
                    elif item_property[item_using]["type"] == "mr":
                        mana_display(item_using)
                    else:
                        strength_display(item_using)
                    break
            if quit_yn:
                continue
        elif fight_choose == 3 or fight_choose is None:
            if g.ccbox("你确定要逃跑吗？", choices=["是的", "不了"]):
                g.msgbox("你逃跑了")
                return 1
            else:
                continue
        if random.randint(1, 100) < player_property["miss"] * 0.01 + \
                item_property[pocket["equip"]["armor"]]["miss"] * 0.01:
            g.msgbox(f"你似乎躲开了这次攻击")
        else:
            damage = int(random.randint(mob.atk[0], mob.atk[1]) * (1 - (player_property["define"] +
                                                                        item_property[
                                                                            pocket["equip"]["armor"]][
                                                                            "def"]) * 0.0001))
            player_property["hp"] -= damage
            g.msgbox(f"{item_namespaces[mob.namespace]}对你造成了{damage}点伤害")
        player_property["str"] += player_property["str_reg"]
        g.msgbox(f"你回复了{player_property['str_reg']}体力")
        if player_property["str"] > player_property["max_str"]:
            player_property["str"] = player_property["max_str"]
            g.msgbox("你的体力溢出了，可你无法保存溢出的体力")
        player_property["mana"] += player_property["mana_reg"]
        g.msgbox(f"你回复了{player_property['mana_reg']}法力")
        if player_property["mana"] > player_property["max_mana"]:
            player_property["mana"] = player_property["max_mana"]
            g.msgbox("你的法力溢出了，可你无法保存溢出的法力")
    check_level()


def range_avg():
    return int((item_property[pocket["equip"]["weapon"]]["atk"][0] + item_property[pocket["equip"]["weapon"]]["atk"][1])
               / 2)


def check_level():
    global player_property
    if player_property["exp"] >= player_property["need exp"]:
        player_property["lv"] += 1
        player_property["exp"] = player_property["exp"] - player_property["need exp"]
        player_property["need exp"] = player_property["lv"] * (10 + player_property["lv"]) + player_property["lv"] - 1
        player_property["max_hp"] = player_property["lv"] * 10 + int(player_property["lv"] * 2 - 1)
        player_property["hp"] = player_property["max_hp"]
        player_property["max_mana"] = player_property["lv"] * 10 + 20
        player_property["mana"] = player_property["max_mana"]
        player_property["mana_reg"] = int(player_property["lv"] / 5) + 1
        player_property["str"] = player_property["lv"] * 35 + 15
        player_property["max_str"] = player_property["str"]
        player_property["str_reg"] = int(player_property["lv"] * 0.1) + 1
        g.msgbox(f"你升级了！\n你目前的LV为{player_property['lv']}\n"
                 f"你的HP上限变为了{player_property['max_hp']}\n你的HP回满了\n你的法力上限变为了{player_property['max_mana']}"
                 f"\n你的法力回满了\n你的体力上限变为了{player_property['max_str']}\n你的体力回满了")


def set_skill(ic):
    skill_display: str = ""
    for i in item_property[ic]["skill"]:
        skill_display += item_namespaces[i]
        if item_property[ic]["skill"].index(i) != \
                len(item_property[ic]["skill"]) - 1:
            skill_display += " "
    return skill_display


def craft_expr_interpreter(expr):
    materials_namespace = []
    expr = expr.split("->")
    expr[0] = expr[0].split(";")
    for materials in expr[0]:
        materials = materials.split("*")
        for i in range(int(materials[0])):
            materials_namespace.append(int(materials[1]))
    return materials_namespace, int(expr[1])


def _makedir(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass


def _makefile(name):
    try:
        fd = open(name, mode="w", encoding="utf-8")
        fd.close()
    except FileExistsError:
        pass


def _back():
    os.chdir(os.path.dirname(os.getcwd()))


def _get_path():
    return os.getcwd()


def _option_go(path):
    os.chdir(path)


def _update_save():
    with open(player, "w") as save_obj:
        save_txt = str(player_property) + "\n" + str(pocket)
        save_obj.write(base64.b64encode(save_txt.encode()).decode())


def _update_save_version():
    for i in settings.PROPERTY_KEY:
        if i not in player_property.keys():
            exec(settings.PROPERTY_EXPR[i])
    _update_save()


for i in range(20):
    explore_list.append([])
# place 1
add_explore(615, 1, 1)
add_explore(62, 2, 1)
add_explore(67, 2, 1)
add_explore(71, 2, 1)
add_explore(63, 3, 1)
add_explore(68, 4, 1)
add_explore(610, 10, 1)
add_explore(11, 10, 1)
add_explore(70, 10, 1)
add_explore(61, 56, 1)
# place 2
add_explore(62, 1, 2)
add_explore(67, 1, 2)
add_explore(71, 1, 2)
add_explore(63, 2, 2)
add_explore(68, 8, 2)
add_explore(610, 5, 2)
add_explore(11, 10, 2)
add_explore(70, 10, 2)
add_explore(61, 60, 2)
# place 3
add_explore(62, 4, 3)
add_explore(67, 2, 3)
add_explore(71, 1, 3)
add_explore(63, 7, 3)
add_explore(610, 6, 3)
add_explore(11, 10, 3)
add_explore(70, 20, 3)
add_explore(61, 50, 3)
# place 4
add_explore(68, 10, 4)
add_explore(11, 4, 4)
add_explore(70, 30, 4)
add_explore(61, 56, 4)
# place 5
add_explore(68, 5, 5)
add_explore(70, 35, 5)
add_explore(61, 55, 5)
# place 6
add_explore(67, 5, 6)
add_explore(64, 4, 6)
add_explore(71, 5, 6)
add_explore(68, 5, 6)
add_explore(610, 5, 6)
add_explore(11, 10, 6)
add_explore(70, 10, 6)
add_explore(61, 56, 6)
# place 7
add_explore(610, 5, 7)
add_explore(617, 10, 7)
add_explore(615, 15, 7)
add_explore(70, 20, 7)
add_explore(61, 50, 7)
# place 8
add_explore(68, 10, 8)
add_explore(617, 10, 8)
add_explore(616, 15, 8)
add_explore(70, 15, 8)
add_explore(61, 50, 8)
# place 9
add_explore(67, 2, 9)
add_explore(68, 8, 9)
add_explore(617, 10, 9)
add_explore(610, 10, 9)
add_explore(70, 20, 9)
add_explore(61, 50, 9)
# place 10
add_explore(70, 6, 10)
add_explore(616, 10, 10)
add_explore(67, 14, 10)
add_explore(610, 15, 10)
add_explore(615, 20, 10)
add_explore(617, 20, 10)
add_explore(68, 30, 10)
# place 11
add_explore(62, 2, 11)
add_explore(67, 2, 11)
add_explore(71, 3, 11)
add_explore(63, 3, 11)
add_explore(610, 4, 11)
add_explore(11, 6, 11)
add_explore(70, 40, 11)
add_explore(61, 40, 11)
# place 12
add_explore(36, 5, 12)
add_explore(624, 10, 12)
add_explore(617, 25, 12)
add_explore(68, 30, 12)
add_explore(70, 30, 12)
# place 13
add_explore(624, 10, 13)
add_explore(617, 20, 13)
add_explore(68, 25, 13)
add_explore(70, 45, 13)
# place 14
add_explore(36, 5, 14)
add_explore(624, 15, 14)
add_explore(617, 25, 14)
add_explore(70, 25, 14)
add_explore(68, 30, 14)
# place 15
add_explore(68, 5, 15)
add_explore(65, 10, 15)
add_explore(11, 10, 15)
add_explore(70, 20, 15)
add_explore(67, 25, 15)
add_explore(71, 30, 15)
# place 16
add_explore(11, 5, 16)
add_explore(65, 25, 16)
add_explore(67, 30, 16)
add_explore(71, 40, 16)
# place 17
add_explore(70, 10, 17)
add_explore(624, 20, 17)
add_explore(617, 30, 17)
add_explore(68, 40, 17)
# place 18
add_explore(70, 15, 18)
add_explore(624, 15, 18)
add_explore(617, 30, 18)
add_explore(68, 40, 18)
# place 19
add_explore(624, 15, 19)
add_explore(617, 15, 19)
add_explore(68, 30, 19)
add_explore(70, 40, 19)
# place 20
add_explore(624, 5, 20)
add_explore(617, 10, 20)
add_explore(70, 85, 20)

run_environment = _get_path()
_makedir("save")
_option_go("save")
saves = os.listdir()
for save in saves:
    save.replace(run_environment, "")
g.msgbox("""
                                  fight dv-006
                                      欢迎
""")
saves.append("创建新存档")
while len(saves) < 2:
    saves.append("无")
while True:
    save = g.choicebox("请选择存档", choices=saves)
    if save is None:
        exit()
    elif save == "创建新存档":
        breaking = False
        while True:
            player = g.enterbox("请输入玩家的名字")
            if player == "":
                continue
            elif player is None:
                break
            elif player in saves:
                if g.ccbox(f"\"{player}\"是一个已经被用过的名字，是否要覆盖原存档（请经过存档主人同意后操作）",
                           choices=["是的", "不了"]):
                    _makefile(player)
                    _update_save()
                    breaking = True
                    break
                else:
                    continue
            else:
                _makefile(player)
                _update_save()
                breaking = True
                break
        if breaking:
            break
    else:
        player = save
        with open(save) as save_obj:
            save_txt = save_obj.read().rstrip().encode()
            save_txt = base64.b64decode(save_txt).decode()
            save_txt_list = save_txt.split("\n")
            exec("player_property = " + save_txt_list[0])
            exec("pocket = " + save_txt_list[1])
            _update_save_version()
        g.msgbox(f"存档已读取\n欢迎回来，{player}！")
        break

# get mob list
for i in item_property.keys():
    if str(i)[0] == "4":
        mobs.append(i)

# get boss list
for i in item_property.keys():
    if str(i)[0] == "8":
        bosses.append(item_namespaces[i])

while True:
    check_level()
    choose = g.indexbox(f"你好，{player}！\n", choices=["状态", "背包", "探索", "商店", "贤者", "与普通怪物战斗",
                                                    "与Boss级怪物战斗", "存档"])
    if choose is None:
        g.msgbox("再见")
        exit()

    # status UI
    if choose == 0:
        g.msgbox(f"""
{player}
LV: {player_property["lv"]}
EXP: {player_property["exp"]}/{player_property["need exp"]}
HP: {player_property["hp"]}/{player_property["max_hp"]}
体力: {player_property["str"]}/{player_property["max_str"]}
体力回复: {player_property["str_reg"]}
法力: {player_property["mana"]}/{player_property["max_mana"]}
法力回复: {player_property["mana_reg"]}
现金: {player_property["gold"]}$
武器：{item_namespaces[pocket["equip"]["weapon"]]}  ATK {item_property[pocket["equip"]["weapon"]]["atk"][0]} ~ {item_property[pocket["equip"]["weapon"]]["atk"][1]} 
盔甲：{item_namespaces[pocket["equip"]["armor"]]}  DEF {item_property[pocket["equip"]["armor"]]["def"]}
        """)
    # pocket UI
    elif choose == 1:
        while True:
            check_pos = g.ccbox("请选择你要查看的物品位置", choices=["已装备的物品", "物品栏"])
            if check_pos is None:
                break

            # equipped item
            if check_pos:
                while True:
                    item_checking = g.choicebox("请选择你要操作的物品", choices=[item_namespaces[pocket["equip"]["weapon"]],
                                                                       item_namespaces[pocket["equip"]["armor"]]
                                                                       ])
                    if item_checking is None:
                        break
                    item_checking = get_key(item_checking)
                    if item_checking == 0:
                        g.msgbox("你想操作空气吗？")
                    elif item_property[item_checking]["type"] == "wep":
                        while True:
                            use = g.indexbox(f"{item_namespaces[item_checking]}", choices=["卸下", "信息", "丢弃"])
                            if use is None:
                                break
                            elif use == 0:
                                if item_checking == 10:
                                    g.msgbox("你不能砍掉你的手！")
                                else:
                                    pocket["inventory"].append(item_checking)
                                    pocket["equip"]["weapon"] = 10
                                    break
                            elif use == 1:
                                g.msgbox(f"""
{item_namespaces[item_checking]}
atk: {item_property[item_checking]["atk"][0]} ~ {item_property[item_checking]["atk"][1]}
技能: {set_skill(item_checking)}
“{item_property[item_checking]["description"]}”
    """)
                            elif use == 2:
                                if item_checking == 10:
                                    g.msgbox("你不能砍掉你的手！")
                                    continue
                                elif item_property[item_checking]["type"] == "wep":
                                    pocket["equip"]["weapon"] = 10
                                else:
                                    pocket["equip"]["armor"] = 0
                                g.msgbox(f"{item_namespaces[item_checking]}被扔的远远的")
                                break
                    elif item_property[item_checking]["type"] == "arm":
                        while True:
                            use = g.indexbox(f"{item_namespaces[item_checking]}", choices=["卸下", "信息", "丢弃"])
                            if use is None:
                                break
                            elif use == 0:
                                if item_checking == 10:
                                    g.msgbox("你不能剥掉你的皮！")
                                else:
                                    pocket["inventory"].append(item_checking)
                                    pocket["equip"]["armor"] = 0
                                    break
                            elif use == 1:
                                g.msgbox(f"""
{item_namespaces[item_checking]}
def: +{item_property[item_checking]["def"]}
miss: +{item_property[item_checking]["miss"]}
技能: {set_skill(item_checking)}
“{item_property[item_checking]["description"]}”
                            """)
                            elif use == 2:
                                if item_checking == 0:
                                    g.msgbox("你不能剥掉你的皮！")
                                    continue
                                elif item_property[item_checking]["type"] == "wep":
                                    pocket["equip"]["weapon"] = 10
                                else:
                                    pocket["equip"]["armor"] = 0
                                g.msgbox(f"{item_namespaces[item_checking]}被扔的远远的")
                                break
            else:
                while True:
                    set_inventory_display(pocket_yn=True)
                    item_checking = g.choicebox("请选择你要操作的物品", choices=inventory_display)
                    if item_checking is None:
                        break
                    elif item_checking == "合成界面":
                        while True:
                            if player_property["sm1"]:
                                craft_expr.pop("一级科学机器碎片 * 4 + 生铁 * 2 -> 一级科学机器", None)
                            elif player_property["sm2"]:
                                craft_expr.pop("二级科学机器碎片 * 10 + 电路板（需要一级科学机器）-> 二级科学机器", None)
                            elif player_property["sm3"]:
                                craft_expr.pop("三级科学机器碎片 * 15 + 中级电路板 -> 三级科学机器", None)
                            craft_display = []
                            for craft_key in craft_expr.keys():
                                craft_display.append(craft_key)
                            sm_display = []
                            for i in range(3):
                                if player_property[f"sm{i + 1}"]:
                                    sm_display.append("✔")
                                else:
                                    sm_display.append("❌")
                            crafting_item = g.choicebox(f"请选择你要合成的物品 一级科学机器: {sm_display[0]}"
                                                        f"二级科学机器: {sm_display[1]} 三级科学机器: {sm_display[2]}",
                                                        choices=craft_display)
                            if crafting_item is None:
                                break
                            elif craft_expr[crafting_item] is None:
                                continue
                            craft_materials = craft_expr_interpreter(craft_expr[crafting_item])
                            if item_property[craft_materials[1]]["craft"] == 1 and not player_property["sm1"]:
                                g.msgbox("你没有一级科学机器")
                                continue
                            elif item_property[craft_materials[1]]["craft"] == 2 and not player_property["sm2"]:
                                g.msgbox("你没有二级科学机器")
                                continue
                            materials_collections = collections.Counter(craft_materials[0])
                            pocket_collections = collections.Counter(pocket["inventory"])
                            cyn = False
                            for mat in materials_collections.keys():
                                cyn = False
                                if mat not in pocket_collections:
                                    g.msgbox("你没有足够的材料")
                                    cyn = True
                                    break
                                elif pocket_collections[mat] < materials_collections[mat]:
                                    g.msgbox("你没有足够的材料")
                                    cyn = True
                                    break
                            if cyn:
                                continue
                            for mat in craft_materials[0]:
                                pocket["inventory"].remove(mat)
                            g.msgbox(f"你合成了{item_namespaces[craft_materials[1]]}")
                            if craft_materials[1] == 621:
                                player_property["sm1"] = True
                            elif craft_materials[1] == 622:
                                player_property["sm2"] = True
                            else:
                                pocket["inventory"].append(craft_materials[1])

                        continue
                    item_checking = get_key(item_checking)
                    if item_checking == 0:
                        g.msgbox("你想操作空气吗？")
                    elif item_property[item_checking]["type"] == "wep":
                        while True:
                            use = g.indexbox(f"{item_namespaces[item_checking]}", choices=["装备", "信息", "丢弃"])
                            if use is None:
                                break
                            elif use == 0:
                                if pocket["equip"]["weapon"] != 10:
                                    pocket["inventory"].append(pocket["equip"]["weapon"])
                                pocket["inventory"].remove(item_checking)
                                pocket["equip"]["weapon"] = item_checking
                                break
                            elif use == 1:

                                g.msgbox(f"""
{item_namespaces[item_checking]}
ATK: {item_property[item_checking]["atk"][0]} ~ {item_property[item_checking]["atk"][1]}
技能: {set_skill(item_checking)}
“{item_property[item_checking]["description"]}”
""")
                            elif use == 2:
                                pocket["inventory"].remove(item_checking)
                                g.msgbox(f"{item_namespaces[item_checking]}被扔的远远的")
                                break
                    elif item_property[item_checking]["type"] == "arm":
                        while True:
                            use = g.indexbox(f"{item_namespaces[item_checking]}", choices=["装备", "信息", "丢弃"])
                            if use is None:
                                break
                            elif use == 0:
                                if pocket["equip"]["armor"] != 0:
                                    pocket["inventory"].append(item_checking)
                                pocket["inventory"].remove(item_checking)
                                pocket["equip"]["armor"] = item_checking
                                break
                            elif use == 1:
                                g.msgbox(f"""
{item_namespaces[item_checking]}
def: +{item_property[item_checking]["def"]}
miss: +{item_property[item_checking]["miss"]}
技能: {set_skill(item_checking)}
“{item_property[item_checking]["description"]}”
""")
                            elif use == 2:
                                pocket["inventory"].remove(item_checking)
                                g.msgbox(f"{item_namespaces[item_checking]}被扔的远远的")
                                break
                    elif item_property[item_checking]["type"] == "med" or item_property[item_checking]["type"] == "mr" \
                            or item_property[item_checking]["type"] == "sr":
                        while True:
                            use = g.indexbox(f"{item_namespaces[item_checking]}", choices=["使用", "信息", "丢弃"])
                            if use is None:
                                break
                            elif use == 0:
                                if item_property[item_checking]["type"] == "med":
                                    cure_display(item_checking)
                                elif item_property[item_checking]["type"] == "mr":
                                    mana_display(item_checking)
                                else:
                                    strength_display(item_checking)
                                break
                            elif use == 1:
                                if item_property[item_checking]["type"] == "med":
                                    g.msgbox(f"""
{item_namespaces[item_checking]}
回复{item_property[item_checking]["heal"]}点HP
“{item_property[item_checking]["description"]}”
    """)
                                elif item_property[item_checking]["type"] == "mr":
                                    g.msgbox(f"""
{item_namespaces[item_checking]}
回复{item_property[item_checking]["heal"]}点法力
“{item_property[item_checking]["description"]}”
                                        """)
                                else:
                                    g.msgbox(f"""
{item_namespaces[item_checking]}
回复{item_property[item_checking]["heal"]}点体力
“{item_property[item_checking]["description"]}”
                                                                            """)
                            elif use == 2:
                                pocket["inventory"].remove(item_checking)
                                g.msgbox(f"{item_namespaces[item_checking]}被扔的远远的")
                                break
                    elif item_property[item_checking]["type"] == "m":
                        while True:
                            use = g.indexbox(f"{item_namespaces[item_checking]}", choices=["使用", "信息", "丢弃"])
                            if use is None:
                                break
                            if use == 0:
                                g.msgbox("你无法使用一个材料")
                            elif use == 1:
                                g.msgbox(f"""
{item_namespaces[item_checking]}
“{item_property[item_checking]["description"]}”
""")
                                pocket["inventory"].remove(item_checking)
                                g.msgbox(f"{item_namespaces[item_checking]}被扔的远远的")
                                break
    # explore UI
    elif choose == 2:
        while True:
            if g.ccbox(f"“{player}”的HP: {player_property['hp']}/{player_property['max_hp']} "
                       f"法力: {player_property['mana']}/{player_property['max_mana']} "
                       f"体力: {player_property['str']}/{player_property['max_str']}\n"
                       f"目前位置: {places[player_property['place']]} {player_property['km']} / 10 km\n"
                       f"是否继续前进？", choices=["是的（消耗5体力）", "不了"]):
                if player_property['str'] < 5:
                    g.msgbox("你没有足够的体力")
                    break
                player_property["str"] -= 5
                player_property['km'] += 0.1
                player_property['km'] = round(player_property['km'], 1)
                event = random.choice(explore_list[player_property["place"] - 1])
                if event == 70:
                    fight_ui()
                elif event == 71:
                    need_gold = random.randint(player_property["lv"] * 10, player_property["lv"] * 20)
                    if g.ccbox(f"一个神秘人向你走来，说到：“战士，我没有剩余的盘缠了，施舍一点吧，只要{need_gold}$就行”\n"
                               f"你是否要对他伸出援手？", choices=["是的", "不了"]):
                        if player_property["gold"] < need_gold:
                            g.msgbox("你没有足够的钱")
                            g.msgbox("神秘人：“算了吧小伙子，我看你也没多少钱啊”\n话音刚落，他便化作树叶随风而去了")
                        else:
                            g.msgbox("“谢谢你，战士，这个作为回礼送给你，再见”\n话音刚落，他便化作树叶随风而去了")
                            pocket["inventory"].append(34)
                            g.msgbox("你获得了木之灵")
                    else:
                        g.msgbox("神秘人：“那好吧，再见”\n话音刚落，他便化作树叶随风而去了")
                else:
                    pocket["inventory"].append(event)
                    g.msgbox(f"你获得了{item_namespaces[event]}")
                if player_property['km'] == 10:
                    if player_property['place'] != 20:
                        teleport = g.choicebox("你来到了地区之间的传送点，你是否要传送呢，可传送的地点列表如下",
                                               choices=place_display)
                        if teleport is None:
                            player_property["place"] += 1
                            g.msgbox(f"你来到了{places[player_property['place']]}!")
                        else:
                            player_property["place"] = get_key(teleport, places)
                            g.msgbox(f"你传送到了{teleport}")
                    else:
                        if g.ccbox("前方就是大灾厄盖侬的巢穴了，你是否要进入挑战呢（不挑战则回到海拉鲁台地）"):
                            g.msgbox("暂未完成，按下OK回到海拉鲁台地（作者的吐槽：打得好快）")
                            player_property["place"] = 1
                        else:
                            g.msgbox("正在回到海拉鲁台地（作者的吐槽：打得好快）")
                            player_property["place"] = 1
                    player_property["km"] = 0.0

            else:
                break

    # shop UI
    elif choose == 3:
        while True:
            item_buying = g.choicebox("请选择你要购买的物品",
                                      choices=["收购", item_namespaces[30], item_namespaces[14], item_namespaces[11],
                                               item_namespaces[31], item_namespaces[32], item_namespaces[33],
                                               item_namespaces[68], item_namespaces[617], item_namespaces[624],
                                               item_namespaces[610], item_namespaces[615],
                                               item_namespaces[616], item_namespaces[631]])
            if item_buying is None:
                break
            elif item_buying == "收购":
                while True:
                    set_inventory_display(selling=True)
                    item_selling = g.choicebox("请选择你要出售的物品", choices=inventory_display)
                    if item_selling is None:
                        break
                    item_selling = item_selling.split(" ")[0]
                    item_selling = get_key(item_selling)
                    get_gold = int(item_property[item_selling]["sell"] / 4)
                    player_property["gold"] += get_gold
                    pocket["inventory"].remove(item_selling)
                    g.msgbox(f"你通过出售{item_namespaces[item_selling]}获得了{get_gold}$")
                continue
            item_buying = get_key(item_buying)
            if g.ccbox(f"""
{item_namespaces[item_buying]}
{item_property[item_buying]["sell"]}$
{item_property[item_buying]["description"]}
            """, choices=["购买", "取消"]):
                if player_property["gold"] >= item_property[item_buying]["sell"]:
                    player_property["gold"] -= item_property[item_buying]["sell"]
                    pocket["inventory"].append(item_buying)
                    g.msgbox(f"你花费{item_property[item_buying]['sell']}$购买了"
                             f"{item_namespaces[item_buying]}")
                else:
                    g.msgbox("你没有足够的钱")
    # sage UI
    elif choose == 4:
        while True:
            set_inventory_display()
            set_up = g.choicebox("贤者：战士，向我献祭你的一件物品，我将根据这件物品的价值，为你回复血量", choices=inventory_display)
            if set_up is None:
                break
            if set_up == "无":
                g.msgbox("贤者：你想献祭空气给我吗？")
                continue
            set_up = get_key(set_up)
            if item_property[set_up]["type"] == "med":
                cure = int(item_property[set_up]["sell"] / 8)
            else:
                cure = int(item_property[set_up]["sell"] / 4)
            player_property["hp"] += cure
            pocket["inventory"].remove(set_up)
            g.msgbox(f"经过贤者的治疗，你回复了{cure}点HP！")
            if player_property["hp"] == player_property["max_hp"]:
                g.msgbox("你的HP满了")
            if player_property["hp"] > player_property["max_hp"]:
                player_property["hp"] = player_property["max_hp"]
                g.msgbox("你的HP溢出了，可惜，即使是贤者，也无法帮你保存溢出的HP")
            if not g.ccbox("贤者：你是否要继续献祭呢？", choices=["是的", "不了"]):
                break
    # normal fight UI
    elif choose == 5:
        while True:
            return_code = fight_ui()
            if return_code:
                break
            if not g.ccbox("你是否要继续战斗（注意，你的血量不会回复）", choices=["是的", "不了"]):
                break
    # Boss fight UI
    elif choose == 6:
        while True:
            boss_fighting = g.choicebox("请选择你要挑战的Boss", choices=bosses)
            if boss_fighting is None:
                break
            boss_object = item_property[get_key(boss_fighting)]
            boss = Boss(get_key(boss_fighting), boss_object["hp"], boss_object["skill"], boss_object["gear"],
                        boss_object["gold"], boss_object["exp"], boss_object["atk"],
                        boss_object["miss"], boss_object["define"], boss_object["description"])
            g.msgbox(f"{item_namespaces[boss.namespace]}出现了！")
            while True:
                if boss.hp <= 0:
                    gear_display = ""
                    for gear in boss.gear:
                        gear_display += item_namespaces[gear]
                        if boss.gear.index(gear) != len(boss.gear) - 1:
                            gear_display += "，"
                        pocket["inventory"].append(gear)
                    gold = random.randint(boss.gold[0], boss.gold[1])
                    g.msgbox("你胜利了")
                    player_property["gold"] += gold
                    player_property["exp"] += boss.exp
                    g.msgbox(f"你获得了{gold}$和{boss.exp}点经验")
                    g.msgbox(f"你获得了 {gear_display}")
                    break
                boss_skill_using = boss.random_skill()
                g.msgbox(f"{item_namespaces[boss.namespace]}使出了{item_namespaces[boss_skill_using]}")
                if random.randint(1, 100) < player_property["miss"] * 0.01 + \
                        item_property[pocket["equip"]["armor"]]["miss"] * 0.01:
                    g.msgbox(f"你似乎躲开了这次攻击")
                else:
                    damage = int(boss.random_atk() * (1 - (player_property["define"] +
                                                           item_property[
                                                               pocket["equip"]["armor"]][
                                                               "def"]) * 0.0001))
                    g.msgbox(f"{item_namespaces[boss.namespace]}对你造成了{damage}点伤害")
                    player_property["hp"] -= damage
                while True:
                    die_detect()
                    fight_choose = g.indexbox(f"{item_namespaces[boss.namespace]} HP: {boss.hp}/{boss.max_hp}\n"
                                              f"“{player}”的HP: {player_property['hp']}/{player_property['max_hp']} "
                                              f"法力: {player_property['mana']}/{player_property['max_mana']} "
                                              f"体力: {player_property['str']}/{player_property['max_str']}",
                                              choices=["战斗", "查看", "物品"])
                    if fight_choose == 0:
                        skill_list_display = ["普通攻击"]
                        for i in item_property[pocket["equip"]["weapon"]]["skill"]:
                            skill_list_display.append(item_namespaces[i])
                        skill_choose = g.choicebox("请选择使用的技能", choices=skill_list_display)
                        if skill_choose == "无" or skill_choose is None:
                            continue
                        skill_num = get_key(skill_choose)
                        if skill_num == 50:
                            str_need = range_avg()
                            if player_property["str"] < str_need:
                                g.msgbox("你没有足够的体力")
                                continue
                            g.msgbox(f"你消耗了{str_need}点体力")
                            player_property["str"] -= str_need
                            if random.randint(1, 100) < boss.miss:
                                g.msgbox(f"{item_namespaces[boss.namespace]}似乎躲开了这次攻击")
                            else:
                                if item_property[pocket["equip"]["weapon"]]["atk"][0] != \
                                        item_property[pocket["equip"]["weapon"]]["atk"][1]:
                                    damage_current_value = random.randint(
                                        item_property[pocket["equip"]["weapon"]]["atk"][0],
                                        item_property[pocket["equip"]["weapon"]]["atk"][1])
                                else:
                                    damage_current_value = item_property[pocket["equip"]["weapon"]]["atk"][0]
                                damage = int(damage_current_value * (1 - boss.define * 0.01))
                                boss.hp -= damage
                                g.msgbox(f"你对{item_namespaces[boss.namespace]}造成了{damage}点伤害")
                        else:
                            if player_property["mana"] >= item_property[skill_num]["cost_mana"]:
                                player_property["mana"] -= item_property[skill_num]["cost_mana"]
                                g.msgbox(f"{player}消耗了{item_property[skill_num]['cost_mana']}点法力使出了“{skill_choose}”！")
                                if item_property[skill_num]["final"]:
                                    skill_types = item_property[skill_num]["type"].split(";")
                                    for skill_type in skill_types:
                                        if skill_type == "a":
                                            if random.randint(1, 100) < boss.miss:
                                                g.msgbox(f"{item_namespaces[boss.namespace]}似乎躲开了这次攻击")
                                            else:
                                                damage_current_value = item_property[skill_num]["atk"]
                                                damage = int(damage_current_value * (1 - boss.define * 0.01))
                                                boss.hp -= damage
                                                g.msgbox(f"你对{item_namespaces[boss.namespace]}造成了{damage}点伤害")
                                        elif skill_type == "c":
                                            cure_display(skill_num, True)
                                        elif skill_type == "m":
                                            mana_display(skill_num)
                                        else:
                                            strength_display(skill_num)

                                else:
                                    if item_property[skill_num]["type"] == "a":
                                        if random.randint(1, 100) < boss.miss:
                                            g.msgbox(f"{item_namespaces[boss.namespace]}似乎躲开了这次攻击")
                                        else:
                                            damage_current_value = item_property[skill_num]["atk"]
                                            damage = int(damage_current_value * (1 - boss.define * 0.01))
                                            boss.hp -= damage
                                            g.msgbox(f"你对{item_namespaces[boss.namespace]}造成了{damage}点伤害")
                                    elif item_property[skill_num]["type"] == "c":
                                        cure_display(skill_num, True)
                                    elif item_property[skill_num]["type"] == "m":
                                        mana_display(skill_num)
                                    else:
                                        strength_display(skill_num)
                            else:
                                g.msgbox("你没有足够的法力！")
                                continue
                        break

                    elif fight_choose == 1:
                        g.msgbox(f"""
{item_namespaces[boss.namespace]}
HP: {boss.hp}/{boss.max_hp}
ATK: {boss.atk[0]}~{boss.atk[1]}
DEF: {boss.define}%
MISS: {boss.miss}%
“{boss.description}”
                                        """)
                        break
                    elif fight_choose == 2:
                        quit_yn = False
                        while True:
                            set_inventory_display(["med", "mr", "sr"])
                            item_using = g.choicebox("请选择你要使用的物品（只有药物）", choices=inventory_display)
                            if item_using is None:
                                quit_yn = True
                                break
                            item_using = get_key(item_using)
                            if item_using == 0:
                                g.msgbox("你想使用空气吗？")
                            else:
                                if item_property[item_using]["type"] == "med":
                                    cure_display(item_using)
                                elif item_property[item_using]["type"] == "mr":
                                    mana_display(item_using)
                                else:
                                    strength_display(item_using)
                                break
                        if quit_yn:
                            continue
                        break
    elif choose == 7:
        _update_save()
        g.msgbox("已存档")
