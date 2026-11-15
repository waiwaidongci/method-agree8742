from fastapi import APIRouter,Depends
from src.config.database import get_db
from src.utils.auth import current_user,editor
from src.schemas.instrument import InstrumentInput
from src.controllers.instrument_controller import list_instruments,create_instrument
router=APIRouter(prefix="/instruments")
@router.get("")
def index(db=Depends(get_db),user=Depends(current_user)):return list_instruments(db)
@router.post("",status_code=201)
def create(data:InstrumentInput,db=Depends(get_db),user=Depends(editor)):return create_instrument(db,data)
