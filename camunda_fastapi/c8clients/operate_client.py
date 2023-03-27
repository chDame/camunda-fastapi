import asyncio
import requests

from camunda_fastapi.settings import Settings 
from requests.auth import HTTPBasicAuth
import json
import xml.etree.ElementTree as ET

class OperateClient:
    def __init__(self, *, settings: Settings):
        self.settings = settings
        self.x = requests.post('https://login.cloud.camunda.io/oauth/token', json = {'grant_type':'client_credentials', 'audience':'operate.camunda.io', 'client_id': settings.client_id, 'client_secret':settings.client_secret})
        self.token = self.x.json()['access_token']
        
    def process_definitions(self):
        search={"filter":{},"size":1000,"sort":[{"field":"name","order":"ASC"},{"field":"version","order":"DESC"}]}
        headers={"Authorization": "Bearer "+self.token, "Content-Type":"application/json"}
        response = requests.post('https://bru-2.operate.camunda.io/'+self.settings.cluster_id+'/v1/process-definitions/search', headers=headers, data=json.dumps(search), verify=True)
        definitions = response.json()["items"]
        result = []
        result.append(definitions[0])
        lastDefId=definitions[0]["bpmnProcessId"]
        for definition in definitions:
            if (lastDefId!=definition["bpmnProcessId"]):
                result.append(definition)
                lastDefId=definition["bpmnProcessId"]
        return result

    def embedded_form(self, processDefinitionId:str, formId:str):
        headers={"Authorization": "Bearer "+self.token}
        response = requests.get('https://bru-2.operate.camunda.io/'+self.settings.cluster_id+'/v1/process-definitions/'+processDefinitionId+'/xml', headers=headers)
        xml = response.text
        tree = ET.ElementTree(ET.fromstring(xml))
        return json.loads(tree.getroot().find("./*/*/*[@id='"+formId+"']").text)
