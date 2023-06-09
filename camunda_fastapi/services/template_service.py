import os
import json
import datetime

path = "workspace/templates/";

def resolve(name:str) -> str:
    return path+name

def find_names() -> list:
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
    return os.listdir(path)

def find_by_name(name:str) -> dict:
    f = open(resolve(name))
    data = json.load(f)
    f.close()
    return data

def save(name:str, template:dict) -> dict:
    #template["modified"] = datetime.datetime.now()
    json_object = json.dumps(template, indent=4)
    with open(resolve(name), "w") as outfile:
        outfile.write(json_object)
    return template

def delete(name:str):
    os.remove(resolve(name))
