"""Service endpoints"""
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from camunda_fastapi.services import form_service
from camunda_fastapi.zeebe_containers import ZeebeContainer
from camunda_fastapi.c8clients.operate_client import OperateClient

router = APIRouter()

@router.post('/api/auth/login')
def login(auth:dict) -> None:
    auth["profile"]="Admin"
    auth["token"]="someToken"
    auth["groups"]=["group1","group2"]
    
    return auth
    
@router.get('/api/auth/logout')
def logout() -> None:
    return {"result":"done"}