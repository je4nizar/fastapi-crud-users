from typing import Optional
from pydantic import BaseModel

#model that represents the database columns that we will use for queries
class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    password: str