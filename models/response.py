from typing import List, Optional
from pydantic import BaseModel
from models.result import Result
from models.statistic import Statistic


class AppResponse(BaseModel):
    results: Optional[List[Result]] = []
    statistics: Optional[Statistic] = None