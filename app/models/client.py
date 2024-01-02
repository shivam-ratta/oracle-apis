from pydantic import BaseModel


class Client(BaseModel):
    clientid: str
    companyid: str
    companyname: str
