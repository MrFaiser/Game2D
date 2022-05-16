import json
import os
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
            "health_pack": 20,
            "stamina": 30,
            "max_stamina": 30,
            "stamina_reg": 0.1,
            "stamina_cost": 1,

            #upgrade lvl
            "UPGRADE_LEVEL_max_health_up": 0,
            "UPGRADE_LEVEL_health_pack_up": 0,
            "UPGRADE_LEVEL_auto_reg_up": 0,
            "UPGRADE_LEVEL_auto_reg_amount": 0,
            "UPGRADE_LEVEL_show_player_hp": 0,

            #Weapon
            "pistol_ammo": 25,
            "shotgun_ammo": -1,
            "sniper_ammo": -1,
            "rifle_ammo": -1,
            "laser_ammo": 1234567890,
            "compas_lvl": 1,
            "compas_all": False

        }
    ]
}


def create_file():
    if(os.stat("savefiles/data.json").st_size == 0):
        print("c")
        with open('savefiles/data.json', 'w') as File:
            File.write(json.dumps(data, indent = 4))
            print(data)
            print("Create File!")
    else:
        print("File already exists!")


def read_file(region, key):
    print("r", key)
    with open('savefiles/data.json', 'r') as File:
        daten = json.load(File)
        for i in daten[region]:
            result = i[key]
        return result

def write_file(region, key, wert):
    print("w", key, wert)
    with open("savefiles/data.json", "r") as File:
        data = json.load(File)

    for k in data[region]:
        k[key] = wert

    with open("savefiles/data.json", "w") as File:
        File.write(json.dumps(data, indent=4))
