# version <dv-009-pv-002>
# lines: 2366 + 4 (project description: 2; start blank: 1; end blank: 1) = 2370
import base64
import collections
import os
import random
import time

import pygame.mixer

import easygui as g
import settings

inscriptions = {
    "空符文槽": {"ht": 0, "atk": 0, "atk_p": 0, "def": 0, "def_p": 0, "crit": 0, "miss": 0},
    "突刺者": {"ht": 0, "atk": 0, "atk_p": -5, "def": 0, "def_p": -5, "crit": 10, "miss": 10},
    "锐利之锋": {"ht": 0, "atk": 5, "atk_p": 8, "def": 0, "def_p": -10, "crit": 5, "miss": -5},
    "铜墙铁壁": {"ht": 0, "atk": 0, "atk_p": -8, "def": 0, "def_p": 8, "crit": -15, "miss": -30},
    "饮血之刃": {"ht": 25, "atk": 0, "atk_p": -5, "def": -5, "def_p": -30, "crit": 10, "miss": -10},
    "茹毛饮血": {"ht": 20, "atk": 0, "atk_p": -5, "def": 0, "def_p": -5, "crit": 5, "miss": -15},
    "嗜血成性": {"ht": 30, "atk": -5, "atk_p": 0, "def": -5, "def_p": -15, "crit": 0, "miss": -25},
    "嗜血如命": {"ht": 40, "atk": -5, "atk_p": -5, "def": -20, "def_p": -35, "crit": -5, "miss": -45},
    "无尽仲裁": {"ht": 0, "atk": 10, "atk_p": 1, "def": 0, "def_p": -5, "crit": 4, "miss": -5},
    "夜行者": {"ht": 0, "atk": 0, "atk_p": -5, "def": 0, "def_p": -30, "crit": 2, "miss": 35},
    "无极之刃": {"ht": 5, "atk": 5, "atk_p": 5, "def": 0, "def_p": -10, "crit": 5, "miss": -20},
    "舍命虹吸": {"ht": 65, "atk": -5, "atk_p": -20, "def": -15, "def_p": -30, "crit": -50, "miss": -40},
    "舍命之刃": {"ht": -15, "atk": 50, "atk_p": 40, "def": -45, "def_p": -40, "crit": 5, "miss": -30},
    "C.R.I.T.": {"ht": -20, "atk": -35, "atk_p": -20, "def": -10, "def_p": -25, "crit": 65, "miss": -45},
    "天降正义": {"ht": 0, "atk": 30, "atk_p": 3, "def": -25, "def_p": -10, "crit": 10, "miss": -35},
    "奥术彗星": {"ht": 0, "atk": 10, "atk_p": 1, "def": -10, "def_p": -5, "crit": 5, "miss": -25},
}
item_namespaces = {
    0: "无",

    # weapon
    10: "手", 11: "木棍", 12: "波克棒", 13: "石板波克棒", 14: "桃木剑", 15: "莫力布林棍", 16: "石板莫力布林棍", 17: "木剑",
    18: "骑士之剑", 19: "灵木剑", 110: "自然法杖I", 111: "自然法杖II", 112: "龙骨波克棒", 113: "精英骑士之剑", 114: "荣誉骑士之剑",
    115: "铂金骑士之剑", 116: "钻石骑士之剑", 117: "[UT限定][光]龙骨炮", 118: "[光]近卫骑士之剑", 119: "[流彩]荣耀骑士之剑",
    120: "[下界DLC]诡异之剑", 121: "[跨次元联动][三次元限定][传说]一口魚の兵器", 122: "[史诗]王者骑士之剑",
    123: "[跨次元联动][三次元限定][传说]青槍", 124: "[下界DLC]绯红之剑", 125: "[下界DLC]骸骨", 126: "[下界DLC][流彩]骸骨之歌",
    127: "[跨次元联动][三次元限定][传说]得力の文具",
    # armor
    21: "石板甲", 22: "士兵之甲", 23: "骑士之甲", 24: "法师长袍", 25: "[MC限定]唤魔者长袍", 26: "[流彩]荣耀骑士之甲",

    # medicine
    30: "绷带", 31: "医用绷带", 32: "小型法力回复剂", 33: "小型体力回复剂", 34: "木之灵", 35: "木之心", 36: "仙人掌果",
    37: "小型经验瓶", 38: "中型经验瓶", 39: "中型法力回复剂", 310: "中型体力回复剂",

    # mobs
    41: "波布克林", 42: "蓝色波布克林", 43: "丘丘", 44: "莫力布林", 45: "蓝色莫力布林", 46: "木系法师",

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
    523: "跳劈重击V（攻击）",
    524: "[UT限定][光]龙骨激光（攻击）",
    525: "横扫攻击IV（攻击）",
    526: "[光]近卫荣耀！（终极技能）（攻击/治疗）",
    527: "[流彩]荣耀骑士的信仰（终极技能）（攻击/回体力）",
    528: "[被动]法阵之力",
    529: "[MC限定][被动]法阵之力II",
    530: "[MC限定][被动]恼鬼攻击",
    531: "[下界DLC]怨魂斩（攻击）",
    532: "[跨次元联动][三次元限定][传说]武器を投げる（投掷武器）（攻击+/回体力-）",
    533: "[跨次元联动][三次元限定][传说]MAX·涅槃（终极技能）（回体力+/回法力+/治疗-）",
    534: "[跨次元联动][三次元限定][传说]吸う（吸噬）（攻击-/治疗++）",
    535: "[流彩]最强骑士的跳劈！（终极技能）（攻击+/治疗-）",
    536: "[流彩]最强骑士的横扫！（终极技能）（攻击-/治疗+）",
    537: "[流彩]最强骑士之魂！！（终极技能）（攻击-/治疗+/回体力）",
    538: "[跨次元联动][三次元限定][传说]ケチャップホップチョップ（番茄酱跳劈）（终极技能）（攻击/治疗-）",
    539: "[跨次元联动][三次元限定][传说]犬の頭を食べる（吃狗头）（治疗+）",
    540: "[跨次元联动][三次元限定][传说]ブルーアタック（蓝色攻击）（回体力）",
    541: "[跨次元联动][三次元限定][传说]オレンジアタック（橙色攻击）（回法力）",
    542: "[流彩][被动]荣耀骑士的力量（治疗）",
    543: "[下界DLC]炽刃斩（攻击）",
    544: "[下界DLC]骸骨斩（终极技能）（攻击/治疗-）",
    545: "[下界DLC]骸骨の歌（终极技能）（治疗+/回体力）",
    546: "[跨次元联动][三次元限定][传说]何もないから（无中生有）（终极技能）（回法力/回体力-）",
    547: "[跨次元联动][三次元限定][传说]幾何学的パズル（几何难题）（终极技能）（攻击+/治疗+）",
    548: "[跨次元联动][三次元限定][传说]文房具の実体（文具真身）（终极技能）（治疗+/回体力+）",
    549: "[跨次元联动][三次元限定][传说]得力症候群（得力综合征）（终极技能）（攻击++）（高耗蓝）",
    550: "[跨次元联动][三次元限定][传说]私の仏は思いやりがあります（我佛慈悲）（终极技能）（攻击+/回体力-/治疗-）",
    551: "[跨次元联动][三次元限定][传说]デーモンスラッシュ（魔之斩）（攻击++）（高耗蓝）",

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
    634: "铜锡合金板",
    635: "致密铜锡合金板",
    636: "基础机械外壳",
    637: "采矿机器人",
    638: "采矿机器人储存升级模块",
    639: "四级科学机器碎片",
    640: "四级科学机器",
    641: "高级电路板",
    642: "初级全合金",
    643: "初级全合金板",
    644: "致密初级全合金板",
    645: "采矿机器人升级模块",
    646: "[MC限定][史诗]龙蛋",
    647: "金粒",
    648: "金锭",
    649: "[下界DLC]末影珍珠",
    650: "[下界DLC][光]末影传送盒",
    651: "[下界DLC]菌光体",
    652: "[下界DLC]诡异木板",
    653: "严密初级全合金板",
    654: "[DLC]异世界返回传送器",
    655: "[下界DLC]绯红木板",
    656: "[下界DLC]骨头",
    657: "[下界DLC]骨块",
    658: "[下界DLC]骸骨结晶",

    # events
    70: "随机怪物",
    71: "需要帮助的神秘人",

    # boss
    80: "岩石巨人", 81: "棕色波布克林", 82: "大型守护者（陆地型）", 83: "[UT限定]Sans", 84: "[MC限定]小末影龙",
    85: "[MC限定]唤魔者", 86: "大型守护者（陆地型）+",

    # boss skill
    91: "岩石重击",
    92: "岩石炮",
    93: "能量炮",
    94: "守护者之斩",
    95: "[MC限定]飞高高",
    96: "[MC限定]龙息弹",
    97: "[MC限定][光]龙息轰炸机！",
    98: "[MC限定][光]急速飞高高",
    99: "[MC限定]尖牙突刺",
    910: "[MC限定]尖牙锁定VI",
    911: "[MC限定][光]尖牙锁定X",
    912: "[MC限定][光]恼鬼大军",
    913: "[下界DLC]骸骨斩",
    914: "交叉弹射",
    915: "镭射扫荡",
    916: "[光]光刃",
    917: "[流彩]粒子对撞",
    918: "[史诗]以守护之名",

    # dlc mobs
    101: "[下界DLC]僵尸猪灵",
    102: "[下界DLC]末影人",
    103: "[下界DLC]炼狱骷髅",
    104: "[下界DLC][BOSS]炼狱骷髅西诺克斯",
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
    18: {"atk": [10, 26], "type": "wep", "skill": [54, 59, 510], "description": "海拉鲁王国的骑士所用的单手剑", "sell": 2500,
         "craft": 1},
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
    116: {"atk": [35, 50], "type": "wep", "skill": [523, 59, 522], "description": "海拉鲁王国的钻石骑士所用的单手剑",
          "craft": 3, "sell": 22000},
    117: {"atk": [10, 20], "type": "wep", "skill": [],
          "description": "[UT限定][光]那些去挑战Sans的人们从未返乡，拿到了它的你拥有无上荣耀！"},
    118: {"atk": [40, 70], "type": "wep", "skill": [523, 525, 526], "description": "[光]海拉鲁王国的近卫骑士所用的单手剑",
          "sell": 15000, "craft": 4},
    119: {"atk": [50, 80], "type": "wep", "skill": [523, 525, 526, 527],
          "description": "[流彩]海拉鲁王国的荣耀骑士所用的单手剑", "sell": 32000, "craft": 4},
    120: {"atk": [5, 9], "type": "wep", "skill": [531], "description": "由诡异木板制成的剑，有些诡异，似乎蕴藏着怨魂的力量",
          "sell": 1500, "craft": 0},
    121: {"atk": [125, 225], "type": "wep", "skill": [523, 59, 532, 533, 534, 551],
          "description": "传说!!!\n看起来像鱼骨，又像嘴巴。。。的神秘武器", "sell": 500000},
    122: {"atk": [90, 150], "type": "wep", "skill": [523, 59, 535, 536, 537],
          "description": "史诗!\n海拉鲁王国的王者骑士所用的单手剑", "sell": 40000, "craft": 4},
    123: {"atk": [150, 250], "type": "wep", "skill": [523, 59, 538, 539, 540, 541],
          "description": "传说!!!\n一把破旧的长矛，但依旧是大犬汪最趁手的武器", "sell": 500000},
    124: {"atk": [10, 15], "type": "wep", "skill": [531], "description": "由绯红木板制成的剑，有些炽热，似乎蕴藏着火焰的力量",
          "sell": 1500, "craft": 0},
    125: {"atk": [15, 30], "type": "wep", "skill": [543], "description": "炼狱骷髅所持的武器，由骨头制成，十分骇人",
          "sell": 1500},
    126: {"atk": [25, 45], "type": "wep", "skill": [543, 544, 545],
          "description": "由骸骨结晶和骸骨制成的武器，较骸骨相比有更强的炽热之力", "sell": 25000, "craft": 0},
    127: {"atk": [125, 225], "type": "wep", "skill": [523, 59, 546, 547, 548, 549, 550],
          "description": "传说!!!\n一把破旧的长矛，但依旧是大犬汪最趁手的武器", "sell": 500000},
    # armor
    21: {"def": 100, "miss": 50, "skill": [0], "type": "arm", "sell": 80,
         "description": "蓝色波克布林所使用的防具，十分简陋，但防御有效", "craft": 0},
    22: {"def": 200, "miss": 100, "skill": [0], "type": "arm", "description": "海拉鲁王国的士兵用的防具", "sell": 3500,
         "craft": 1},
    23: {"def": 450, "miss": 70, "skill": [0], "type": "arm", "description": "海拉鲁王国的骑士所用的防具", "sell": 7200,
         "craft": 1},
    24: {"def": 50, "miss": 60, "skill": [528], "type": "arm", "description": "那些在海拉鲁大地上的法师用的防具，很轻便"
                                                                              "，但没什么防御力，似乎还有其他的用处",
         "sell": 1500},
    25: {"def": 100, "miss": 70, "skill": [529, 530], "type": "arm",
         "description": "那些在海拉鲁大地上的唤魔者用的防具，非常轻便，但没什么防御力，似乎还有其他的用处", "sell": 1500},
    26: {"def": 600, "miss": 50, "skill": [542], "type": "arm", "description": "海拉鲁王国的荣耀骑士所用的防具",
         "sell": 70000, "craft": 4},
    # medicine
    30: {"heal": 2, "type": "med", "buff": [0],
         "description": "普通的布质绷带，能包裹你的伤口", "sell": 10},
    31: {"heal": 5, "type": "med", "buff": [0],
         "description": "洒上酒精的绷带，这使它的治疗效果增加了3", "sell": 50},
    32: {"heal": 30, "type": "mr", "description": "非常普通的法力回复剂", "sell": 10},
    33: {"heal": 100, "type": "sr", "description": "非常普通的体力回复剂, 因为制作材料很常见，所以很便宜", "sell": 5},
    34: {"heal": 40, "type": "med", "buff": [0],
         "description": "帮助神秘人后神秘人回赠的礼物，是一个发光的绿色小球，似乎与桃木剑有什么关系，非常珍贵", "sell": 1000},
    35: {"heal": 120, "type": "med", "buff": [0],
         "description": "由木之灵合成的绿色小球，似乎更有生命力了，有时能感受到小球在跳动，价值连城", "sell": 4200, "craft": 0},
    36: {"heal": 7, "type": "med", "buff": [0], "description": "在沙漠能找到的果子", "sell": 60},
    37: {"heal": 25, "type": "exp", "description": "小型的经验瓶", "sell": 40},
    38: {"heal": 90, "type": "exp", "description": "中型的经验瓶", "sell": 100},
    39: {"heal": 100, "type": "mr", "description": "大一点的法力回复剂", "sell": 30},
    310: {"heal": 300, "type": "sr", "description": "大一点的体力回复剂", "sell": 10},

    # mobs
    41: {"hp": 13, "atk": [1, 2], "type": "mob",
         "description": "一个浑身通红的怪物，四肢发达，头脑简单，还特别弱",
         "miss": 0, "define": 0, "gear": [11, 12], "gold": [5, 10], "exp": 5, "skill": []},
    42: {"hp": 25, "atk": [3, 4], "type": "mob",
         "description": "波布克林的一级加强版，聪明了些，武器也更加精良，甚至还有盔甲",
         "miss": 2, "define": 10, "gear": [13, 21], "gold": [18, 30], "exp": 12, "skill": [56]},
    43: {"hp": 5, "atk": [0, 1], "type": "mob",
         "description": "一个极弱的怪物，甚至有可能打出0点伤害...",
         "miss": 0, "define": 0, "gear": [11], "gold": [3, 7], "exp": 3, "skill": []},
    44: {"hp": 70, "atk": [5, 10], "type": "mob",
         "description": "波克布林的亲戚，更加强壮了，因此攻击力增强",
         "miss": 0, "define": 15, "gear": [15], "gold": [40, 85], "exp": 40, "skill": [51, 58]},
    45: {"hp": 180, "atk": [10, 20], "type": "mob",
         "description": "莫力布林的一级加强版，武器更加精良，因为体型太大没有适合的盔甲",
         "miss": 1, "define": 18, "gear": [16], "gold": [90, 155], "exp": 100, "skill": [54, 55]},
    46: {"hp": 25, "atk": [15, 30], "type": "mob", "miss": 10, "define": 35, "gold": [50, 100], "exp": 70,
         "gear": [110, 24], "description": "普通的法师，拥有着木系的能力", "skill": [515, 516]},

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
    523: {"final": False, "type": "a", "atk": 75, "cost_mana": 60},
    524: {"final": False, "type": "a", "atk": 35, "cost_mana": 5},
    525: {"final": False, "type": "a", "atk": 40, "cost_mana": 30},
    526: {"final": True, "type": "a;c", "atk": 65, "heal": 55, "cost_mana": 130},
    527: {"final": True, "type": "a;s", "atk": 90, "heal_s": 280, "cost_mana": 160},
    528: {"type": "cm", "heal": 10},
    529: {"type": "cm", "heal": 15},
    530: {"type": "ca", "atk": 5},
    531: {"final": False, "type": "a", "atk": 40, "cost_mana": 25},
    532: {"final": True, "type": "a;s", "atk": 950, "heal_s": 450, "cost_mana": 1200},
    533: {"final": True, "type": "c;s;m", "heal_s": 200, "heal_m": 50, "heal": 20, "cost_mana": 0},
    534: {"final": True, "type": "a;c", "atk": 500, "heal": 1000, "cost_mana": 1100},
    535: {"final": True, "type": "a;c", "atk": 500, "heal": 100, "cost_mana": 600},
    536: {"final": True, "type": "a;c", "atk": 300, "heal": 200, "cost_mana": 700},
    537: {"final": True, "type": "a;c;s", "atk": 200, "heal": 150, "heal_s": 200, "cost_mana": 950},
    538: {"final": True, "type": "a;c", "atk": 1000, "heal": 400, "cost_mana": 1600},
    539: {"final": False, "type": "c", "heal": 600, "cost_mana": 800},
    540: {"final": False, "type": "s", "heal": 1000, "cost_mana": 400},
    541: {"final": False, "type": "m", "heal": 50, "cost_mana": 0},
    542: {"type": "cc", "heal": 20},
    543: {"final": False, "type": "a", "atk": 60, "cost_mana": 35},
    544: {"final": True, "type": "a;c", "atk": 120, "heal": 35, "cost_mana": 160},
    545: {"final": True, "type": "c;s", "heal": 70, "heal_s": 150, "cost_mana": 150},
    546: {"final": True, "type": "m;s", "heal_m": 20, "heal_s": 10, "cost_mana": 0},
    547: {"final": True, "type": "a;c", "heal": 100, "atk": 1000, "cost_mana": 1200},
    548: {"final": True, "type": "c;s", "heal": 300, "heal_s": "all", "cost_mana": 700},
    549: {"final": False, "type": "c;s", "atk": 2222, "cost_mana": 1900},
    550: {"final": True, "type": "a;c;s", "atk": 1000, "heal": 300, "heal_s": 10, "cost_mana": 1400},
    551: {"final": False, "type": "a", "atk": 2333, "cost_mana": 2000},

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
    636: {"type": "m", "description": "基础机械的铁质外壳，可以适用于大多数机器", "sell": 2000, "craft": 2},
    637: {"type": "m", "craft": 3},
    638: {"type": "m", "description": "可以将采矿机器人的储存上限提升2000的模块", "sell": 5000, "craft": 3},
    639: {"type": "m", "description": "四级科学机器的碎片", "sell": 1500},
    640: {"type": "m", "craft": 3},
    641: {"type": "m", "description": "高级的电路板，极大的运算量", "craft": 3, "sell": 10000},
    642: {"type": "m", "description": "由铜，铁，锡三种金属制成的合金", "craft": 4, "sell": 3000},
    643: {"type": "m", "description": "被压制成板的初级全合金", "craft": 4, "sell": 7000},
    644: {"type": "m", "description": "二重压缩的初级全合金", "craft": 4, "sell": 15000},
    645: {"type": "m", "description": "提升采矿机器人等级的工具，等级提升可以让挖矿机器人挖矿机器人每次采矿的时间缩短", "craft": 3,
          "sell": 6000},
    646: {"type": "m", "description": "[MC限定][史诗]打败末影龙获得的东西，价值连城", "sell": 50000},
    647: {"type": "m", "description": "一小块金", "sell": 2000},
    648: {"type": "m", "description": "标准大小的金", "sell": 20000},
    649: {"type": "m", "description": "击败末影人后的战利品，使用后可以快速前进1km", "sell": 5000},
    650: {"type": "m", "description": "一次性的传送用具，使用后可以传送到当前维度的任意地区", "sell": 35000},
    651: {"type": "m", "description": "一种存于下界的真菌，会发光", "sell": 1000},
    652: {"type": "m", "description": "由一种存于下界的大型青蓝色真菌的茎制成的类似于木板的物品", "sell": 500},
    653: {"type": "m", "description": "三重压缩的初级全合金", "sell": 35000, "craft": 4},
    654: {"type": "m", "description": "用于从DLC的维度返回主世界的传送器", "sell": 500},
    655: {"type": "m", "description": "由一种存于下界的大型绯红色真菌的茎制成的类似于木板的物品", "sell": 500},
    656: {"type": "m", "description": "一块骨头，上面有一些血迹", "sell": 50},
    657: {"type": "m", "description": "大密度的骨粉", "sell": 500},
    658: {"type": "m", "description": "炼狱骷髅西诺克斯的结晶，价值连城", "sell": 20000},

    # events
    70: {"type": "e", "*description": "summon a random mob"},
    71: {"type": "e", "*description": "a mystery man that need gold to help"},

    # boss
    80: {"type": "boss", "hp": 50, "atk": [5, 10], "skill": [50, 91, 92], "gear": [66, 66, 66, 68, 68],
         "gold": [80, 210], "exp": 90, "define": 20, "miss": 0, "description": "浑身是岩石的大块头"},
    81: {"type": "boss", "hp": 260, "atk": [25, 35], "skill": [520, 55], "gear": [21, 112], "gold": [300, 630],
         "exp": 210, "define": 10, "miss": 10, "description": "波布克林的二级加强版，超强"},
    82: {"type": "boss", "hp": 1500, "atk": [10, 12], "skill": [93, 94], "gear": [69, 69, 618, 618, 620, 620, 628,
                                                                                  635, 635],
         "gold": [3000, 6000], "exp": 2000, "define": 30, "miss": 20,
         "description": "古代希卡族为对抗灾厄盖侬而打造出的机械自动兵器，但现在被灾厄盖侬的怨念夺走"},
    83: {"type": "boss", "hp": 1, "atk": [1, 5], "skill": [], "gear": [83], "gold": [210, 500], "exp": 999,
         "define": 0, "miss": 99.99, "description": "最弱的Boss，他不可能一直躲下去"},
    84: {"type": "boss", "hp": 200, "atk": [1, 3], "skill": [95, 96, 97, 98], "gear": [646], "gold": [100, 120],
         "exp": 150, "define": 35, "miss": 42.01, "description": "盘踞于末路之地的龙的孩子，也守护着她宝贵的龙蛋"},
    85: {"type": "boss", "hp": 60, "atk": [5, 10], "skill": [99, 910, 911, 912], "gear": [25], "gold": [40, 70],
         "exp": 240, "define": 50, "miss": 15, "description": "法师的头子，比较强大"},
    86: {"type": "boss", "hp": 2500, "atk": [10, 18], "skill": [914, 915, 916, 917, 918],
         "gear": [639, 639, 641, 641, 642, 643, 643, 643, 643, 643],
         "gold": [8000, 15000], "exp": 5000, "define": 50, "miss": 30,
         "description": " 古代希卡族为了对抗灾厄盖侬而打造出的机械自动兵器，这种守护者拥有更强的武器及设备，可以在对抗中起到关键作用，"
                        "但现在被灾厄盖侬的怨念夺走"},

    # boss skill
    91: {"type": "a", "atk": 28},
    92: {"type": "a", "atk": 32},
    93: {"type": "a", "atk": 50},
    94: {"type": "a", "atk": 48},
    95: {"type": "a", "atk": 24},
    96: {"type": "a", "atk": 8},
    97: {"type": "a", "atk": 55},
    98: {"type": "a", "atk": 30},
    99: {"type": "a", "atk": 20},
    910: {"type": "a", "atk": 50},
    911: {"type": "a", "atk": 90},
    912: {"type": "a", "atk": 70},
    913: {"type": "a", "atk": 80},
    914: {"type": "a", "atk": 75},
    915: {"type": "a", "atk": 90},
    916: {"type": "a", "atk": 120},
    917: {"type": "a", "atk": 145},
    918: {"type": "a", "atk": 165},

    # dlc mob
    101: {"type": "dlcnm", "hp": 45, "atk": [10, 15], "miss": 5, "define": 65, "gold": [145, 235], "exp": 90,
          "gear": [647, 647, 647, 647, 648], "skill": [54], "description": "下界中最常见的怪物，可以从它身上获取金"},
    102: {"type": "dlcnm", "hp": 100, "atk": [5, 10], "miss": 65, "define": 0, "gold": [55, 120], "exp": 180,
          "gear": [649], "skill": [58], "description": "神奇的瘦长怪物，可以通过操作末影珍珠瞬移，家乡是末路之地"},
    103: {"type": "dlcnm", "hp": 60, "atk": [10, 15], "gear": [656, 657], "gold": [20, 50], "exp": 120,
          "skill": [55, 59], "miss": 0, "define": 10, "description": "来自下界的骷髅，浑身炙热"},
    104: {"type": "dlcnb", "hp": 360, "atk": [10, 20], "gear": [658], "gold": [340, 560], "exp": 340,
          "skill": [913], "miss": 0, "define": 50, "description": "炼狱中的的骷髅西诺克斯，骸骨之歌是其武器"},

    0: {"def": 0, "miss": 0, "skill": [], "type": ""},
}
player_property = {"lv": 1, "hp": 20, "max_hp": 20, "gold": 20, "miss": 5, "define": 0, "exp": 0, "km": 0.0, "place": 1,
                   "need exp": 10, "mana": 30, "max_mana": 30, "mana_reg": 1, "str": 50, "max_str": 50, "str_reg": 3,
                   "sm1": False, "sm2": False, "sm3": False, "sm4": False, "miner_tier": 1,
                   "miner": False, "miner_max": 1000, "last_login": None, "base_atk": 0, "cheating": False,
                   "nether_dlc": False, "nether": False, "inscription_buff":
                       {"ht": 0, "atk": 0, "atk_p": 0, "def": 0, "def_p": 0, "crit": 0, "miss": 0},
                   "inscriptions": ["空符文槽", "空符文槽"], "inscription_num": 2}

craft_expr = {
    "一级科学机器碎片 * 4 + 生铁 * 2 -> 一级科学机器": "4 * 615; 2 * 69 -> 621",
    "二级科学机器碎片 * 10 + 电路板（需要一级科学机器）-> 二级科学机器": "10 * 616; 1 * 623 -> 622",
    "三级科学机器碎片 * 15 + 中级电路板 -> 三级科学机器": "15 * 631; 1 * 630 -> 632",
    "四级科学机器碎片 * 5 + 高级电路板 -> 四级科学机器": "5 * 639; 1 * 641 -> 640",
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
    "[下界DLC]骸骨 + [下界DLC]骸骨结晶 -> [下界DLC]骸骨之歌": "1 * 125; 1 * 658 -> 126",
    "====================一级科学机器====================": None,  # craft: 1
    "铁矿 * 2 -> 生铁": "2 * 68 -> 69",
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
    "铁板 * 4 -> 基础机械外壳": "4 * 611 -> 636",
    "====================三级科学机器====================": None,  # craft: 3
    "生铜 * 3 + 生锡 * 3 -> 铜锡合金": "3 * 618; 3 * 625 -> 633", "铜锡合金 * 3 -> 铜锡合金板": "3 * 633 -> 634",
    "铜锡合金板 * 3 -> 致密铜锡合金板": "3 * 634 -> 635", "铜锡合金板 * 4 + 铁柄 -> 铂金骑士之剑": "4 * 634; 1 * 613 -> 115",
    "致密铜锡合金板 * 4 + 铁柄 -> 钻石骑士之剑": "4 * 635; 1 * 613 -> 116",
    "基础机械外壳 * 2 + 中级电路板 + 电路板 + 锡线 * 4 -> 采矿机器人": "2 * 636; 1 * 630; 1 * 623; 4 * 626 -> 637",
    "电路板 + 铁板 * 4 -> 采矿机器人储存升级模块": "1 * 623; 4 * 611 -> 638",
    "铜锡合金板 + 锡线 * 3 -> 高级电路板": "1 * 634; 3 * 626 -> 641",
    "电路板 + 铜线 * 3 + 锡线 * 1 -> 采矿机器人升级模块": "1 * 623; 3 * 620; 1 * 626 -> 645",
    "[下界DLC]末影珍珠 * 4 + 铜锡合金板 * 4 -> [下界DLC]末影传送盒": "4 * 649; 4 * 634 -> 650",
    "====================四级科学机器====================": None,  # craft: 4
    "生铁 * 3 + 生铜 * 2 + 生锡 -> 初级全合金": "3 * 69; 2 * 618; 1 * 625 -> 642",
    "初级全合金 * 2 -> 初级全合金板": "2 * 642 -> 643", "初级全合金板 * 2 -> 致密初级全合金板": "2 * 643 -> 644",
    "致密初级全合金板 * 2 -> 严密初级全合金板": "2 * 644 -> 653",
    "初级全合金板 * 7 + 生铁 * 5 -> [流彩]荣耀骑士之甲": "7 * 643; 5 * 69 -> 26",
    "初级全合金板 + 铁柄 -> [光]近卫骑士之剑": "1 * 643; 1 * 613 -> 118",
    "致密初级全合金板 + 铁柄 -> [流彩]荣耀骑士之剑": "1 * 644; 1 * 613 -> 119",
    "严密初级全合金板 + 铁柄 -> [史诗]王者骑士之剑": "1 * 653; 1 * 613 -> 122",
}

inventory_display = []

mobs = []

bosses = []

places = {1: "海拉鲁台地", 2: "海拉鲁山脉", 3: "哈特尔平原", 4: "南哈特诺山脉",
          5: "西哈特诺高原", 6: "中哈特诺盆地", 7: "东哈特尔雪山", 8: "南哈特尔山脉",
          9: "雷之台地", 10: "漂流物岬角", 11: "南海拉鲁平原", 12: "东努克尔沙漠",
          13: "中努克尔沙漠", 14: "北努克尔沙漠", 15: "南哈尔里丛林", 16: "哈尔里丛林深部", 17: "咕隆地区", 18: "死亡火山脚",
          19: "死亡火山腰", 20: "死亡火山口", 80: "下界传送门"}
nether_places = {1: "下界荒漠", 2: "诡异森林", 3: "绯红森林", 4: "灵魂沙峡谷"}

explore_list = []
nether_explore_list = []

place_display = []
for i in places.keys():
    place_display.append(places[i])

nether_place_display = []
for i in nether_places.keys():
    nether_place_display.append(nether_places[i])

breaking = False


# classes
class Mob:
    def __init__(self, namespace, max_hp, atk, description, miss, define, gear, gold, exp, skill):
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
        if skill is []:
            self.skill = [50]
        else:
            self.skill = skill


class Boss:
    def __init__(self, namespace, hp, skill, gear, gold, exp, atk, miss, define, description):
        self.namespace = namespace
        self.max_hp = hp
        self.hp = hp
        self.skill = skill
        self.skill.append(50)
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


def add_nether_explore(item, p, place):
    for t in range(p):
        nether_explore_list[place - 1].append(item)


def inscription_buff_set():
    player_property["inscription_buff"] = {"ht": 0, "atk": 0, "atk_p": 0, "def": 0, "def_p": 0, "crit": 0, "miss": 0}
    for inscription in player_property["inscriptions"]:
        for buff in inscriptions[inscription].keys():
            player_property["inscription_buff"][buff] += inscriptions[inscription][buff]


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


def mana_display(item_checking, skill=False):
    """
    a function using at display
    """
    if skill:
        if "cm" not in item_property[item_checking]["type"]:
            if item_property[item_checking]["final"]:
                if item_property[item_checking]["heal_m"] == "all":
                    player_property["mana"] = player_property["max_mana"]
                    g.msgbox("你的法力回满了！")
                else:
                    player_property["mana"] += item_property[item_checking]["heal_m"]
                    g.msgbox("你回复了" + str(item_property[item_checking]["heal_m"]) + "点法力")
                    if player_property["mana"] > player_property["max_mana"]:
                        g.msgbox(f"你的法力溢出了\n可惜的是，{item_namespaces[item_checking]}似乎"
                                 "不会帮你保存溢出的法力")
                        player_property["mana"] = player_property["max_mana"]
                    elif player_property["mana"] == player_property["max_mana"]:
                        g.msgbox("你的法力满了")
            else:
                if item_property[item_checking]["heal"] == "all":
                    player_property["mana"] = player_property["max_mana"]
                    g.msgbox("你的法力回满了！")
                else:
                    player_property["mana"] += item_property[item_checking]["heal"]
                    g.msgbox("你回复了" + str(item_property[item_checking]["heal"]) + "点法力")
                    if player_property["mana"] > player_property["max_mana"]:
                        g.msgbox(f"你的法力溢出了\n可惜的是，{item_namespaces[item_checking]}似乎"
                                 "不会帮你保存溢出的法力")
                        player_property["mana"] = player_property["max_mana"]
                    elif player_property["mana"] == player_property["max_mana"]:
                        g.msgbox("你的法力满了")
        else:
            if item_property[item_checking]["heal"] == "all":
                player_property["mana"] = player_property["max_mana"]
                g.msgbox("你的法力回满了！")
            else:
                player_property["mana"] += item_property[item_checking]["heal"]
                g.msgbox("你回复了" + str(item_property[item_checking]["heal"]) + "点法力")
                if player_property["mana"] > player_property["max_mana"]:
                    g.msgbox(f"你的法力溢出了\n可惜的是，{item_namespaces[item_checking]}似乎"
                             "不会帮你保存溢出的法力")
                    player_property["mana"] = player_property["max_mana"]
                elif player_property["mana"] == player_property["max_mana"]:
                    g.msgbox("你的法力满了")

    else:
        if item_property[item_checking]["heal"] == "all":
            player_property["mana"] = player_property["max_mana"]
            g.msgbox("你的法力回满了！")
        else:
            player_property["mana"] += item_property[item_checking]["heal"]
            g.msgbox("你回复了" + str(item_property[item_checking]["heal"]) + "点法力")
            if player_property["mana"] > player_property["max_mana"]:
                g.msgbox(f"你的法力溢出了\n可惜的是，{item_namespaces[item_checking]}似乎"
                         "不会帮你保存溢出的法力")
                player_property["mana"] = player_property["max_mana"]
            elif player_property["mana"] == player_property["max_mana"]:
                g.msgbox("你的法   力满了")
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


def strength_display(item_checking, skill=False):
    if skill:
        if "cs" not in item_property[item_checking]["type"]:
            if item_property[item_checking]["final"]:
                if item_property[item_checking]["heal_s"] == "all":
                    player_property["str"] = player_property["str"]
                    g.msgbox("你的体力回满了！")
                else:
                    player_property["str"] += item_property[item_checking]["heal_s"]
                    g.msgbox("你回复了" + str(item_property[item_checking]["heal_s"]) + "点体力")
                    if player_property["str"] > player_property["max_str"]:
                        g.msgbox(f"你的体力溢出了\n可惜的是，{item_namespaces[item_checking]}似乎"
                                 "不会帮你保存溢出的体力")
                        player_property["str"] = player_property["max_str"]
                    elif player_property["str"] == player_property["max_str"]:
                        g.msgbox("你的体力满了")
            else:
                if item_property[item_checking]["heal"] == "all":
                    player_property["str"] = player_property["str"]
                    g.msgbox("你的体力回满了！")
                else:
                    player_property["str"] += item_property[item_checking]["heal"]
                    g.msgbox("你回复了" + str(item_property[item_checking]["heal"]) + "点体力")
                    if player_property["str"] > player_property["max_str"]:
                        g.msgbox(f"你的体力溢出了\n可惜的是，{item_namespaces[item_checking]}似乎"
                                 "不会帮你保存溢出的体力")
                        player_property["str"] = player_property["max_str"]
                    elif player_property["str"] == player_property["max_str"]:
                        g.msgbox("你的体力满了")
        else:
            if item_property[item_checking]["heal"] == "all":
                player_property["str"] = player_property["str"]
                g.msgbox("你的体力回满了！")
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
    else:
        if item_property[item_checking]["heal"] == "all":
            player_property["str"] = player_property["str"]
            g.msgbox("你的体力回满了！")
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


def fight_ui(dlc=None):
    def attack_response():
        if random.randint(1, 100) < mob.miss:
            g.msgbox(f"{item_namespaces[mob.namespace]}似乎躲开了这次攻击")
        else:
            damage_current_value = item_property[skill_num]["atk"]
            crit_damage = 1
            if random.randint(1, 100) <= player_property["inscription_buff"]["crit"]:
                crit_damage = 1.75
                g.msgbox("暴击！")
            damage = int((damage_current_value +
                          player_property["inscription_buff"]["atk"]) *
                         (1 + 0.01 * player_property["inscription_buff"]["atk_p"]) * (1 - mob.define * 0.01) *
                         crit_damage) + player_property["base_atk"]
            mob.hp -= damage
            g.msgbox(f"你对{item_namespaces[mob.namespace]}造成了{damage}点伤害")
            hp_take = int(damage * player_property["inscription_buff"]["ht"] * 0.01)
            player_property["hp"] += hp_take
            if hp_take != 0:
                if hp_take > 0:
                    g.msgbox(f"你吸取了{hp_take}点HP")
                else:
                    g.msgbox(f"你被反噬了{hp_take}点HP")
            if player_property["hp"] > player_property["max_hp"]:
                player_property["hp"] = player_property["max_hp"]
                g.msgbox("你的HP溢出了，可惜你无法保存溢出的HP")
    if dlc is None:
        mob_object = item_property[random.choice(mobs)]
    else:
        mob_object = item_property[random.choice(dlc_mobs["nether"])]
    mob = Mob(get_key(mob_object, item_property), mob_object["hp"],
              mob_object["atk"], mob_object["description"], mob_object["miss"], mob_object["define"],
              mob_object["gear"], mob_object["gold"], mob_object["exp"], mob_object["skill"])
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
                if random.randint(1, 10000) < mob.miss * 100:
                    g.msgbox(f"{item_namespaces[mob.namespace]}似乎躲开了这次攻击")
                else:
                    if item_property[pocket["equip"]["weapon"]]["atk"][0] != \
                            item_property[pocket["equip"]["weapon"]]["atk"][1]:
                        damage_current_value = random.randint(
                            item_property[pocket["equip"]["weapon"]]["atk"][0],
                            item_property[pocket["equip"]["weapon"]]["atk"][1])
                    else:
                        damage_current_value = item_property[pocket["equip"]["weapon"]]["atk"][0]
                    crit_damage = 1
                    if random.randint(1, 100) <= player_property["inscription_buff"]["crit"]:
                        crit_damage = 1.75
                        g.msgbox("暴击！")
                    damage = int((damage_current_value +
                                  player_property["inscription_buff"]["atk"]) *
                                 (1 + 0.01 * player_property["inscription_buff"]["atk_p"]) * (1 - mob.define * 0.01) *
                                 crit_damage) + player_property["base_atk"]
                    mob.hp -= damage
                    g.msgbox(f"你对{item_namespaces[mob.namespace]}造成了{damage}点伤害")
                    hp_take = int(damage * player_property["inscription_buff"]["ht"] * 0.01)
                    player_property["hp"] += hp_take
                    if hp_take != 0:
                        if hp_take > 0:
                            g.msgbox(f"你吸取了{hp_take}点HP")
                        else:
                            g.msgbox(f"你被反噬了{hp_take}点HP")
                    if player_property["hp"] > player_property["max_hp"]:
                        player_property["hp"] = player_property["max_hp"]
                        g.msgbox("你的HP溢出了，可惜你无法保存溢出的HP")
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
                                cure_display(skill_num, True)
                            elif skill_type == "m":
                                mana_display(skill_num, True)
                            else:
                                strength_display(skill_num, True)

                    else:
                        if item_property[skill_num]["type"] == "a":
                            attack_response()
                        elif item_property[skill_num]["type"] == "c":
                            cure_display(skill_num, True)
                        elif item_property[skill_num]["type"] == "m":
                            mana_display(skill_num, True)
                        else:
                            strength_display(skill_num, True)
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
                item_property[pocket["equip"]["armor"]]["miss"] * 0.01 + \
                player_property["inscription_buff"]["miss"] * 0.01:
            g.msgbox(f"你似乎躲开了这次攻击")
        else:
            damage = int(random.randint(mob.atk[0], mob.atk[1]) *
                         (1 - ((player_property["define"] + item_property[pocket["equip"]["armor"]]["def"] +
                                player_property["inscription_buff"]["def"]) * 0.0001 +
                               player_property["inscription_buff"]["def_p"] * 0.01)))
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
        for sk in item_property[pocket["equip"]["armor"]]["skill"]:
            if sk != 0:
                g.msgbox(f"{player}使出了{item_namespaces[sk]}!")
                if item_property[sk]["type"] == "cm":
                    mana_display(sk, True)
                elif item_property[sk]["type"] == "ca":
                    if random.randint(1, 10000) < mob.miss * 100:
                        g.msgbox(f"{item_namespaces[mob.namespace]}似乎躲开了这次攻击")
                    else:
                        damage_current_value = item_property[sk]["atk"]
                        damage = int((damage_current_value +
                                      player_property["inscription_buff"]["atk"]) *
                                     (1 + 0.01 * player_property["inscription_buff"]["atk_p"]) * (
                                             1 - mob.define * 0.01)) \
                                 + player_property["base_atk"]
                        mob.hp -= damage
                        g.msgbox(f"你对{item_namespaces[mob.namespace]}造成了{damage}点伤害")
                        hp_take = int(damage * player_property["inscription_buff"]["ht"] * 0.01)
                        player_property["hp"] += hp_take
                        if hp_take != 0:
                            if hp_take > 0:
                                g.msgbox(f"你吸取了{hp_take}点HP")
                            else:
                                g.msgbox(f"你被反噬了{hp_take}点HP")
                        if player_property["hp"] > player_property["max_hp"]:
                            player_property["hp"] = player_property["max_hp"]
                            g.msgbox("你的HP溢出了，可惜你无法保存溢出的HP")
                elif item_property[sk]["type"] == "cc":
                    cure_display(sk, True)
    check_level()


def range_avg():
    return int((item_property[pocket["equip"]["weapon"]]["atk"][0] + item_property[pocket["equip"]["weapon"]]["atk"][1])
               / 2)


def check_level():
    global player_property
    if player_property["exp"] >= player_property["need exp"]:
        while player_property["exp"] >= player_property["need exp"]:
            player_property["lv"] += 1
            player_property["exp"] = player_property["exp"] - player_property["need exp"]
            player_property["need exp"] = player_property["lv"] * (10 + player_property["lv"]) + player_property[
                "lv"] - 1
            player_property["max_hp"] = player_property["lv"] * 10 + int(player_property["lv"] * 2 - 1)
            player_property["hp"] = player_property["max_hp"]
            player_property["max_mana"] = player_property["lv"] * 10 + 20
            player_property["mana"] = player_property["max_mana"]
            player_property["mana_reg"] = int(player_property["lv"] / 5) + 1
            player_property["str"] = player_property["lv"] * 35 + 15
            player_property["max_str"] = player_property["str"]
            player_property["str_reg"] = int(player_property["lv"] * 0.1) + 1
            player_property["base_atk"] = int(player_property["lv"] * 0.1)
            player_property["inscription_num"] = int(player_property["lv"] * 0.1) + 2
            if player_property["inscription_num"] > 11:
                player_property["inscription_num"] = 11
            while len(player_property["inscriptions"]) < player_property["inscription_num"]:
                player_property["inscriptions"].append("空符文槽")
        g.msgbox(f"你升级了！\n你目前的LV为{player_property['lv']}\n"
                 f"你的HP上限变为了{player_property['max_hp']}\n你的HP回满了\n你的法力上限变为了{player_property['max_mana']}"
                 f"\n你的法力回满了\n你的体力上限变为了{player_property['max_str']}\n你的体力回满了\n"
                 f"你的基础ATK现在为{player_property['base_atk']}\n你的符文槽个数现在为{player_property['inscription_num']}")


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


# technical functions
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


def inventory_sort(inventory: list):
    for i in range(1, len(inventory)):
        if str(inventory[i]) < str(inventory[i - 1]):
            inventory[i], inventory[i - 1] = inventory[i - 1], inventory[i]
    return inventory


pygame.mixer.init()
pygame.mixer_music.load("bgm.mp3")
pygame.mixer_music.play(-1)

for i in range(20):
    explore_list.append([])
for i in range(5):
    nether_explore_list.append([])
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
add_explore(70, 10, 16)
add_explore(65, 25, 16)
add_explore(67, 30, 16)
add_explore(71, 30, 16)
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

# nether
# place 1
add_nether_explore(647, 5, 1)
add_nether_explore(70, 95, 1)

# place 2
add_nether_explore(651, 15, 2)
add_nether_explore(652, 30, 2)
add_nether_explore(70, 55, 2)

# place 3
add_nether_explore(651, 25, 3)
add_nether_explore(655, 5, 3)
add_nether_explore(70, 70, 3)

# place 4
add_nether_explore(656, 5, 4)
add_nether_explore(657, 20, 4)
add_nether_explore(70, 75, 4)

run_environment = _get_path()
_makedir("save")
_option_go("save")
saves = os.listdir()
g.msgbox("""
                                  fight dv-009
                                      欢迎
""")
_back()
mod_list = os.listdir()
index = 0
while index < len(mod_list):
    if mod_list[index].split(".")[-1] != "py" or mod_list[index].split("_")[-1] != "mod.py":
        mod_list.remove(mod_list[index])
        continue
    mod = mod_list[index].replace(".py", "")
    mod_list[index] = mod
    index += 1
print(f"[{time.strftime('%H:%M:%S', time.localtime())}][INFO]start mod preload")
mod_objects = []
mod_gui = False
mod_gui_count = 0
mod_display = []
dlc_mobs = {"nether": []}
for mod_name in mod_list:
    exec(f"""
import {mod_name}
mod_class_name = {mod_name}.class_name
exec(f"mod_object = {{mod_name}}.{{mod_class_name}}()")
mod_objects.append(mod_object)
if mod_objects[-1].GUI:
    mod_gui = True
    mod_gui_count += 1
if mod_objects[-1].LOAD_GUI:
    mod_objects[-1].load(item_property=item_property, item_namespaces=item_namespaces)
if mod_objects[-1].PRELOAD_ITEM:
    for i in mod_objects[-1].ITEMS.keys():
        item_namespaces[mod_objects[-1].ITEM_PREFIX + i] = mod_objects[-1].ITEMS[i]
        item_property[mod_objects[-1].ITEM_PREFIX + i] = mod_objects[-1].ITEMS_PROPERTY[i]
    """)
    mod_display.append(mod_name.replace("_mod", "", 1))
print(f"[{time.strftime('%H:%M:%S', time.localtime())}][INFO]mod preload finished")
_option_go("save")
if len(mod_list) != 0:
    if g.ccbox(f"已加载{len(mod_list)}个模组 是否查看模组列表？", choices=["是的", "不了"]):
        while len(mod_display) < 2:
            mod_display.append("无")
        g.choicebox("按任意键退出", choices=mod_display)
saves.append("创建新存档")
while len(saves) < 2:
    saves.append("无")
while True:
    save = g.choicebox("请选择存档", choices=saves)
    if save is None:
        exit()
    elif save == "无":
        continue
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
                    if player == "EM":
                        g.msgbox("你获得了开发者的眷顾")
                        player_property["gold"] = 10000
                    elif player == "PM":
                        g.msgbox("你获得了开发者的眷顾II")
                        player_property["gold"] = 99999
                        pocket["inventory"].append(119)
                    _update_save()
                    breaking = True
                    break
                else:
                    continue
            else:
                _makefile(player)
                if player == "EM":
                    g.msgbox("你获得了开发者的眷顾")
                    player_property["gold"] = 10000
                # There is no "egg" XD
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
            # Check the items in the unloaded mods in the save
            delete_item = False
            mod_item_not_loaded = False
            for item in pocket["inventory"]:
                if type(item) == str:
                    if item not in item_namespaces.keys():
                        mod_item_not_loaded = True
                        if delete_item:
                            pocket["inventory"].remove(item)
                        else:
                            if g.ccbox("这里有一些未被识别的物品在你的存档里（可能是未加载的模组里的物品），你想要删除他们吗？",
                                       choices=["是", "否"]):
                                delete_item = True
                                pocket["inventory"].remove(item)
                            else:
                                break
            if not delete_item and mod_item_not_loaded:
                continue
            if type(pocket["equip"]["weapon"]) == str:
                if item not in item_namespaces.keys():
                    if delete_item:
                        pocket["inventory"].remove(item)
                    else:
                        if g.ccbox("这里有一些未被识别的物品在你的存档里（可能是未加载的模组里的物品），你想要删除他们吗？",
                                   choices=["是", "否"]):
                            delete_item = True
                            pocket["inventory"].remove(item)
                        else:
                            break
            if not delete_item and mod_item_not_loaded:
                continue
            if type(pocket["equip"]["armor"]) == str:
                if item not in item_namespaces.keys():
                    if delete_item:
                        pocket["inventory"].remove(item)
                    else:
                        if g.ccbox("这里有一些未被识别的物品在你的存档里（可能是未加载的模组里的物品），你想要删除他们吗？",
                                   choices=["是", "否"]):
                            delete_item = True
                            pocket["inventory"].remove(item)
                        else:
                            break
            if not delete_item and mod_item_not_loaded:
                continue
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

# get dlc mob list
for i in item_property.keys():
    if "dlc" in item_property[i]["type"] and "m" in item_property[i]["type"]:
        if "n" in item_property[i]["type"]:
            dlc_mobs["nether"].append(i)

if player_property["miner"]:
    get_gold = int((time.time() - player_property["last_login"]) / (3600 / player_property["miner_tier"])) * 5
    if get_gold > player_property["miner_max"]:
        get_gold = player_property["miner_max"]
    player_property["gold"] += get_gold
    g.msgbox(f"在你离开的这段时间里，采矿机器人为你收集了{get_gold}$")
player_property["last_login"] = time.time()
while True:
    inscription_buff_set()
    check_level()
    pocket["inventory"] = inventory_sort(pocket["inventory"])
    main_choices = ["状态", "背包", "探索", "商店", "贤者", "与普通怪物战斗", "与Boss级怪物战斗", "符文配置",
                    "存档", "更换存档", "DLC兑换"]
    mod_keys = {}
    if mod_gui:
        for mod in mod_objects:
            if mod.GUI:
                main_choices.append(mod.name)
                mod_keys[len(main_choices) - 1] = mod_objects.index(mod)
    choose = g.indexbox(f"你好，{player}！\n", choices=main_choices)
    if choose is None:
        if g.ccbox("你确定要退出存档吗（若要更换存档，可在主界面的更换存档处操作）", choices=["是的", "不了"]):
            g.msgbox("再见")
            exit()

    # status UI
    elif choose == 0:
        if g.ccbox(f"""
{player}
作弊: {player_property["cheating"]}
LV: {player_property["lv"]}
EXP: {player_property["exp"]}/{player_property["need exp"]}
HP: {player_property["hp"]}/{player_property["max_hp"]}
基础ATK: {player_property["base_atk"]}
体力: {player_property["str"]}/{player_property["max_str"]}
体力回复: {player_property["str_reg"]}
法力: {player_property["mana"]}/{player_property["max_mana"]}
法力回复: {player_property["mana_reg"]}
现金: {player_property["gold"]}$
武器：{item_namespaces[pocket["equip"]["weapon"]]}  ATK {item_property[pocket["equip"]["weapon"]]["atk"][0]} ~ {item_property[pocket["equip"]["weapon"]]["atk"][1]} 
盔甲：{item_namespaces[pocket["equip"]["armor"]]}  DEF {item_property[pocket["equip"]["armor"]]["def"]}
        """, choices=["更换角色名字", "OK"]):
            while True:
                new_player = g.enterbox("请输入玩家的名字")
                if new_player == "":
                    continue
                elif new_player is None:
                    break
                elif new_player in saves:
                    if g.ccbox(f"\"{player}\"是一个已经被用过的名字，是否要覆盖原存档（请经过存档主人同意后操作）",
                               choices=["是的", "不了"]):
                        pass
                else:
                    os.rename(player, new_player)
                    player = new_player
                    break
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
                    if player_property["miner"]:
                        miner_display = "✔"
                        max_store_display = player_property["miner_max"]
                        tier = player_property["miner_tier"]
                    else:
                        miner_display = "❌"
                        max_store_display = "/"
                        tier = "/"
                    item_checking = g.choicebox(f"请选择你要操作的物品 采矿机器人: {miner_display} LV {tier} "
                                                f"采矿机器人最大储存量: {max_store_display}",
                                                choices=inventory_display)
                    if item_checking is None:
                        break
                    elif item_checking == "合成界面":
                        while True:
                            if player_property["sm1"]:
                                craft_expr.pop("一级科学机器碎片 * 4 + 生铁 * 2 -> 一级科学机器", None)
                            if player_property["sm2"]:
                                craft_expr.pop("二级科学机器碎片 * 10 + 电路板（需要一级科学机器）-> 二级科学机器", None)
                            if player_property["sm3"]:
                                craft_expr.pop("三级科学机器碎片 * 15 + 中级电路板 -> 三级科学机器", None)
                            if player_property["sm4"]:
                                craft_expr.pop("四级科学机器碎片 * 5 + 高级电路板 -> 四级科学机器", None)
                            if player_property["miner"]:
                                craft_expr.pop("基础机械外壳 * 2 + 中级电路板 + 电路板 + 锡线 * 4 -> 采矿机器人", None)
                            craft_display = []
                            for craft_key in craft_expr.keys():
                                craft_display.append(craft_key)
                            sm_display = []
                            for i in range(4):
                                if player_property[f"sm{i + 1}"]:
                                    sm_display.append("✔")
                                else:
                                    sm_display.append("❌")
                            crafting_item = g.choicebox(f"请选择你要合成的物品 一级科学机器: {sm_display[0]}"
                                                        f"二级科学机器: {sm_display[1]} 三级科学机器: {sm_display[2]}"
                                                        f"四级科学机器: {sm_display[3]}",
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
                            elif item_property[craft_materials[1]]["craft"] == 3 and not player_property["sm3"]:
                                g.msgbox("你没有三级科学机器")
                                continue
                            elif item_property[craft_materials[1]]["craft"] == 4 and not player_property["sm4"]:
                                g.msgbox("你没有四级科学机器")
                                continue
                            materials_collections = collections.Counter(craft_materials[0])
                            pocket_collections = collections.Counter(pocket["inventory"])
                            cyn = False
                            for mat in materials_collections.keys():
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
                            while True:
                                breaking_craft_num = False
                                craft_num = g.enterbox("请输入你要合成的数量")
                                if craft_num is None:
                                    breaking_craft_num = True
                                    break
                                try:
                                    craft_num = int(craft_num)
                                except ValueError:
                                    continue
                                else:
                                    break
                            if breaking_craft_num:
                                continue
                            craft_count = 0
                            while craft_count < craft_num:
                                pocket_collections = collections.Counter(pocket["inventory"])
                                cyn = False
                                for mat in materials_collections.keys():
                                    if mat not in pocket_collections:
                                        cyn = True
                                        break
                                    elif pocket_collections[mat] < materials_collections[mat]:
                                        cyn = True
                                        break
                                if cyn:
                                    break
                                for mat in craft_materials[0]:
                                    pocket["inventory"].remove(mat)
                                if craft_materials[1] == 621:
                                    player_property["sm1"] = True
                                elif craft_materials[1] == 622:
                                    player_property["sm2"] = True
                                elif craft_materials[1] == 632:
                                    player_property["sm3"] = True
                                elif craft_materials[1] == 640:
                                    player_property["sm4"] = True
                                elif craft_materials[1] == 637:
                                    player_property["miner"] = True
                                else:
                                    pocket["inventory"].append(craft_materials[1])
                                craft_count += 1
                            if cyn:
                                g.msgbox(f"由于你的材料不够，你只合成了{craft_count} * {item_namespaces[craft_materials[1]]}")
                            else:
                                g.msgbox(f"你合成了{craft_count} * {item_namespaces[craft_materials[1]]}")

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
                                    pocket["inventory"].append(pocket["equip"]["armor"])
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
                    elif item_property[item_checking]["type"] == "exp":
                        while True:
                            use = g.indexbox(f"{item_namespaces[item_checking]}", choices=["使用", "信息", "丢弃"])
                            if use is None:
                                break
                            elif use == 0:
                                player_property["exp"] += item_property[item_checking]["heal"]
                                pocket["inventory"].remove(item_checking)
                                g.msgbox(f"你增加了{item_property[item_checking]['heal']}点EXP")
                                check_level()
                                break
                            elif use == 1:
                                g.msgbox(f"""
{item_namespaces[item_checking]}
增加{item_property[item_checking]["heal"]}点EXP
                                """)
                    elif item_property[item_checking]["type"] == "m":
                        while True:
                            use = g.indexbox(f"{item_namespaces[item_checking]}", choices=["使用", "信息", "丢弃"])
                            if use is None:
                                break
                            if use == 0:
                                if item_checking == 638:
                                    player_property["miner_max"] += 2000
                                    g.msgbox("你的采矿机器人的储存量增加了2000")
                                    pocket["inventory"].remove(item_checking)
                                    break
                                elif item_checking == 645:
                                    player_property["miner_tier"] += 1
                                    g.msgbox("你的采矿机器人升级了")
                                    pocket["inventory"].remove(item_checking)
                                    break
                                elif item_checking == 649:
                                    player_property["km"] += 1
                                    g.msgbox("你通过投掷末影珍珠前进了1km")
                                    pocket["inventory"].remove(item_checking)
                                    break
                                elif item_checking == 650:
                                    if not player_property["nether"]:
                                        teleport = g.choicebox("末影传送盒面板: 可传送的地点列表如下",
                                                               choices=place_display)
                                        if teleport is None:
                                            continue
                                        player_property["place"] = get_key(teleport, places)
                                        pocket["inventory"].remove(item_checking)
                                        g.msgbox(f"你传送到了{teleport}")
                                        break
                                    else:
                                        teleport = g.choicebox("末影传送盒面板: 可传送的地点列表如下",
                                                               choices=nether_place_display)
                                        if teleport is None:
                                            continue
                                        player_property["place"] = get_key(teleport, places)
                                        pocket["inventory"].remove(item_checking)
                                        g.msgbox(f"你传送到了{teleport}")
                                        break
                                elif item_checking == 654:
                                    player_property["nether"] = False
                                    player_property["place"] = 1
                                    pocket["inventory"].remove(item_checking)
                                    g.msgbox("你回到了海拉鲁台地")
                                    break
                                else:
                                    g.msgbox("你无法使用一个材料")
                            elif use == 1:
                                g.msgbox(f"""
{item_namespaces[item_checking]}
“{item_property[item_checking]["description"]}”
""")
                            elif use == 2:
                                pocket["inventory"].remove(item_checking)
                                g.msgbox(f"{item_namespaces[item_checking]}被扔的远远的")
                                break
    # explore UI
    elif choose == 2:
        while True:
            if not player_property["nether"]:
                if player_property["place"] == 80:
                    if not player_property["nether_dlc"]:
                        g.msgbox("你没有解锁下界DLC")
                        g.msgbox("正在回到海拉鲁台地")
                        player_property["place"] = 1
                        continue
                    elif not g.ccbox("前方就是下界传送门了，你要进入吗?（不进入则回到海拉鲁台地）", choices=["进入", "不了"]):
                        g.msgbox("正在回到海拉鲁台地")
                        player_property["place"] = 1
                        continue
                    else:
                        player_property["nether"] = True
                        player_property["place"] = 1
                        continue
                    player_property["km"] = 0.0
                if g.ccbox(f"“{player}”的HP: {player_property['hp']}/{player_property['max_hp']} "
                           f"法力: {player_property['mana']}/{player_property['max_mana']} "
                           f"体力: {player_property['str']}/{player_property['max_str']}\n"
                           f"目前位置: {places[player_property['place']]} {player_property['km']} / 10 km\n"
                           f"是否继续前进？", choices=["是的（消耗5体力）", "不了"]):
                    if player_property['str'] < 5:
                        g.msgbox("你没有足够的体力")
                        break
                else:
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
                if player_property['km'] >= 10:
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
            elif player_property["nether_dlc"]:
                if g.ccbox(f"“{player}”的HP: {player_property['hp']}/{player_property['max_hp']} "
                           f"法力: {player_property['mana']}/{player_property['max_mana']} "
                           f"体力: {player_property['str']}/{player_property['max_str']}\n"
                           f"目前位置: {nether_places[player_property['place']]} {player_property['km']} / 10 km\n"
                           f"是否继续前进？", choices=["是的（消耗5体力）", "不了"]):
                    if player_property['str'] < 5:
                        g.msgbox("你没有足够的体力")
                        break
                else:
                    break
                player_property["str"] -= 5
                player_property['km'] += 0.1
                player_property['km'] = round(player_property['km'], 1)
                event = random.choice(nether_explore_list[player_property["place"] - 1])
                if event == 70:
                    fight_ui("nether")
                else:
                    pocket["inventory"].append(event)
                    g.msgbox(f"你获得了{item_namespaces[event]}")
                if player_property['km'] >= 10:
                    player_property["place"] += 1
                    if player_property["place"] > 2:
                        player_property["place"] = 1
                    g.msgbox(f"你来到了{places[player_property['place']]}!")
    # shop UI
    elif choose == 3:
        while True:
            item_buying = g.choicebox("请选择你要购买的物品",
                                      choices=["收购", item_namespaces[121], item_namespaces[123], item_namespaces[127],
                                               item_namespaces[30], item_namespaces[14], item_namespaces[11],
                                               item_namespaces[31], item_namespaces[37], item_namespaces[38],
                                               item_namespaces[32], item_namespaces[33], item_namespaces[39],
                                               item_namespaces[310], item_namespaces[68], item_namespaces[617],
                                               item_namespaces[624], item_namespaces[610],
                                               item_namespaces[615], item_namespaces[616], item_namespaces[631],
                                               item_namespaces[639], item_namespaces[623], item_namespaces[653]])
            if item_buying is None:
                break
            elif item_buying == "收购":
                while True:
                    set_inventory_display(selling=True)
                    item_selling = g.choicebox("请选择你要出售的物品", choices=inventory_display)
                    if item_selling is None:
                        break
                    while True:
                        buy_num = g.enterbox("请输入你要售出的数量")
                        if buy_num is None:
                            break
                        try:
                            buy_num = int(buy_num)
                        except ValueError:
                            continue
                        item_selling = item_selling.split(" ")[0]
                        item_selling = get_key(item_selling)
                        get_gold = int(item_property[item_selling]["sell"] / 4)
                        buy_count = 0
                        while buy_count != buy_num and item_selling in pocket["inventory"]:
                            player_property["gold"] += get_gold
                            pocket["inventory"].remove(item_selling)
                            buy_count += 1
                        if buy_count == buy_num:
                            g.msgbox(f"你通过出售{item_namespaces[item_selling]} * {buy_count}获得了{get_gold * buy_count}$")
                        else:
                            g.msgbox(f"由于物品不够，你只通过出售{item_namespaces[item_selling]} * {buy_count}"
                                     f"获得了{get_gold * buy_count}$")
                        break
                continue
            item_buying = get_key(item_buying)
            if g.ccbox(f"""
{item_namespaces[item_buying]}
{item_property[item_buying]["sell"]}$
{item_property[item_buying]["description"]}
            """, choices=["购买", "取消"]):
                if player_property["gold"] >= item_property[item_buying]["sell"]:
                    while True:
                        buy_num = g.enterbox("请输入你要购买的数量")
                        if buy_num is None:
                            break
                        try:
                            buy_num = int(buy_num)
                        except ValueError:
                            continue
                        buy_count = 0
                        while buy_count < buy_num and player_property["gold"] >= item_property[item_buying]["sell"]:
                            player_property["gold"] -= item_property[item_buying]["sell"]
                            pocket["inventory"].append(item_buying)
                            buy_count += 1
                        if buy_count == buy_num:
                            g.msgbox(f"你花费{item_property[item_buying]['sell'] * buy_count}$购买了"
                                     f"{buy_count} * {item_namespaces[item_buying]}")
                        else:
                            g.msgbox(f"由于钱不够，你只花费{item_property[item_buying]['sell'] * buy_count}$购买了"
                                     f"{buy_count} * {item_namespaces[item_buying]}")
                        break
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
                    g.msgbox(f"你获得了{gear_display}")
                    break
                boss_skill_using = boss.random_skill()
                g.msgbox(f"{item_namespaces[boss.namespace]}使出了{item_namespaces[boss_skill_using]}")
                if random.randint(1, 100) < player_property["miss"] * 0.01 + \
                        item_property[pocket["equip"]["armor"]]["miss"] * 0.01 + \
                        player_property["inscription_buff"]["miss"] * 0.01:
                    g.msgbox(f"你似乎躲开了这次攻击")
                else:
                    if boss_skill_using == 50:
                        damage = int(boss.random_atk() *
                                     (1 - (player_property["define"] + item_property[pocket["equip"]["armor"]]["def"] +
                                           player_property["inscription_buff"]["def"]) * 0.0001 +
                                      player_property["inscription_buff"]["def_p"] * 0.01))
                    else:
                        damage = int(item_property[boss_skill_using]["atk"] *
                                     (1 - ((player_property["define"] + item_property[pocket["equip"]["armor"]]["def"] +
                                            player_property["inscription_buff"]["def"]) * 0.0001 +
                                           player_property["inscription_buff"]["def_p"] * 0.01)))
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
                                crit_damage = 1
                                if random.randint(1, 100) <= player_property["inscription_buff"]["crit"]:
                                    crit_damage = 1.75
                                    g.msgbox("暴击！")
                                damage = int((damage_current_value +
                                              player_property["inscription_buff"]["atk"]) *
                                             (1 + 0.01 * player_property["inscription_buff"]["atk_p"]) * (
                                                     1 - boss.define * 0.01) *
                                             crit_damage) + player_property["base_atk"]
                                boss.hp -= damage
                                g.msgbox(f"你对{item_namespaces[boss.namespace]}造成了{damage}点伤害")
                                hp_take = int(damage * player_property["inscription_buff"]["ht"] * 0.01)
                                player_property["hp"] += hp_take
                                if hp_take != 0:
                                    if hp_take > 0:
                                        g.msgbox(f"你吸取了{hp_take}点HP")
                                    else:
                                        g.msgbox(f"你被反噬了{hp_take}点HP")
                                if player_property["hp"] > player_property["max_hp"]:
                                    player_property["hp"] = player_property["max_hp"]
                                    g.msgbox("你的HP溢出了，可惜你无法保存溢出的HP")
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
                                                crit_damage = 1
                                                if random.randint(1, 100) <= player_property["inscription_buff"][
                                                    "crit"]:
                                                    crit_damage = 1.75
                                                    g.msgbox("暴击！")
                                                damage = int((damage_current_value +
                                                              player_property["inscription_buff"]["atk"]) *
                                                             (1 + 0.01 * player_property["inscription_buff"][
                                                                 "atk_p"]) * (1 - boss.define * 0.01) *
                                                             crit_damage) + player_property["base_atk"]
                                                boss.hp -= damage
                                                g.msgbox(f"你对{item_namespaces[boss.namespace]}造成了{damage}点伤害")
                                                hp_take = int(damage * player_property["inscription_buff"]["ht"] * 0.01)
                                                player_property["hp"] += hp_take
                                                if hp_take != 0:
                                                    if hp_take > 0:
                                                        g.msgbox(f"你吸取了{hp_take}点HP")
                                                    else:
                                                        g.msgbox(f"你被反噬了{hp_take}点HP")
                                                if player_property["hp"] > player_property["max_hp"]:
                                                    player_property["hp"] = player_property["max_hp"]
                                                    g.msgbox("你的HP溢出了，可惜你无法保存溢出的HP")
                                        elif skill_type == "c":
                                            cure_display(skill_num, True)
                                        elif skill_type == "m":
                                            mana_display(skill_num, True)
                                        else:
                                            strength_display(skill_num, True)

                                else:
                                    if item_property[skill_num]["type"] == "a":
                                        if random.randint(1, 10000) < boss.miss * 100:
                                            g.msgbox(f"{item_namespaces[boss.namespace]}似乎躲开了这次攻击")
                                        else:
                                            damage_current_value = item_property[skill_num]["atk"]
                                            crit_damage = 1
                                            if random.randint(1, 100) <= player_property["inscription_buff"]["crit"]:
                                                crit_damage = 1.75
                                                g.msgbox("暴击！")
                                            damage = int((damage_current_value +
                                                          player_property["inscription_buff"]["atk"]) *
                                                         (1 + 0.01 * player_property["inscription_buff"]["atk_p"]) * (
                                                                 1 - boss.define * 0.01) *
                                                         crit_damage) + player_property["base_atk"]
                                            boss.hp -= damage
                                            g.msgbox(f"你对{item_namespaces[boss.namespace]}造成了{damage}点伤害")
                                            hp_take = int(damage * player_property["inscription_buff"]["ht"] * 0.01)
                                            player_property["hp"] += hp_take
                                            if hp_take != 0:
                                                if hp_take > 0:
                                                    g.msgbox(f"你吸取了{hp_take}点HP")
                                                else:
                                                    g.msgbox(f"你被反噬了{hp_take}点HP")
                                            if player_property["hp"] > player_property["max_hp"]:
                                                player_property["hp"] = player_property["max_hp"]
                                                g.msgbox("你的HP溢出了，可惜你无法保存溢出的HP")

                                    elif item_property[skill_num]["type"] == "c":
                                        cure_display(skill_num, True)
                                    elif item_property[skill_num]["type"] == "m":
                                        mana_display(skill_num, True)
                                    else:
                                        strength_display(skill_num, True)
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
                    else:
                        continue
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
                for skill in item_property[pocket["equip"]["armor"]]["skill"]:
                    if skill != 0:
                        g.msgbox(f"{player}使出了{item_namespaces[skill]}!")
                        if item_property[skill]["type"] == "cm":
                            mana_display(skill, True)
                        elif item_property[skill]["type"] == "ca":
                            if random.randint(1, 10000) < boss.miss * 100:
                                g.msgbox(f"{item_namespaces[boss.namespace]}似乎躲开了这次攻击")
                            else:
                                damage_current_value = item_property[skill]["atk"]
                                crit_damage = 1
                                if random.randint(1, 100) <= player_property["inscription_buff"]["crit"]:
                                    crit_damage = 1.75
                                    g.msgbox("暴击！")
                                damage = int((damage_current_value +
                                              player_property["inscription_buff"]["atk"]) *
                                             (1 + 0.01 * player_property["inscription_buff"]["atk_p"]) * (
                                                     1 - boss.define * 0.01) *
                                             crit_damage) + player_property["base_atk"]
                                boss.hp -= damage
                                g.msgbox(f"你对{item_namespaces[boss.namespace]}造成了{damage}点伤害")
                                hp_take = int(damage * player_property["inscription_buff"]["ht"] * 0.01)
                                player_property["hp"] += hp_take
                                if hp_take != 0:
                                    if hp_take > 0:
                                        g.msgbox(f"你吸取了{hp_take}点HP")
                                    else:
                                        g.msgbox(f"你被反噬了{hp_take}点HP")
                                if player_property["hp"] > player_property["max_hp"]:
                                    player_property["hp"] = player_property["max_hp"]
                                    g.msgbox("你的HP溢出了，可惜你无法保存溢出的HP")
                        elif item_property[skill]["type"] == "cc":
                            cure_display(skill, True)
    elif choose == 7:
        ins_display = ["查看当前符文"]
        for i in inscriptions.keys():
            ins_display.append(i)
        ins_display.remove("空符文槽")
        while True:
            ins_choice = g.choicebox(f"符文系统 | 配置你的符文\n当前符文槽: {player_property['inscription_num']}/11\n",
                                     choices=ins_display)
            if ins_choice is None:
                break
            if ins_choice == "查看当前符文":
                while True:
                    ins_check = g.choicebox(f"""你当前的符文
| 加成 |
生命偷取: {player_property["inscription_buff"]["ht"]}%
ATK: {player_property["inscription_buff"]["atk"]} + {player_property["inscription_buff"]["atk_p"]}%ATK
DEF: {player_property["inscription_buff"]["def"]} + {player_property["inscription_buff"]["def_p"]}%DEF
暴击几率: {player_property["inscription_buff"]["crit"]}%
miss: {player_property["inscription_buff"]["miss"]}%
                    """, choices=player_property["inscriptions"])
                    if ins_check is None:
                        break
                    ins_property = inscriptions[ins_check]
                    while True:
                        if g.ccbox(f"""
{ins_check}
| 加成 |
生命偷取: {ins_property["ht"]}%
ATK: {ins_property["atk"]} + {ins_property["atk_p"]}%ATK
DEF: {ins_property["def"]} + {ins_property["def_p"]}%DEF
暴击几率: {ins_property["crit"]}%
miss: {ins_property["miss"]}%
                        """, choices=["卸下", "取消"]):
                            if ins_check == "空符文槽":
                                g.msgbox("你无法卸下符文槽")
                                continue
                            player_property["inscriptions"].remove(ins_check)
                            player_property["inscriptions"].append("空符文槽")
                            g.msgbox("已卸下")
                            break
                        else:
                            break
            else:
                ins_property = inscriptions[ins_choice]
                while True:
                    if g.ccbox(f"""
                {ins_choice}
                | 加成 |
                生命偷取: {ins_property["ht"]}%
                ATK: {ins_property["atk"]} + {ins_property["atk_p"]}%ATK
                DEF: {ins_property["def"]} + {ins_property["def_p"]}%DEF
                暴击几率: {ins_property["crit"]}%
                miss: {ins_property["miss"]}%
                                """, choices=["装备", "取消"]):
                        if ins_choice in player_property["inscriptions"]:
                            g.msgbox("你已经携带了该符文！")
                            continue
                        replace_ins = g.choicebox("请选择要替换的符文或符文槽", choices=player_property["inscriptions"])
                        if replace_ins is None:
                            continue
                        player_property["inscriptions"][player_property["inscriptions"].index(replace_ins)] = ins_choice
                        inscription_buff_set()
                        break
                    else:
                        break
    elif choose == 8:
        _update_save()
        g.msgbox("已存档")
    elif choose == 9:
        while True:
            if "创建新存档" in saves:
                saves.remove("创建新存档")
            save_changing = g.choicebox("请选择你要更换的存档（若要创建新存档，请重启游戏）", choices=saves)
            if save_changing is None:
                break
            elif save_changing == "无":
                continue
            player = save_changing
            with open(save_changing) as save_obj:
                save_txt = save_obj.read().rstrip().encode()
                save_txt = base64.b64decode(save_txt).decode()
                save_txt_list = save_txt.split("\n")
                exec("player_property = " + save_txt_list[0])
                exec("pocket = " + save_txt_list[1])
                _update_save_version()
            g.msgbox(f"存档已读取\n欢迎回来，{player}！")
            break
    elif choose == 10:
        while True:
            active_code = g.enterbox("请输入DLC兑换码")
            if active_code is None:
                break
            if base64.b64decode(active_code.encode()).decode() == player + "nether":
                player_property["nether_dlc"] = True
                g.msgbox("下界DLC已激活")
                break
    else:
        choosing_mod = mod_keys[choose]
        mod_checking = mod_objects[choosing_mod]
        mod_value_return = mod_checking.main(pocket=pocket, item_namespaces=item_namespaces,
                                             item_property=item_property, player_property=player_property,
                                             player=player)
        pocket = mod_value_return["pocket"]
        item_namespaces = mod_value_return["item_namespaces"]
        item_property = mod_value_return["item_property"]
        player_property = mod_value_return["player_property"]
        player = mod_value_return["player"]
