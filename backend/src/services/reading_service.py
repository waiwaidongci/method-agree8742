from sqlalchemy import select,func
from fastapi import HTTPException
from src.models import PairDataset,PairedReading
def list_readings(db,dataset_id,search,offset,limit):
    if not db.get(PairDataset,dataset_id):raise HTTPException(404,"配对数据集不存在")
    q=select(PairedReading).where(PairedReading.dataset_id==dataset_id)
    if search:q=q.where(PairedReading.sample_code.contains(search,autoescape=True))
    total=db.scalar(select(func.count()).select_from(q.subquery()))
    return {"total":total,"rows":db.scalars(q.order_by(PairedReading.sample_code).offset(offset).limit(limit)).all()}
