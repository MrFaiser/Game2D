import json
import os

data = {
    'save': [
        {
            'NAME': "user",
            'CURRENT_LEVEL': 0,
            'COINS': 0
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
        print("File not empty!")


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

