"""Service endpoints"""
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from camunda_fastapi.zeebe_containers import ZeebeContainer
from camunda_fastapi.tasklist_client import TasklistClient
from pyzeebe import ZeebeClient

router = APIRouter()


@router.get('/api/startProcess')
@inject
async def startProcess(zeebe_client: ZeebeClient = Depends(Provide[ZeebeContainer.zeebe_client])) -> None:
    instance = await zeebe_client.run_process(bpmn_process_id="python-process", variables={"id":"toto"})
    return instance;

@router.get('/api/tasks')
@inject
async def tasks(tasklist_client: TasklistClient = Depends(Provide[ZeebeContainer.tasklist_client])) -> None:
    tasks = await tasklist_client.read_tasks()
    return tasks;
    
@router.get('/api/tasks/{task_id}/claim')
@inject
async def tasks(task_id:int, tasklist_client: TasklistClient = Depends(Provide[ZeebeContainer.tasklist_client])) -> None:
    tasks = await tasklist_client.claim(task_id=task_id, assignee="python")
    return tasks;