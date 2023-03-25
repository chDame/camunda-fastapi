import asyncio
import threading
import requests
import time
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

    async def read_tasks(self):
        transport = AIOHTTPTransport(url="https://bru-2.tasklist.camunda.io/"+self.settings.cluster_id+"/graphql",
        headers={'Authorization': 'Bearer '+self.token})

        # Using `async with` on the client will start a connection on the transport
        # and provide a `session` variable to execute queries on this connection
        async with Client(
            transport=transport,
            fetch_schema_from_transport=True,
        ) as session:

            # Execute single query
            query = gql(
                """
                query GetTasks($assignee: String, $assigned: Boolean, $state: TaskState, $pageSize: Int, $searchAfter: [String!], $searchBefore: [String!], $searchAfterOrEqual: [String!]) {
                    tasks(
                        query: {assignee: $assignee, assigned: $assigned, state: $state, pageSize: $pageSize, searchAfter: $searchAfter, searchBefore: $searchBefore, searchAfterOrEqual: $searchAfterOrEqual}
                    ) {
                        id
                        name
                        processName
                        assignee
                        creationTime
                        taskState
                        sortValues
                        isFirst
                        __typename
                        variables {
                            id
                            name
                            value
                            previewValue
                            isValueTruncated
                            __typename
                        }
                    }
                }
            """
            )
            params = {
                "state": "CREATED"
            }
            result = await session.execute(query, variable_values=params)

            return result["tasks"]