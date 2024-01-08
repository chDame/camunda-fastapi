import asyncio
import requests

from camunda_fastapi.settings import Settings 
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from requests.auth import HTTPBasicAuth
import json

class TasklistClient:
    def __init__(self, *, settings: Settings):
        self.settings = settings
        self.x = requests.post('https://login.cloud.camunda.io/oauth/token', json = {'grant_type':'client_credentials', 'audience':'tasklist.camunda.io', 'client_id': settings.client_id, 'client_secret':settings.client_secret})
        self.token = self.x.json()['access_token']
        
    async def claim(self, task_id: int, assignee:str):
        transport = AIOHTTPTransport(url="https://bru-2.tasklist.camunda.io/"+self.settings.cluster_id+"/graphql",
        headers={'Authorization': 'Bearer '+self.token})

        # Using `async with` on the client will start a connection on the transport
        # and provide a `session` variable to execute queries on this connection
        async with Client(
            transport=transport,
            fetch_schema_from_transport=True,
        ) as session:
            query = gql(
                """
                mutation ClaimTask($taskId: String!, $assignee: String) {
                    claimTask(taskId: $taskId, assignee: $assignee) {
                        id
                        assignee
                    }
                }
            """
            )
            params = {
                "taskId": task_id,
                "assignee": assignee
            }
            result = await session.execute(query, variable_values=params)
            
    async def unclaim(self, task_id: int):
        transport = AIOHTTPTransport(url="https://bru-2.tasklist.camunda.io/"+self.settings.cluster_id+"/graphql",
        headers={'Authorization': 'Bearer '+self.token})

        # Using `async with` on the client will start a connection on the transport
        # and provide a `session` variable to execute queries on this connection
        async with Client(
            transport=transport,
            fetch_schema_from_transport=True,
        ) as session:
            query = gql(
                """
                mutation UnclaimTask($taskId: String!) {
                    unclaimTask(taskId: $taskId) {
                        id
                    }
                }
            """
            )
            params = {
                "taskId": task_id
            }
            result = await session.execute(query, variable_values=params)
        
    async def complete(self, task_id: int, variables:dict):
        transport = AIOHTTPTransport(url="https://bru-2.tasklist.camunda.io/"+self.settings.cluster_id+"/graphql",
        headers={'Authorization': 'Bearer '+self.token})

        # Using `async with` on the client will start a connection on the transport
        # and provide a `session` variable to execute queries on this connection
        async with Client(
            transport=transport,
            fetch_schema_from_transport=True,
        ) as session:
            query = gql(
                """
                mutation CompleteTask($taskId: String!, $variables: [VariableInput!]!) {
                    completeTask(taskId: $taskId, variables: $variables) {
                        id
                        taskState
                        variables {
                            name
                            value
                            __typename
                        }
                        completionTime
                        __typename
                    }
                }
                """
            )
            varibalesInput=[]
            for key in variables:
                varibalesInput.append({"name":key,"value":json.dumps(variables[key])});
                
            params = {
                "taskId": task_id,
                "variables": varibalesInput
            }
            result = await session.execute(query, variable_values=params)

    async def read_tasks(self):
        search={"state": "CREATED"}
        headers={"Authorization": "Bearer "+self.token, "Content-Type":"application/json"}
        response = requests.post('https://bru-2.tasklist.camunda.io/'+self.settings.cluster_id+'/v1/tasks/search', headers=headers, data=json.dumps(search), verify=True)
        
        return response.json();