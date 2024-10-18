from pydantic import BaseModel


# blog
class NamesSchema(BaseModel):
    name : str 
    first_name : str = None
    last_name : str = None
    
class ResponseNamesSchema(NamesSchema):
    id: int



# authentication
class LoginResponseSchema(BaseModel):
    token: str
    user_id: int
    detail: str


class LoginRequestSchema(BaseModel):
    username: str
    password: str

# register user
class RegisterRequestSchema(BaseModel):
    username: str
    password: str

class RegisterResponseSchema(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True