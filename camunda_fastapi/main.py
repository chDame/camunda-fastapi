import uvicorn
import asyncio

from asyncio import sleep
from typing import Callable

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from camunda_fastapi.endpoints import process, task
from camunda_fastapi.zeebe_containers import ZeebeContainer
from pyzeebe import ZeebeWorker


class App(FastAPI):
    """A FastAPI application"""

    def __init__(self, container_factory: Callable[[], ZeebeContainer] = ZeebeContainer):
        container = container_factory()
        container.wire(modules=[process])
        container.wire(modules=[task])

        super().__init__()
        self.container = container
        self.include_router(process.router)
        self.include_router(task.router)
        #self.mount('/webui', StaticFiles(directory='webui/public', html=True), name='static')


def create_app() -> App:
    """A FastAPI app factory"""
    app = App()
    zeebe_worker: ZeebeWorker = app.container.zeebe_worker.provided()
    running: boolean = True
    async def stop_workers():
        running = False
        zeebe_worker.stop()

    async def start_zeebe_worker():
        asyncio.ensure_future(run_zeebe_workers())
        
    async def run_zeebe_workers():
        while running:
            await zeebe_worker.work()
            await sleep(1000)

    app.add_event_handler('startup', start_zeebe_worker)
    app.add_event_handler('shutdown', zeebe_worker.stop)
    return app
    
    
app = create_app()

def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("camunda_fastapi.main:app", host="0.0.0.0", port=8000, reload=True)