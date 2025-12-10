from pydantic import BaseModel

class SupporterIn(BaseModel):
    name: str 
    class_: str 

class SupporterOut(BaseModel):
    id: int 
    name: str 
    class_: str 

class SupporterStatusIn(BaseModel):
    status: bool