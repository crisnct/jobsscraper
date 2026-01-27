from typing import List, Optional
from pydantic import BaseModel

from src.models.result import Result
from src.models.statistic import Statistic


class AppResponse(BaseModel):
    results: Optional[List[Result]] = []
    statistics: Optional[Statistic] = None