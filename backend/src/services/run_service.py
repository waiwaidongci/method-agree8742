import hashlib,json
from sqlalchemy import select
from fastapi import HTTPException
from redis import Redis
from src.config.settings import REDIS_URL
from src.constants.enums import RunStatus
from src.models import PairDataset,PairedReading,Instrument,ComparisonRun
from src.services.agreement import agreement_analysis
from src.services.deming import inverse_calibrate
queue=Redis.from_url(REDIS_URL)
def list_runs(db):return db.scalars(select(ComparisonRun).order_by(ComparisonRun.id.desc())).all()
def get_run(db,id):
    run=db.get(ComparisonRun,id)
    if not run:raise HTTPException(404,"比对研究不存在")
    return run
def create_run(db,data):
    dataset=db.get(PairDataset,data.dataset_id)
    if not dataset:raise HTTPException(404,"数据集不存在")
    if db.scalar(select(ComparisonRun).where(ComparisonRun.name==data.name)):raise HTTPException(409,"研究名称已存在")
    run=ComparisonRun(**data.model_dump(),status=RunStatus.QUEUED);db.add(run);db.commit();queue.lpush("optics:runs",str(run.id));return run
def execute_run(db,id):
    run=db.get(ComparisonRun,id)
    if not run or run.status not in (RunStatus.QUEUED,RunStatus.RUNNING):return
    run.status=RunStatus.RUNNING;db.commit()
    try:
        dataset=db.get(PairDataset,run.dataset_id)
        rows=db.scalars(select(PairedReading).where(PairedReading.dataset_id==dataset.id,PairedReading.reference_value>=run.range_low,PairedReading.reference_value<=run.range_high).order_by(PairedReading.sample_code)).all()
        x=[r.reference_value for r in rows];y=[r.candidate_value for r in rows]
        result=agreement_analysis(x,y,run.lambda_ratio,run.bootstrap_count)
        config={key:getattr(run,key) for key in ('lambda_ratio','allowance','range_low','range_high','bootstrap_count')}
        instruments=[db.get(Instrument,dataset.reference_id),db.get(Instrument,dataset.candidate_id)]
        snapshot={"algorithm":"deming-ba-v1","dataset":{"id":dataset.id,"name":dataset.name,"source_file":dataset.source_file},"instruments":[{"id":i.id,"code":i.code,"unit":i.unit,"lower":i.lower,"upper":i.upper} for i in instruments],"pairs":[[r.sample_code,r.reference_value,r.candidate_value] for r in rows],"config":config,"seed":73}
        result.update({"fingerprint":hashlib.sha256(json.dumps(snapshot,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest(),"x_range":[min(x),max(x)],"y_range":[min(y),max(y)],"config":config,"instrument_codes":[i.code for i in instruments],"raw_eligible":result['lower_ci'][0]>=-run.allowance and result['upper_ci'][1]<=run.allowance and not result['heteroscedastic_warning'],"points":[{"code":r.sample_code,"x":r.reference_value,"y":r.candidate_value,"mean":(r.reference_value+r.candidate_value)/2,"diff":r.candidate_value-r.reference_value} for r in rows]})
        run.result=result;run.status=RunStatus.COMPLETED;run.error="";db.commit()
    except Exception as exc:
        db.rollback();run=db.get(ComparisonRun,id);run.status=RunStatus.FAILED;run.error=str(exc)[:600];db.commit()
def calibrate(db,id,value):
    run=get_run(db,id)
    if run.status!=RunStatus.COMPLETED:raise HTTPException(409,"研究尚未完成")
    try:estimate=inverse_calibrate(value,run.result['intercept'],run.result['slope'],run.result['x_range'],run.result['y_range'])
    except ValueError as exc:raise HTTPException(422,str(exc))
    return {"reference_estimate":estimate,"candidate_value":value,"scope":"研究内逆校准点估计，不含个体预测误差"}
