from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    USERTYPE: str
    USERNAME: str
    LOGINNAME: str
    PASSWORD: str
    ISACTIVE: str
    CREATEDBY: str
    CREATEDON: str
    MODIFIEDON: Optional[str] = None
    MODIFIEDBY: Optional[str] = None
    IPADDRESS: str
    MACADDRESS: Optional[str] = None
    USERSID: int
    CLIENTID: Optional[int] = None
    ALLOWMAIL: str


class TokenRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
