from sqlalchemy import select
from fastapi import HTTPException
from src.models import Instrument
def list_instruments(db):return db.scalars(select(Instrument).order_by(Instrument.id)).all()
def create_instrument(db,data):
    if db.scalar(select(Instrument).where(Instrument.code==data.code)):raise HTTPException(409,"仪器编号已存在")
    item=Instrument(**data.model_dump());db.add(item);db.commit();return item
