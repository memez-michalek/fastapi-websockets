from pydantic import BaseModel

class BaseUser(BaseModel):
    username :str
    email :str

class UserOut(BaseUser):
    ID: str
    

class UserIn(BaseUser):
    password :str

class DBIn(BaseUser):
    hashedpassword :str
