
from pydantic import BaseModel

class Result(BaseModel):
    company:str
    job_url:str
    meta_info:str
    