from typing import List, Optional
from pydantic import BaseModel


class Filter(BaseModel):
    platform: Optional[str] = None
    keywords: Optional[List[str]] = []
    location: Optional[str] = None
    roles: Optional[List[str]] = []
    remote: Optional[bool] = False
    hybrid: Optional[bool] = False
    onsite: Optional[bool] = False
    exclude: Optional[List[str]] = []
    max_results: Optional[int] = 20