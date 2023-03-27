import os
import json
import datetime

formsPath = "workspace/forms/";

def resolve_form(name:str) -> str:
    return formsPath+name

def find_names() -> list:
    return os.listdir(formsPath)

def find_by_name(formKey:str) -> dict:
    f = open(resolve_form(formKey))
    data = json.load(f)
    f.close()
    if not "generator" in data:
        data["generator"]="formJs"
    return data

def save_form(form:dict) -> dict:
    form["modified"] = datetime.datetime.now()
    json_object = json.dumps(form, indent=4)
    with open(resolve_form(form["name"]), "w") as outfile:
        outfile.write(json_object)
    return form

def delete(name:str):
    os.remove(resolve_form(name))
