from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy import create_engine, Column, String, Text, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import uuid
from typing import Optional, List
from models import Base, Advertisement
from schemas import AdvertisementCreate, AdvertisementUpdate, Advertisement

# Database setup
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@db/app_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Advertisement Service", version="1.0.0")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/advertisements", response_model=Advertisement, status_code=201)
def create_advertisement(ad: AdvertisementCreate, db: Session = Depends(get_db)):
    db_ad = Advertisement(
        id=str(uuid.uuid4()),
        title=ad.title,
        description=ad.description,
        price=ad.price,
        author=ad.author,
        created_at=datetime.utcnow()
    )
    db.add(db_ad)
    db.commit()
    db.refresh(db_ad)
    return db_ad

@app.get("/advertisements/{ad_id}", response_model=Advertisement)
def read_advertisement(ad_id: str, db: Session = Depends(get_db)):
    db_ad = db.query(Advertisement).filter(Advertisement.id == ad_id).first()
    if db_ad is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return db_ad

@app.patch("/advertisements/{ad_id}", response_model=Advertisement)
def update_advertisement(ad_id: str, ad_update: AdvertisementUpdate, db: Session = Depends(get_db)):
    db_ad = db.query(Advertisement).filter(Advertisement.id == ad_id).first()
    if db_ad is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    
    update_data = ad_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_ad, field, value)
    
    db.commit()
    db.refresh(db_ad)
    return db_ad

@app.delete("/advertisements/{ad_id}")
def delete_advertisement(ad_id: str, db: Session = Depends(get_db)):
    db_ad = db.query(Advertisement).filter(Advertisement.id == ad_id).first()
    if db_ad is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    
    db.delete(db_ad)
    db.commit()
    return {"message": "Advertisement deleted successfully"}

@app.get("/advertisements", response_model=List[Advertisement])
def search_advertisements(
    title: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(Advertisement)
    
    if title:
        query = query.filter(Advertisement.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(Advertisement.author.ilike(f"%{author}%"))
    if min_price is not None:
        query = query.filter(Advertisement.price >= min_price)
    if max_price is not None:
        query = query.filter(Advertisement.price <= max_price)
    
    return query.all()
