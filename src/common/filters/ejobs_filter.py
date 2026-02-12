from typing import Optional
from pydantic import BaseModel


class EJobsFilter(BaseModel):
    location:Optional[str]