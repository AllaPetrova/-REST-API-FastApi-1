from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class AdModel(Base):
    __tablename__ = "advertisements"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    author = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

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

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Advertisement Service", version="1.0.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/advertisement", response_model=AdResponse)
async def create_advertisement(ad: AdCreate, db: Session = Depends(get_db)):
    db_ad = AdModel(**ad.dict())
    db.add(db_ad)
    db.commit()
    db.refresh(db_ad)
    return db_ad

@app.get("/advertisement/{advertisement_id}", response_model=AdResponse)
async def get_advertisement(advertisement_id: int, db: Session = Depends(get_db)):
    db_ad = db.query(AdModel).filter(AdModel.id == advertisement_id).first()
    if db_ad is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return db_ad

@app.get("/advertisement", response_model=List[AdResponse])
async def search_advertisements(
    title: Optional[str] = None,
    description: Optional[str] = None,
    author: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = db.query(AdModel)
    
    if title:
        query = query.filter(AdModel.title.ilike(f"%{title}%"))
    if description:
        query = query.filter(AdModel.description.ilike(f"%{description}%"))
    if author:
        query = query.filter(AdModel.author.ilike(f"%{author}%"))
    if min_price is not None:
        query = query.filter(AdModel.price >= min_price)
    if max_price is not None:
        query = query.filter(AdModel.price <= max_price)
    
    ads = query.order_by(AdModel.created_at.desc()).all()
    return ads

@app.patch("/advertisement/{advertisement_id}", response_model=AdResponse)
async def update_advertisement(
    advertisement_id: int, 
    ad_update: AdUpdate, 
    db: Session = Depends(get_db)
):
    db_ad = db.query(AdModel).filter(AdModel.id == advertisement_id).first()
    if db_ad is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    
    update_data = ad_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_ad, field, value)
    
    db.commit()
    db.refresh(db_ad)
    return db_ad

@app.delete("/advertisement/{advertisement_id}")
async def delete_advertisement(advertisement_id: int, db: Session = Depends(get_db)):
    db_ad = db.query(AdModel).filter(AdModel.id == advertisement_id).first()
    if db_ad is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    
    db.delete(db_ad)
    db.commit()
    return {"message": "Advertisement deleted successfully"}

@app.get("/")
async def root():
    return {"message": "Advertisement Service is running"}
