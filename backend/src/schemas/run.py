from pydantic import BaseModel,Field,model_validator
class RunInput(BaseModel):
    name:str=Field(min_length=2,max_length=160)
    dataset_id:int
    lambda_ratio:float=Field(default=1,ge=.01,le=100,allow_inf_nan=False)
    allowance:float=Field(default=3,gt=0,le=50,allow_inf_nan=False)
    range_low:float=Field(default=0,ge=0,le=100,allow_inf_nan=False)
    range_high:float=Field(default=100,ge=0,le=100,allow_inf_nan=False)
    bootstrap_count:int=Field(default=500,ge=200,le=2000)
    @model_validator(mode="after")
    def valid_range(self):
        if self.range_low>=self.range_high:raise ValueError("研究范围下限必须小于上限")
        return self
class CalibrationInput(BaseModel):
    candidate_value:float=Field(ge=0,le=100,allow_inf_nan=False)
