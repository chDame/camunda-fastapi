def create_tasks(worker):
    @worker.task(task_type="task1")
    async def task1(id:str):
        return {"businessKey": "cda"}
        
    @worker.task(task_type="task2")
    async def task2(businessKey: str):
        return {"businessKey": businessKey + "me"}