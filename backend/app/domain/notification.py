from pydantic import BaseModel


class Notification(BaseModel):
    name: str
    email: str
    message: str
