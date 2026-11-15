import csv,io
from sqlalchemy import select
from fastapi import HTTPException
from src.models import Qualification,ComparisonRun
from src.constants.enums import RunStatus,QualificationMode,QualificationStatus
def list_qualifications(db):return db.scalars(select(Qualification).order_by(Qualification.id.desc())).all()
def validate_scope(run,mode,low,high):
    if run.status!=RunStatus.COMPLETED:raise HTTPException(409,"研究尚未完成")
    if low<run.result['x_range'][0]-1e-9 or high>run.result['x_range'][1]+1e-9:raise HTTPException(422,"资格范围必须包含在本次实际观测X范围内")
    if mode==QualificationMode.RAW and not run.result['raw_eligible']:raise HTTPException(422,"原值互换条件未满足：需外侧bootstrap界限在允许误差内，且无异方差提示")
def create_qualification(db,data):
    run=db.get(ComparisonRun,data.run_id)
    if not run:raise HTTPException(404,"研究不存在")
    validate_scope(run,data.mode,data.scope_low,data.scope_high)
    if db.scalar(select(Qualification).where(Qualification.title==data.title)):raise HTTPException(409,"资格档案标题已存在")
    item=Qualification(**data.model_dump(),status=QualificationStatus.DRAFT);db.add(item);db.commit();return item
def approve_qualification(db,id,user):
    item=db.get(Qualification,id)
    if not item:raise HTTPException(404,"资格档案不存在")
    run=db.get(ComparisonRun,item.run_id);validate_scope(run,item.mode,item.scope_low,item.scope_high)
    item.status=QualificationStatus.APPROVED;item.approved_by=user.email;db.commit();return item
def export_qualification(db,id):
    item=db.get(Qualification,id)
    if not item:raise HTTPException(404,"资格档案不存在")
    if item.status!=QualificationStatus.APPROVED:raise HTTPException(409,"先由负责人批准资格档案")
    run=db.get(ComparisonRun,item.run_id);result=run.result
    output=io.StringIO();output.write("\ufeff");writer=csv.writer(output)
    writer.writerow(['sample_code','reference_pct','candidate_pct','difference_pct','inverse_calibrated_pct','mode','scope_low','scope_high','run_fingerprint'])
    for point in result['points']:
        if item.scope_low<=point['x']<=item.scope_high:
            code=point['code'];code=("'"+code) if code.startswith(('=','+','-','@','\t','\r')) else code
            writer.writerow([code,point['x'],point['y'],point['diff'],(point['y']-result['intercept'])/result['slope'],item.mode,item.scope_low,item.scope_high,result['fingerprint']])
    return output.getvalue()
