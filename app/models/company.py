from pydantic import BaseModel


class Company(BaseModel):
    clientid: str
    companyid: str
    companyname: str
