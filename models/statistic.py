from typing import List
from pydantic import BaseModel
from models.error import Error 


class Statistic(BaseModel):
    totalRequestsSent:int
    successfullRequests:int
    errors:List[Error]