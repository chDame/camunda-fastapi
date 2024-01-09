import base64

from pyzeebe import Job
from pyzeebe.errors import BusinessError
from camunda_fastapi.services import mail_service

def create_mail_task(worker):
    @worker.task(task_type="email", single_value=False)
    async def mail(*args, **kwargs) -> dict:
        print(type(kwargs))
        if kwargs["to"]=="christophe.dame@camunda.com":
            raise BusinessError("MAIL_FORMAT_ERROR")
        else:
            mail_service.send_mail(kwargs["to"], kwargs["subject"], kwargs["template"], kwargs["locale"], kwargs)
        return {}
