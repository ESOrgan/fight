# version <pf-001>
# lines: 105 + 4 (project description: 2 + 1; end blank: 1) = 101

import easygui as g


def get_key(dict_obj, value):
    for key, val in dict_obj.items():
        if val == value:
            return key


item_namespaces = {
    0: "无", 10: "手", 11: "木棍"
}
pocket = {"equip": {"weapon": 10, "armor": 0}, "inventory": []}
item_property = {
    10: {"atk": 1, "type": "wep", "skill": "无", "description": "你无敌的手"},
    11: {"atk": 2, "type": "wep", "skill": "无", "description": "一根普通的木棍，没有什么特别之处"}
}
player_property = {"lv": 1, "hp": 10}

inventory_display = []

g.msgbox("""
                                  fight ra-001
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
                item_checking = g.choicebox("请选择你要操作的物品", choices=[item_namespaces[pocket["equip"]["weapon"]],
                                                                   item_namespaces[pocket["equip"]["armor"]]
                                                                   ])
                item_checking = get_key(item_namespaces, item_checking)
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
                # set display list
                if pocket["inventory"] is []:
                    inventory_display = ["无", "无"]
                else:
                    for i in pocket["inventory"]:
                        inventory_display.append(get_key(item_namespaces, i))
                while True:
                    item_checking = g.choicebox("请选择你要操作的物品", choices=inventory_display)
                    item_checking = get_key(item_namespaces, item_checking)
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
