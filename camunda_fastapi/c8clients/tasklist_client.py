import asyncio
from operator import truediv
from pickle import TRUE
import requests

from camunda_fastapi.settings import Settings 
from requests.auth import HTTPBasicAuth
import json

class TasklistClient:
    def __init__(self, *, settings: Settings):
        self.settings = settings
        self.x = requests.post('https://login.cloud.camunda.io/oauth/token', json = {'grant_type':'client_credentials', 'audience':'tasklist.camunda.io', 'client_id': settings.client_id, 'client_secret':settings.client_secret})
        self.token = self.x.json()['access_token']
        
    async def claim(self, task_id: int, assignee:str):
        body={
          "assignee": assignee,
          "allowOverrideAssignment": True
        }
        headers={"Authorization": "Bearer "+self.token, "Content-Type":"application/json"}
        response = requests.patch('https://bru-2.tasklist.camunda.io/'+self.settings.cluster_id+'/v1/tasks/'+str(task_id)+'/assign', headers=headers, data=json.dumps(body), verify=True)
        
        return response.json();
            
    async def unclaim(self, task_id: int):
        headers={"Authorization": "Bearer "+self.token, "Content-Type":"application/json"}
        response = requests.patch('https://bru-2.tasklist.camunda.io/'+self.settings.cluster_id+'/v1/tasks/'+str(task_id)+'/unassign', headers=headers, verify=True)
        
        return response.json();
        
    async def complete(self, task_id: int, variables:dict):
        varibalesInput=[]
        for key in variables:
            varibalesInput.append({"name":key,"value":json.dumps(variables[key])});
        body={"variables": varibalesInput}
        headers={"Authorization": "Bearer "+self.token, "Content-Type":"application/json"}
        response = requests.patch('https://bru-2.tasklist.camunda.io/'+self.settings.cluster_id+'/v1/tasks/'+str(task_id)+'/complete', headers=headers, data=json.dumps(body), verify=True)
        
        return response.json();

    async def read_tasks(self):
        search={"state": "CREATED"}
        headers={"Authorization": "Bearer "+self.token, "Content-Type":"application/json"}
        response = requests.post('https://bru-2.tasklist.camunda.io/'+self.settings.cluster_id+'/v1/tasks/search', headers=headers, data=json.dumps(search), verify=True)
        
        return response.json();
        
    async def read_variables(self, task_id:int):
        headers={"Authorization": "Bearer "+self.token, "Content-Type":"application/json"}
        response = requests.post('https://bru-2.tasklist.camunda.io/'+self.settings.cluster_id+'/v1/tasks/'+str(task_id)+'/variables/search', headers=headers, data=json.dumps({}), verify=True)
        
        return response.json();
