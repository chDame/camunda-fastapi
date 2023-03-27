"""Service endpoints"""
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from camunda_fastapi.services import template_service

router = APIRouter()

@router.get('/api/elttemplates')
def templates() -> None:
    return template_service.find_names()
    
    
@router.post('/api/elttemplates/{name}')
def save(name:str, template:dict) -> None:
    return template_service.save(name, template)

@router.get('/api/elttemplates/{name}')
def get_template(name:str) -> None:
    return template_service.find_by_name(name)
    
@router.delete('/api/elttemplates/{name}')
def delete(name:str) -> None:
    template_service.delete(name)
    
@router.get('/api/elttemplates/new/{name}')
def new(name:str) -> None:
    content = {
  "$schema" : "https://unpkg.com/@camunda/zeebe-element-templates-json-schema/resources/schema.json",
  "name" : "Some Connector",
  "id" : "io.camunda.someconnector",
  "description" : "Execute GraphQL query",
  "version" : 1,
  "category" : {
    "id" : "connectors",
    "name" : "Connectors"
  },
  "appliesTo" : [ "bpmn:Task" ],
  "elementType" : {
    "value" : "bpmn:ServiceTask"
  },
  "groups" : [ {
    "id" : "group1",
    "label" : "group1"
  }],
  "properties" : [ {
    "type" : "Hidden",
    "value" : "io.camunda:some-connector:1",
    "binding" : {
      "type" : "zeebe:taskDefinition:type"
    }
  }, {
    "label" : "Property",
    "id" : "myProperty",
    "group" : "group1",
    "description" : "some description of the propertu",
    "value" : "a value",
    "type" : "Text",
    "binding" : {
      "type" : "zeebe:input",
      "name" : "myProperty"
    }
  }]
}
    return template_service.save(name, content)