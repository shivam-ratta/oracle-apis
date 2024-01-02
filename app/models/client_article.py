from pydantic import BaseModel


class ClientArticle(BaseModel):
    clientid: str
    companyid: str
    companyname: str
    headlines: str
    publicationname: str
    articleid: int
    articledate: str
    uploadcity: str
    journalist: str
    pagenos: str
    emailpriority: int
    haspdf: str
    hashtml: str
    articlesummary: str
    space: int
    pubgroupname: str
    pubcategory: str
    hassummary: str
    height: int
    width: int
    mailsectionid: int
    articledetailtextorgone: str
    artstate: str
    language: str
    tags: str
    tone: int
    priority: int
    otherpubs: str
