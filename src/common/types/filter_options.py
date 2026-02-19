from typing import TypeAlias

from src.common.filters.best_jobs_filter import BestJobsFilter
from src.common.filters.ejobs_filter import EJobsFilter
FilterOptions:TypeAlias = BestJobsFilter | EJobsFilter #TODO: add more filters and add them to the type alias