"""Service endpoints"""
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from camunda_fastapi.zeebe_containers import ZeebeContainer
from camunda_fastapi.c8clients.tasklist_client import TasklistClient
from pyzeebe import ZeebeClient

router = APIRouter()

@router.get('/api/tasks')
@inject
async def tasks(tasklist_client: TasklistClient = Depends(Provide[ZeebeContainer.tasklist_client])) -> None:
    tasks = await tasklist_client.read_tasks()
    return tasks;
    
@router.post('/api/tasks/search')
@inject
async def tasks(tasklist_client: TasklistClient = Depends(Provide[ZeebeContainer.tasklist_client])) -> None:
    tasks = await tasklist_client.read_tasks()
    return tasks;   
 
@router.get('/api/tasks/{task_id}/claim')
@inject
async def tasks(task_id:int, tasklist_client: TasklistClient = Depends(Provide[ZeebeContainer.tasklist_client])) -> None:
    tasks = await tasklist_client.claim(task_id=task_id, assignee="python")
    return tasks;
    
@router.get('/api/tasks/{task_id}/unclaim')
@inject
async def tasks(task_id:int, tasklist_client: TasklistClient = Depends(Provide[ZeebeContainer.tasklist_client])) -> None:
    tasks = await tasklist_client.unclaim(task_id=task_id)
    return tasks;
    
@router.post('/api/tasks/{task_id}')
@inject
async def tasks(task_id:int, variables:dict, tasklist_client: TasklistClient = Depends(Provide[ZeebeContainer.tasklist_client])) -> None:
    tasks = await tasklist_client.complete(task_id=task_id, variables=variables)
    return tasks;
    