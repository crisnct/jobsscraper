from typing import Optional
from pydantic import BaseModel


class Metadata(BaseModel):
    work_type: Optional[str] = ""
    payment: Optional[str] = ""
    experience: Optional[str] = ""