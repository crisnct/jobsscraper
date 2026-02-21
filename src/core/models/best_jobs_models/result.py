
from typing import Optional
from pydantic import BaseModel

from src.core.models.best_jobs_models.metadata import Metadata




class Result(BaseModel):
    company:Optional[str] = ""
    job_url:str
    meta_info:Optional[Metadata]
    