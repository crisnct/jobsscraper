
from typing import Optional
from pydantic import BaseModel

from models.metadata import Metadata

class Result(BaseModel):
    company:Optional[str] = ""
    job_url:str
    meta_info:Optional[Metadata]
    