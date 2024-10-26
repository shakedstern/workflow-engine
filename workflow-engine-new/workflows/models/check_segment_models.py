from pydantic import BaseModel


class CheckSegemtResult(BaseModel):
    address:str
    dns:str

class CheckSegmentsResult(BaseModel):
    process_id:str
    unavailable:list[CheckSegemtResult]
    available:list[CheckSegemtResult]

    