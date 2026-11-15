from fastapi import APIRouter,Depends,Query
from src.config.database import get_db
from src.utils.auth import current_user
from src.controllers.reading_controller import list_readings
router=APIRouter(prefix="/readings")
@router.get("")
def index(dataset_id:int,search:str=Query(default="",max_length=80),offset:int=Query(default=0,ge=0),limit:int=Query(default=25,ge=1,le=200),db=Depends(get_db),user=Depends(current_user)):return list_readings(db,dataset_id,search,offset,limit)
