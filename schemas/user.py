from typing import Optional
from pydantic import BaseModel

# Model that represents the database columns used for queries
class User(BaseModel):
    # Optional 'id' field of type integer, defaults to None
    id: Optional[int] = None
    # 'name' field of type string, required
    name: str
    # 'email' field of type string, required
    email: str
    # 'password' field of type string, required
    password: str