from pydantic import BaseModel
#create a schema for the user model
class UserCreate(BaseModel):
    name: str
    age: int
    birth_state: str

class UserOut(UserCreate):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
