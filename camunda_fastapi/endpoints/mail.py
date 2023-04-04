"""Service endpoints"""
import chevron
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from camunda_fastapi.services import mail_service
from camunda_fastapi.zeebe_containers import ZeebeContainer
from camunda_fastapi.c8clients.operate_client import OperateClient

router = APIRouter()

@router.get('/api/edition/mails/names')
def names() -> None:
    return mail_service.find_names()
    
@router.post('/api/edition/mails')
def save(mail:dict) -> None:
    return mail_service.save(mail)

@router.get('/api/edition/mails/{name}')
def get(name:str) -> None:
    return mail_service.find_by_name(name)
    

@router.post('/api/edition/mails/preview')
def preview(mail:dict) -> None:
    return chevron.render(mail["htmlTemplate"], mail["previewData"])
    
@router.delete('/api/edition/mails/{name}')
def delete(name:str) -> None:
    mail_service.delete(name)