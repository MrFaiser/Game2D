import json
import os

import pygame

import sprites

data = {
    'save': [
        {   #player stats
            'name': "user",
            'current_level': -1,
            'coins': 0,
            'xp': 0,
            'xp_points': 0,
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
            "npc_gun": 0

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

def get_completed_quests():
    print("r", "complete")
    with open('files/quest_settings.json', 'r') as File:
        daten = json.load(File)
        quests = []
        for i in daten:
            if read_quest_file(i, "completed"):
                quests.append(i)
        return quests

def get_open_quests():
    print("r", "open")
    with open('files/quest_settings.json', 'r') as File:
        daten = json.load(File)
        quests = []
        for i in daten:
            if read_quest_file(i, "completed") == False:
                quests.append(i)
        return quests

def is_avtiv(NameDerQuest):
    print("r", "activ")
    for i in data:
        if read_quest_file(NameDerQuest, "activ"):
            return True

def set_avtiv(NameDerQuest):
    print("wQa")
    with open("files/quest_settings.json", "r") as File:
        data = json.load(File)

    for k in data[NameDerQuest]:
        k["activ"] = True

    with open("files/quest_settings.json", "w") as File:
        File.write(json.dumps(data, indent=4))


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