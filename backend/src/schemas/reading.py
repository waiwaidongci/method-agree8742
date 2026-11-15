from pydantic import BaseModel,Field
class ReadingInput(BaseModel):
    sample_code:str=Field(min_length=1,max_length=80)
    reference_value:float=Field(ge=0,le=100,allow_inf_nan=False)
    candidate_value:float=Field(ge=0,le=100,allow_inf_nan=False)
