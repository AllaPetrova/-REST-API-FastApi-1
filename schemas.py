from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AdBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    author: str

class AdCreate(AdBase):
    pass

class AdUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    author: Optional[str] = None

class AdResponse(AdBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
