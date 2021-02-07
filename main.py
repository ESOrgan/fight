# version <dv-001>
# lines: 221 + 4 (project description: 2; start blank: 1; end blank: 1) = 225

import easygui as g

item_namespaces = {
    0: "无",
    10: "手", 11: "木棍",
    30: "绷带"

}
pocket = {"equip": {"weapon": 10, "armor": 0}, "inventory": [30]}
item_property = {
    10: {"atk": 1, "type": "wep", "skill": "无", "description": "你无敌的手"},
    11: {"atk": 2, "type": "wep", "skill": "无",
         "description": "一根普通的木棍，没有什么特别之处", "sell": 5},
    30: {"heal": 1, "type": "med", "buff": "无",
         "description": "普通的布质绷带，能包裹你的伤口", "sell": 10},
    0: {'def': 0}
}
player_property = {"lv": 1, "hp": 10, "max_hp": 11, "gold": 40}

inventory_display = []


def get_key(value, dict_obj=None):
    if dict_obj is None:
        dict_obj = item_namespaces
    for key, val in dict_obj.items():
        if val == value:
            return key


g.msgbox("""
                                  fight dv-001
                                      欢迎
""")
while True:
    player = g.enterbox("请输入玩家的名字")
    if player is None:
        exit()
    break
while True:
    choose = g.indexbox(f"你好，{player}！\n", choices=["背包"])
    if choose is None:
        g.msgbox("再见")
        exit()

    # pocket UI
    if choose == 0:
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
atk: {item_property[item_checking]["atk"]}
技能: {item_property[item_checking]["skill"]}
“{item_property[item_checking]["description"]}”
    """)
                            elif use == 2:
                                if item_checking == 10:
                                    g.msgbox("你不能砍掉你的手！")
                                elif item_checking == 0:
                                    g.msgbox("你不能剥掉你的皮！")
                                elif item_property[item_checking]["type"] == "wep":
                                    pocket["equip"]["weapon"] = 10
                                else:
                                    pocket["equip"]["armor"] = 0
                                g.msgbox(f"{item_namespaces[item_checking]}被扔的远远的")
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
                            def: {item_property[item_checking]["atk"]}
                            技能: {item_property[item_checking]["skill"]}
                            “{item_property[item_checking]["description"]}”
                            """)
                            elif use == 2:
                                if item_checking == 10:
                                    g.msgbox("你不能砍掉你的手！")
                                elif item_checking == 0:
                                    g.msgbox("你不能剥掉你的皮！")
                                elif item_property[item_checking]["type"] == "wep":
                                    pocket["equip"]["weapon"] = 10
                                else:
                                    pocket["equip"]["armor"] = 0
                                g.msgbox(f"{item_namespaces[item_checking]}被扔的远远的")
            else:
                inventory_display = []
                # set display list
                if len(pocket["inventory"]) < 2:
                    for i in pocket["inventory"]:
                        inventory_display.append(item_namespaces[i])
                    while len(inventory_display) < 2:
                        inventory_display.append("无")
                else:
                    for i in pocket["inventory"]:
                        inventory_display.append(item_namespaces[i])
                while True:
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
                                pocket["inventory"].append(pocket["equip"]["weapon"])
                                pocket["equip"]["weapon"] = item_checking
                            elif use == 1:
                                g.msgbox(f"""
{item_namespaces[item_checking]}
atk: {item_property[item_checking]["atk"]}
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
                                pocket["inventory"].append(item_checking)
                                pocket["equip"]["armor"] = 0
                            elif use == 1:
                                g.msgbox(f"""
{item_namespaces[item_checking]}
def: {item_property[item_checking]["atk"]}
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
                                player_property["hp"] += item_property[item_checking]["heal"]
                                g.msgbox("你回复了" + str(item_property[item_checking]["heal"]) + "点HP")
                                if player_property["hp"] > player_property["max_hp"]:
                                    g.msgbox(f"你的HP溢出了\n可惜的是，{item_namespaces[item_checking]}似乎"
                                             "不会帮你保存溢出的HP")
                                elif player_property["hp"] == player_property["max_hp"]:
                                    g.msgbox("你的HP满了")
                                pocket["inventory"].remove(item_checking)
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
            item_buying = g.choicebox("请选择你要购买的物品", choices=[item_namespaces[30], item_namespaces[11]])
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
