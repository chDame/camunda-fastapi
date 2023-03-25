"""Service endpoints"""
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from camunda_fastapi.zeebe_containers import ZeebeContainer
from pyzeebe import ZeebeClient

router = APIRouter()


@router.get('/startProcess')
@inject
async def startProcess(zeebe_client: ZeebeClient = Depends(Provide[ZeebeContainer.zeebe_client])) -> None:
    instance = await zeebe_client.run_process(bpmn_process_id="python-process", variables={"id":"toto"})
    return instance;
