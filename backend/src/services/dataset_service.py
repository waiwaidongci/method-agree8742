import csv,io
from sqlalchemy import select,func
from fastapi import HTTPException
from pydantic import ValidationError
from src.models import PairDataset,PairedReading,Instrument
from src.schemas.reading import ReadingInput
def list_datasets(db):
    rows=db.execute(select(PairDataset,func.count(PairedReading.id)).outerjoin(PairedReading,PairedReading.dataset_id==PairDataset.id).group_by(PairDataset.id)).all()
    return [{"id":d.id,"name":d.name,"reference_id":d.reference_id,"candidate_id":d.candidate_id,"source_file":d.source_file,"note":d.note,"row_count":n} for d,n in rows]
def create_dataset(db,data):
    if data.reference_id==data.candidate_id:raise HTTPException(422,"参考与候选必须为不同仪器")
    ref=db.get(Instrument,data.reference_id);candidate=db.get(Instrument,data.candidate_id)
    if not ref or not candidate:raise HTTPException(404,"仪器不存在")
    if ref.unit!=candidate.unit:raise HTTPException(422,"两台仪器必须使用相同量纲")
    if db.scalar(select(PairDataset).where(PairDataset.name==data.name)):raise HTTPException(409,"数据集名称已存在")
    try:rows=[ReadingInput.model_validate(x) for x in csv.DictReader(io.StringIO(data.csv_text))]
    except (ValidationError,ValueError,csv.Error) as exc:raise HTTPException(422,f"CSV校验失败：{str(exc)[:300]}")
    if not 20<=len(rows)<=5000:raise HTTPException(422,"需要20–5000对样本")
    if len({r.sample_code for r in rows})!=len(rows):raise HTTPException(422,"样本编号不得重复，每个独立试件一对读数")
    if any(not ref.lower<=r.reference_value<=ref.upper or not candidate.lower<=r.candidate_value<=candidate.upper for r in rows):raise HTTPException(422,"读数超出仪器登记量程")
    item=PairDataset(**data.model_dump(exclude={"csv_text"}));db.add(item);db.flush();db.add_all([PairedReading(dataset_id=item.id,**r.model_dump()) for r in rows]);db.commit();return {"id":item.id,"row_count":len(rows)}
