# version <dv-003>
# lines: 434 + 4 (project description: 2; start blank: 1; end blank: 1) = 438

import easygui as g
import random
import settings
import os
import base64

item_namespaces = {
    0: "无",

    # weapon
    10: "手", 11: "木棍", 12: "波克棒", 13: "石板波克棒",

    # armor
    21: "石板甲",

    # medicine
    30: "绷带", 31: "医用绷带",

    # mobs
    41: "波布克林", 42: "蓝色波布克林", 43: "丘丘"
}
pocket = {"equip": {"weapon": 10, "armor": 0}, "inventory": [30]}
item_property = {
    # weapon
    10: {"atk": [1, 1], "type": "wep", "skill": "无", "description": "你无敌的手"},
    11: {"atk": [1, 3], "type": "wep", "skill": "无",
         "description": "一根普通的木棍，没有什么特别之处", "sell": 25},
    12: {"atk": [2, 4], "type": "wep", "skill": "无", "description": "经常能从波布克林身上找到的一个笨重的武器", "sell": 40},
    13: {"atk": [4, 7], "type": "wep", "skill": "无", "description": "蓝色波布克林使用的武器，和普通波克棒不同，它的上方"
                                                                    "附有石板以增强攻击力", "sell": 60},
    # armor
    21: {"def": 100, "miss": 50, "skill": "无", "type": "arm", "sell": 70,
         "description": "蓝色波克布林所使用的防具，十分简陋，但防御有效"},
    # medicine
    30: {"heal": 2, "type": "med", "buff": "无",
         "description": "普通的布质绷带，能包裹你的伤口", "sell": 10},
    31: {"heal": 5, "type": "med", "buff": "无",
         "description": "洒上酒精的绷带，这使它的治疗效果增加了2", "sell": 50},

    # mobs
    41: {"hp": 13, "atk": [1, 2], "type": "mob",
         "description": "一个浑身通红的怪物，四肢发达，头脑简单，还特别弱",
         "miss": 0, "define": 0, "gear": [11, 12], "gold": [2, 5], "exp": 3},
    42: {"hp": 25, "atk": [3, 4], "type": "mob",
         "description": "波布克林的一级加强版，聪明了些，武器也更加精良，甚至还有盔甲",
         "miss": 2, "define": 10, "gear": [13, 21], "gold": [7, 10], "exp": 6},
    43: {"hp": 5, "atk": [0, 1], "type": "mob",
         "description": "一个极弱的怪物，甚至有可能打出0点伤害...",
         "miss": 0, "define": 0, "gear": [11], "gold": [1, 3], "exp": 2},

    0: {"def": 0, "miss": 0},
}
player_property = {"lv": 1, "hp": 20, "max_hp": 20, "gold": 20, "miss": 5, "define": 0, "exp": 0,
                   "need exp": 10}

inventory_display = []

mobs = []

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


# functions
def get_key(value, dict_obj=None):
    if dict_obj is None:
        dict_obj = item_namespaces
    for key, val in dict_obj.items():
        if val == value:
            return key


def set_inventory_display(item_filter: list = None):
    """
    set up the display of the inventory for various modules, there is a filter to choose types
    :param item_filter: list; a filter, list can only contain "wep", "arm", "med" or "mob"
    """
    global inventory_display
    inventory_display = []
    if item_filter is None:
        if len(pocket["inventory"]) < 2:
            for i in pocket["inventory"]:
                inventory_display.append(item_namespaces[i])
            while len(inventory_display) < 2:
                inventory_display.append("无")
        else:
            for i in pocket["inventory"]:
                inventory_display.append(item_namespaces[i])
            while len(inventory_display) < 2:
                inventory_display.append("无")
    else:
        if len(pocket["inventory"]) < 2:
            for i in pocket["inventory"]:
                if item_property[i]["type"] in item_filter:
                    inventory_display.append(item_namespaces[i])
            while len(inventory_display) < 2:
                inventory_display.append("无")
        else:
            for i in pocket["inventory"]:
                if item_property[i]["type"] in item_filter:
                    inventory_display.append(item_namespaces[i])
                while len(inventory_display) < 2:
                    inventory_display.append("无")


def cure_display(item_checking):
    """
    a function using at display
    """
    player_property["hp"] += item_property[item_checking]["heal"]
    g.msgbox("你回复了" + str(item_property[item_checking]["heal"]) + "点HP")
    if player_property["hp"] > player_property["max_hp"]:
        g.msgbox(f"你的HP溢出了\n可惜的是，{item_namespaces[item_checking]}似乎"
                 "不会帮你保存溢出的HP")
        player_property["hp"] = player_property["max_hp"]
    elif player_property["hp"] == player_property["max_hp"]:
        g.msgbox("你的HP满了")
    pocket["inventory"].remove(item_checking)


def check_level():
    global player_property
    if player_property["exp"] >= player_property["need exp"]:
        player_property["lv"] += 1
        player_property["exp"] = player_property["exp"] - player_property["need exp"]
        player_property["need exp"] = player_property["lv"] * (10 + player_property["lv"]) + player_property["lv"] - 1
        player_property["max_hp"] = player_property["lv"] * 10 + int(player_property["lv"] * 2 - 1)
        player_property["hp"] = player_property["max_hp"]
        g.msgbox(f"你升级了！\n你目前的LV为{player_property['lv']}\n"
                 f"你的HP上限变为了{player_property['max_hp']}\n你的HP回满了")


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


run_environment = _get_path()
_makedir("save")
_option_go("save")
saves = os.listdir()
for save in saves:
    save.replace(run_environment, "")
g.msgbox("""
                                  fight dv-003
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
        g.msgbox(f"存档已读取\n欢迎回来，{player}！")
        break

# get mob list
for i in item_property.keys():
    if str(i)[0] == "4":
        mobs.append(i)

while True:
    check_level()
    choose = g.indexbox(f"你好，{player}！\n", choices=["状态", "背包", "商店", "贤者", "与普通怪物战斗", "存档"])
    if choose is None:
        g.msgbox("再见")
        exit()

    # status UI
    if choose == 0:
        g.msgbox(f"""
LV: {player_property["lv"]}
EXP: {player_property["exp"]}/{player_property["need exp"]}
HP: {player_property["hp"]}/{player_property["max_hp"]}
现金: {player_property["gold"]}$
武器：{item_namespaces[pocket["equip"]["weapon"]]}  ATK {item_property[pocket["equip"]["weapon"]]["atk"][0]} ~ {item_property[pocket["equip"]["weapon"]]["atk"][1]} 
盔甲：{item_namespaces[pocket["equip"]["armor"]]}  DEF {item_property[pocket["equip"]["armor"]]["def"]}
        """)
    # pocket UI
    if choose == 1:
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
                            elif use == 1:
                                g.msgbox(f"""
{item_namespaces[item_checking]}
atk: {item_property[item_checking]["atk"][0]} ~ {item_property[item_checking]["atk"][1]}
技能: {item_property[item_checking]["skill"]}
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
                            elif use == 1:
                                g.msgbox(f"""
{item_namespaces[item_checking]}
def: +{item_property[item_checking]["def"]}
miss: +{item_property[item_checking]["miss"]}
技能: {item_property[item_checking]["skill"]}
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
                    set_inventory_display()
                    item_checking = g.choicebox("请选择你要操作的物品", choices=inventory_display)
                    if item_checking is None:
                        break
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
技能: {item_property[item_checking]["skill"]}
“{item_property[item_checking]["description"]}”
""")
                            elif use == 2:
                                pocket["inventory"].remove(item_checking)
                                g.msgbox(f"{item_namespaces[item_checking]}被扔的远远的")
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
技能: {item_property[item_checking]["skill"]}
“{item_property[item_checking]["description"]}”
""")
                            elif use == 2:
                                pocket["inventory"].remove(item_checking)
                                g.msgbox(f"{item_namespaces[item_checking]}被扔的远远的")
                    elif item_property[item_checking]["type"] == "med":
                        while True:
                            use = g.indexbox(f"{item_namespaces[item_checking]}", choices=["使用", "信息", "丢弃"])
                            if use is None:
                                break
                            elif use == 0:
                                cure_display(item_checking)
                                break
                            elif use == 1:
                                g.msgbox(f"""
{item_namespaces[item_checking]}
回复{item_property[item_checking]["heal"]}点HP
“{item_property[item_checking]["description"]}”
""")
                            elif use == 2:
                                pocket["inventory"].remove(item_checking)
                                g.msgbox(f"{item_namespaces[item_checking]}被扔的远远的")
                                break
    # shop UI
    elif choose == 2:
        while True:
            item_buying = g.choicebox("请选择你要购买的物品",
                                      choices=[item_namespaces[30], item_namespaces[11], item_namespaces[31]])
            if item_buying is None:
                break
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
    # cure UI
    elif choose == 3:
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
    elif choose == 4:
        while True:
            breaking = False
            mob_object = item_property[random.choice(mobs)]
            mob = Mob(get_key(mob_object, item_property), mob_object["hp"],
                      mob_object["atk"], mob_object["description"], mob_object["miss"], mob_object["define"],
                      mob_object["gear"], mob_object["gold"], mob_object["exp"])
            g.msgbox(f"{item_namespaces[mob.namespace]}出现了！")
            while True:
                if player_property["hp"] <= 0:
                    g.msgbox("你 死 了")
                    if not settings.REBIRTH:
                        g.msgbox("游戏退出中")
                        exit()
                    g.msgbox("某种神秘的力量将你从死亡拉了回来，不过他似乎抽取了一些费用")
                    player_property["hp"] = 1
                    player_property["gold"] -= int(player_property["gold"] * 0.2)
                if mob.hp <= 0:
                    gear = random.choice(mob.gear)
                    gold = random.randint(mob.gold[0], mob.gold[1])
                    g.msgbox("你胜利了")
                    g.msgbox(f"你获得了{item_namespaces[gear]} * 1和{gold}$以及{mob.exp}点经验")
                    pocket["inventory"].append(gear)
                    player_property["gold"] += gold
                    player_property["exp"] += mob.exp
                    break
                fight_choose = g.indexbox(f"{item_namespaces[mob.namespace]} HP: {mob.hp}/{mob.max_hp}\n"
                                          f"“{player}”的HP: {player_property['hp']}/{player_property['max_hp']}",
                                          choices=["战斗", "查看", "物品", "逃跑"])
                if fight_choose == 0:
                    if random.randint(1, 100) < mob.miss:
                        g.msgbox(f"{item_namespaces[mob.namespace]}似乎躲开了这次攻击")
                    else:
                        if item_property[pocket["equip"]["weapon"]]["atk"][0] != \
                                item_property[pocket["equip"]["weapon"]]["atk"][1]:
                            damage_current_value = random.randint(item_property[pocket["equip"]["weapon"]]["atk"][0],
                                                                  item_property[pocket["equip"]["weapon"]]["atk"][1])
                        else:
                            damage_current_value = item_property[pocket["equip"]["weapon"]]["atk"][0]
                        damage = int(damage_current_value * (1 - mob.define * 0.01))
                        mob.hp -= damage
                        g.msgbox(f"你对{item_namespaces[mob.namespace]}造成了{damage}点伤害")
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
                    while True:
                        set_inventory_display(["med"])
                        item_using = g.choicebox("请选择你要使用的物品（只有药物）", choices=inventory_display)
                        if item_using is None:
                            break
                        item_using = get_key(item_using)
                        if item_using == 0:
                            g.msgbox("你想使用空气吗？")
                        else:
                            cure_display(item_using)
                            break
                elif fight_choose == 3 or fight_choose is None:
                    if g.ccbox("你确定要逃跑吗？", choices=["是的", "不了"]):
                        g.msgbox("你逃跑了")
                        breaking = True
                        break
                    else:
                        continue
                if random.randint(1, 100) < player_property["miss"] * 0.01 + \
                        item_property[pocket["equip"]["armor"]]["miss"] * 0.01:
                    g.msgbox(f"你似乎躲开了这次攻击")
                else:
                    damage = int(random.randint(mob.atk[0], mob.atk[1]) * (1 - (player_property["define"] +
                                                                                item_property[pocket["equip"]["armor"]][
                                                                                    "def"]) * 0.0001))
                    player_property["hp"] -= damage
                    g.msgbox(f"{item_namespaces[mob.namespace]}对你造成了{damage}点伤害")
            check_level()
            if breaking:
                breaking = False
                break
            if not g.ccbox("你是否要继续战斗（注意，你的血量不会回复）", choices=["是的", "不了"]):
                break
    elif choose == 5:
        _update_save()
        g.msgbox("已存档")
