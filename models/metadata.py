from typing import Optional
from pydantic import BaseModel


class Metadata(BaseModel):
    date: Optional[str]
    role:Optional[str]