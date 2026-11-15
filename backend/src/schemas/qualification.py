from pydantic import BaseModel,Field,model_validator
from src.constants.enums import QualificationMode
class QualificationInput(BaseModel):
    title:str=Field(min_length=2,max_length=160)
    run_id:int
    mode:QualificationMode
    scope_low:float=Field(ge=0,le=100,allow_inf_nan=False)
    scope_high:float=Field(ge=0,le=100,allow_inf_nan=False)
    note:str=Field(min_length=10,max_length=1000)
    @model_validator(mode="after")
    def valid_scope(self):
        if self.scope_low>=self.scope_high:raise ValueError("资格范围下限必须小于上限")
        return self
