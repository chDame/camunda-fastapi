import base64

from pyzeebe import Job
from camunda_fastapi.services import mail_service

def create_mail_task(worker):
    @worker.task(task_type="mail", single_value=False)
    async def mail(*args, **kwargs) -> dict:
        print(type(kwargs))
        mail_service.send_mail(kwargs["to"], kwargs["subject"], kwargs["template"], kwargs["locale"], kwargs)
        return {}
