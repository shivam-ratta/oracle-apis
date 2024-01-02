from pydantic import BaseModel

class UserClient(BaseModel):
    loginname: str
    clientid: str
    clientname: str
