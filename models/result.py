
from typing import Optional
from pydantic import BaseModel

class Result(BaseModel):
    company:Optional[str] = ""
    job_url:str
    meta_info:Optional[str] = ""
    