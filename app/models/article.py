from pydantic import BaseModel
from typing import Optional


class Article(BaseModel):
    companyname: Optional[str] = None
    link: Optional[str] = None
    socialfeedid: Optional[int] = None
    feeddate: Optional[str] = None
    headlines: Optional[str] = None
    publication: Optional[str] = None
    publicationid: Optional[str] = None
    summary_snippet: Optional[str] = None
    emailpriority: Optional[int] = None
    companyid: Optional[str] = None
    tone: Optional[str] = None
    reach: Optional[int] = None
    engagement: Optional[int] = None
    articledatenumber: Optional[int] = None
