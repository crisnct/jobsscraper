from pydantic import BaseModel


class Error(BaseModel):
    code:int
    count:int