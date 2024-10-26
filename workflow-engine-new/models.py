from pydantic import BaseModel



class Result(BaseModel):
    _id:str
    is_failed:bool
    result_dict:dict
    
class Process(BaseModel):
    _id: str
    status: str = "pending"
    type: str
    computer_name: str
    result:Result = None
    