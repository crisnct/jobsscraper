
from typing import List, Optional
from pydantic import BaseModel

from src.common.models.best_jobs_models.result import Result
from src.common.models.best_jobs_models.statistic import Statistic



class AppResponse(BaseModel):
    results: Optional[List[Result]] = []
    statistics: Optional[Statistic] = None