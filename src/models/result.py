
from typing import Optional
from pydantic import BaseModel
from src.models.metadata import Metadata


class Result(BaseModel):
    company:Optional[str] = ""
    job_url:str
    meta_info:Optional[Metadata]
    