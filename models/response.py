from typing import List
from pydantic import BaseModel
from models.result import Result
from models.statistic import Statistic


class AppResponse(BaseModel):
    results: List[Result]
    statistics: List[Statistic]