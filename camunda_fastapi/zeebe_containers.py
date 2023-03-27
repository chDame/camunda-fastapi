import grpc
from dependency_injector import containers, providers

from camunda_fastapi.settings import Settings 
from pyzeebe import ZeebeClient, ZeebeWorker, create_camunda_cloud_channel
from camunda_fastapi.workers import create_tasks
from camunda_fastapi.tasklist_client import TasklistClient
from camunda_fastapi.operate_client import OperateClient

def create_channel(settings: Settings) -> grpc.aio.Channel:
    channel = create_camunda_cloud_channel(client_id=settings.client_id, client_secret=settings.client_secret,
                                           cluster_id=settings.cluster_id)
    return channel
    
def create_client(channel: grpc.aio.Channel) -> ZeebeClient:
    client = ZeebeClient(grpc_channel=channel)
    return client;
    
def create_worker(channel: grpc.aio.Channel) -> ZeebeWorker:
    worker = ZeebeWorker(grpc_channel=channel)
    create_tasks(worker)
    return worker;
        
def create_tasklist_client(settings: Settings) -> TasklistClient:
    return TasklistClient(settings=settings)
    
def create_operate_client(settings: Settings) -> OperateClient:
    return OperateClient(settings=settings)
    
class ZeebeContainer(containers.DeclarativeContainer):
    """Dependency Injection container"""
    settings: providers.Provider[Settings] = providers.Singleton(
        Settings
    )
    channel: providers.Provider[grpc.aio.Channel] = providers.Factory(
        create_channel,
        settings=settings,
    )
    zeebe_client: providers.Provider[ZeebeClient] = providers.ThreadLocalSingleton(
        create_client,
        channel=channel,
    )
    zeebe_worker: providers.Provider[ZeebeWorker] = providers.ThreadLocalSingleton(
        create_worker,
        channel=channel,
    )
    tasklist_client: providers.Provider[TasklistClient] = providers.ThreadLocalSingleton(
        create_tasklist_client,
        settings=settings,
    )
    operate_client: providers.Provider[OperateClient] = providers.ThreadLocalSingleton(
        create_operate_client,
        settings=settings,
    )