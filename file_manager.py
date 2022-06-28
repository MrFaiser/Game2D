import json
import os

import pygame

import sprites

data = {
    'save': [
        {   #game stats
            'name': "user",
            'current_level': -1,
            'coins': 0,
            'xp': 0,
            'xp_points': 0,
            #inf
            "inventory": {},

            #player stats
            "sprint_speed": 1.5,
            "hp": 20,
            "max_hp": 20,
            "auto_reg_time": 6.5,
            "auto_reg_amount": 0,
            "health_pack": 20,
            "stamina": 30,
            "max_stamina": 30,
            "stamina_reg": 0.1,
            "stamina_cost": 1,

            #upgrade lvl
            "UPGRADE_LEVEL_max_health_up": 0,
            "UPGRADE_LEVEL_health_pack_up": 0,
            "UPGRADE_LEVEL_auto_reg_up_time": 0,
            "UPGRADE_LEVEL_auto_reg_amount": 0,
            "UPGRADE_LEVEL_show_player_hp": 0,

            #Weapon
            "pistol_ammo": 25,
            "shotgun_ammo": -1,
            "sniper_ammo": -1,
            "rifle_ammo": -1,
            "laser_ammo": 1234567890,
            "compas_lvl": 1,
            "compas_all": False,

            #NPC
            "npc": 0,
            "npc_gun": 0,
            "npc_quest_boy": 0

        }
    ]
}


def create_file():
    if(os.stat("files/data.json").st_size == 0):
        print("c")
        with open('files/data.json', 'w') as File:
            File.write(json.dumps(data, indent = 4))
            print(data)
            print("Create File!")
    else:
        print("File already exists!")

def read_file(region, key):
    print("r", key)
    with open('files/data.json', 'r') as File:
        daten = json.load(File)
        for i in daten[region]:
            result = i[key]
        return result

def write_file(region, key, wert):
    print("w", key, wert)
    with open("files/data.json", "r") as File:
        data = json.load(File)

    for k in data[region]:
        k[key] = wert

    with open("files/data.json", "w") as File:
        File.write(json.dumps(data, indent=4))



#######################################################
#INVENTORY#
#GET
def get_inventory(region):
    print("r", "inventory")
    with open('files/data.json', 'r') as File:
        daten = json.load(File)
        for i in daten[region]:
            result = i["inventory"]
        return result

def get_amount_from_item_in_inventory(region, item):
    if is_item_in_inventory(region, item):
        result = get_inventory(region)[item]
        return result
    else:
        return -1


#IS
def is_item_in_inventory(region, item):
    if item in get_inventory(region):
        return True
    else:
        return False

#SET - ADD
def add_item_to_inventory(region, item, amount):
    if is_item_in_inventory(region, item):
        temp = get_inventory(region)
        temp[item] = get_amount_from_item_in_inventory(region, item) + amount
        write_file(region, "inventory", temp)
        print("ist drin... ")
    else:
        print("add neu")


#######################################################
#QUEST#
#GET
def get_Quest_file():
    print("oQ")
    with open('files/quest_settings.json', 'r') as f:
        data = json.load(f)
    return data

def read_quest_file(NameDerQuest, key):
    print("r-Q", key)
    with open('files/quest_settings.json', 'r') as File:
        daten = json.load(File)
        for i in daten[NameDerQuest]:
            result = i[key]
        return result

def get_all_quest_name():
    print("r", "all")
    with open('files/quest_settings.json', 'r') as File:
        daten = json.load(File)
        quests = []
        for i in daten:
            quests.append(i)
        return quests

def get_all_activ_quest():
    print("r", "complete")
    with open('files/quest_settings.json', 'r') as File:
        daten = json.load(File)
        quests = []
        for i in daten:
            if read_quest_file(i, "activ"):
                quests.append(i)
        return quests

def get_all_completed_quests():
    print("r", "complete")
    with open('files/quest_settings.json', 'r') as File:
        daten = json.load(File)
        quests = []
        for i in daten:
            if read_quest_file(i, "completed"):
                quests.append(i)
        return quests

def get_all_available_quests():
    print("r", "complete")
    with open('files/quest_settings.json', 'r') as File:
        daten = json.load(File)
        quests = []
        for i in daten:
            if read_quest_file(i, "available"):
                quests.append(i)
        return quests

def get_all_available_and_not_completet_quests():
    print("r", "complete")
    with open('files/quest_settings.json', 'r') as File:
        daten = json.load(File)
        quests = []
        for i in daten:
            if read_quest_file(i, "available"):
                if not read_quest_file(i, "completed"):
                    quests.append(i)
        return quests

def set_quest_completed(nameFromQuest):
    with open("files/quest_settings.json", "r") as File:
        data = json.load(File)

    for k in data[nameFromQuest]:
        k["completed"] = True

    with open("files/quest_settings.json", "w") as File:
        File.write(json.dumps(data, indent=4))

def get_all_not_completed_quests():
    print("r", "open")
    with open('files/quest_settings.json', 'r') as File:
        daten = json.load(File)
        quests = []
        for i in daten:
            if read_quest_file(i, "completed") == False:
                quests.append(i)
        return quests

def get_all_not_completed_but_activ_quests():
    print("r", "open")
    with open('files/quest_settings.json', 'r') as File:
        daten = json.load(File)
        quests = []
        for i in daten:
            if read_quest_file(i, "completed") == False:
                if read_quest_file(i, "activ") == True:
                    quests.append(i)
        return quests

def get_quest_attribute(nameFromQuest, attribute):
        for i in get_Quest_file()[nameFromQuest]:
            result = i[attribute]
        return result

#######################################################
#IS
def is_avtiv(nameFromQuest):
    print("r", "activ")

    for i in get_Quest_file():
        if read_quest_file(nameFromQuest, "activ"):
            return True

def is_completed(nameFromQuest):
    print("r", "completed")

    for i in get_Quest_file():
        if read_quest_file(nameFromQuest, "completed"):
            return True


#######################################################
#SET
def set_avtiv(nameFromQuest):
    print("wQa")
    with open("files/quest_settings.json", "r") as File:
        data = json.load(File)

    for k in data[nameFromQuest]:
        k["activ"] = True

    with open("files/quest_settings.json", "w") as File:
        File.write(json.dumps(data, indent=4))

def set_available(nameFromQuest):
    print("wQa")
    with open("files/quest_settings.json", "r") as File:
        data = json.load(File)

    for k in data[nameFromQuest]:
        k["available"] = True

    with open("files/quest_settings.json", "w") as File:
        File.write(json.dumps(data, indent=4))



#######################################################
#DEMO
file = {
    "welcome": [
        {
            "activ": False,
            "completed": False,
            "text": "text",
            "description": "sprech mit dem quest boy",
            "require": 0,
            "currency": "coins",
            "reward_xp": 0,
            "reward_coin": 0,
            "reward_text": "viel erfolg noch. brooo"
        }
    ],
	"100Coins": [
        {
            "activ": False,
            "completed": False,
            "text": "text",
            "description": "geb mir 100 coins",
            "require": 100,
            "currency": "coins",
            "reward_xp": 100,
            "reward_coin": 50,
            "reward_text": "hier noch mal 50Coins kek"
        }
    ]
}

