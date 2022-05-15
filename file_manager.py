import json
import os
import sprites

data = {
    'save': [
        {
            'NAME': "user",
            'CURRENT_LEVEL': -1,
            'COINS': 0,
            "sprint_speed": 2,
            "hp": 20,
            "max_hp": 20,
            "auto_reg_lvl": 0,
            "auto_reg_amount": 1,
            "stamina": 30,
            "max_stamina": 30,
            "stamina_reg": 0.1,
            "stamina_cost": 1,
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
        with open('savefiles/data.json', 'w') as File:
            File.write(json.dumps(data, indent = 4))
            print(data)
            print("Create File!")
    else:
        print("File already exists!")


def read_file(region, key):
    with open('savefiles/data.json', 'r') as File:
        daten = json.load(File)
        for i in daten[region]:
            result = i[key]
        return result

def write_file(region, key, wert):
    with open("savefiles/data.json", "r") as File:
        data = json.load(File)

    for k in data[region]:
        k[key] = wert

    with open("savefiles/data.json", "w") as File:
        File.write(json.dumps(data, indent=4))
