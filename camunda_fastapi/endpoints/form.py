"""Service endpoints"""
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from camunda_fastapi.services import form_service
from camunda_fastapi.zeebe_containers import ZeebeContainer
from camunda_fastapi.c8clients.operate_client import OperateClient

router = APIRouter()

@router.get('/api/edition/forms/names')
def forms() -> None:
    return form_service.find_names()
    
@router.post('/api/edition/forms')
def forms(form:dict) -> None:
    return form_service.save_form(form)

@router.get('/api/edition/forms/{name}')
def get_form(name:str) -> None:
    return form_service.find_by_name(name)
    
@router.delete('/api/edition/forms/{name}')
def delete(name:str) -> None:
    form_service.delete(name)
    
    
@router.get("/api/forms/{processDefinitionId}/{formKey}")
def form_schema(processDefinitionId:str, formKey:str) -> None:
    return form_schema("test", processDefinitionId, formKey)

@router.get("/api/forms/{processName}/{processDefinitionId}/{formKey}")
def form_schema(processName:str, processDefinitionId:str, formKey:str) -> None:
    return localized_form_schema(processName, processDefinitionId, formKey, "en")

@router.get("/api/forms/{processName}/{processDefinitionId}/{formKey}/{locale}")
@inject
def localized_form_schema(processName:str, processDefinitionId:str, formKey:str, locale:str, operate_client: OperateClient = Depends(Provide[ZeebeContainer.operate_client])) -> None:

    if formKey.startswith("camunda-forms:bpmn:"):
      formId = formKey[formKey.rindex(":") + 1:]
      return operate_client.embedded_form(processDefinitionId, formId)


    form = form_service.find_by_name(formKey)
    schema = form["schema"]
    schema["generator"] = form["generator"]
    
    return schema
  
@router.get("/api/forms/instanciation/{bpmnProcessId}")
def getInstanciationFormSchema(bpmnProcessId:str) -> None:
    form = form_service.find_by_name(bpmnProcessId);
    schema = form["schema"]
    schema["generator"] = form["generator"]
    return schema