import json
import os

data = {
    'save': [
        {
            'NAME': "user",
            'CURRENT_LEVEL': 0,
            'TEST': 'test3'
        }
    ]
}


def create_file():
    if(os.stat("savefiles/data.json").st_size == 0):
        with open('savefiles/data.json', 'w') as f:
            f.write(json.dumps(data, indent = 4))
            print(data)
            print("Create File!")
    else:
        print("File not empty!")


def read_file(region, key):
    with open('savefiles/data.json', 'r') as f:
        daten = json.load(f)
        for i in daten[region]:
            result = i[key]
        return result

def write_file(region, key, wert):

    dat = open('savefiles/data.json', 'r')
    chance_data = json.load(dat)

    with open('savefiles/data.json', 'w') as f:
        daten = json.load(f)
        for i in daten[region]:
            chance_data[key] = wert
            #json.dump(chance_data, f)
            f.write(json.dumps(chance_data, indent=4))

    #    json.dumps(data, indent=10, sort_keys=False)


