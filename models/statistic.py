from typing import Optional
from pydantic import BaseModel



class Statistic(BaseModel):
    jobsFound:Optional[int] = 0
    totalRequestsSent:Optional[int] = 0