import os
import json
import datetime

path = "workspace/mails/";

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

def save(mail:dict) -> dict:
    mail["modified"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    json_object = json.dumps(mail, indent=4)
    with open(resolve(mail["name"]), "w") as outfile:
        outfile.write(json_object)
    return mail

def delete(name:str):
    os.remove(resolve(name))
