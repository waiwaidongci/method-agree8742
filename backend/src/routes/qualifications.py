from fastapi import APIRouter,Depends,Response
from src.config.database import get_db
from src.utils.auth import current_user,editor,admin
from src.schemas.qualification import QualificationInput
from src.controllers.qualification_controller import list_qualifications,create_qualification,approve_qualification,export_qualification
router=APIRouter(prefix="/qualifications")
@router.get("")
def index(db=Depends(get_db),user=Depends(current_user)):return list_qualifications(db)
@router.post("",status_code=201)
def create(data:QualificationInput,db=Depends(get_db),user=Depends(editor)):return create_qualification(db,data)
@router.patch("/{id}/approve")
def approve(id:int,db=Depends(get_db),user=Depends(admin)):return approve_qualification(db,id,user)
@router.get("/{id}/export")
def export(id:int,db=Depends(get_db),user=Depends(current_user)):return Response(export_qualification(db,id),media_type="text/csv; charset=utf-8",headers={"Content-Disposition":f'attachment; filename="optics-qualification-{id}.csv"'})
