from pydantic import BaseModel,Field,model_validator
class InstrumentInput(BaseModel):
    code:str=Field(min_length=2,max_length=60)
    name:str=Field(min_length=2,max_length=120)
    serial:str=Field(min_length=2,max_length=100)
    lower:float=Field(default=0,ge=0,le=100,allow_inf_nan=False)
    upper:float=Field(default=100,ge=0,le=100,allow_inf_nan=False)
    @model_validator(mode="after")
    def valid_range(self):
        if self.lower>=self.upper:raise ValueError("仪器量程下限必须小于上限")
        return self
