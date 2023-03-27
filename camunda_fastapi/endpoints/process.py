"""Service endpoints"""
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from camunda_fastapi.zeebe_containers import ZeebeContainer
from camunda_fastapi.c8clients.operate_client import OperateClient
from pyzeebe import ZeebeClient

router = APIRouter()

@router.get('/api/process/definition/latest')
@inject
async def tasks(operate_client: OperateClient = Depends(Provide[ZeebeContainer.operate_client])) -> None:
    return operate_client.process_definitions()

@router.post('/api/process/{bpmnProcessId}/start')
@inject
async def startProcess(bpmnProcessId:str, variables:dict, zeebe_client: ZeebeClient = Depends(Provide[ZeebeContainer.zeebe_client])) -> None:
    instance = await zeebe_client.run_process(bpmn_process_id=bpmnProcessId, variables=variables)
    return instance;