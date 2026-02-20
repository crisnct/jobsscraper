
from typing import List, Optional
from pydantic import BaseModel

from src.core.models.best_jobs_models.result import Result
from src.core.models.best_jobs_models.statistic import Statistic





class BestJobsResponse(BaseModel):
    results: Optional[List[Result]] = []
    statistics: Optional[Statistic] = None