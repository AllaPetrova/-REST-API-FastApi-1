from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class AdvertisementBase(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    author: str = Field(..., max_length=100)

class AdvertisementCreate(AdvertisementBase):
    pass

class AdvertisementUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    author: Optional[str] = Field(None, max_length=100)

class Advertisement(AdvertisementBase):
    id: str
    created_at: datetime
    
    class Config:
        orm_mode = True
