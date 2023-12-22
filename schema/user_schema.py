from pydantic import EmailStr, BaseModel
from datetime import date

class User(BaseModel):
    email : EmailStr
    password : str
    
#signup user schema
class UserSignup(User):
    retype_password : str
    user_type: str = "input: admin or staff or student"

#displayable in signup user schema
class showUserSignup(BaseModel):
    id : int
    email : EmailStr
    user_type: str    
    class Config:
        orm_mode = True


class BaseUser(BaseModel):
    first_name: str
    last_name: str
    gender: str = "male"


#create user profile schema
class CreateStudent(BaseUser):
    dob: date
    origin: str
    
#displayable in create student profile schema
class showCreateStudent(CreateStudent):
    matric_no: str
    owner : showUserSignup
    class Config:
        orm_mode = True


#create admin profile schema
class CreateAdmin(BaseModel):
    username: str
    designation: str
    
#displayable in create admin profile schema
class showAdmin(CreateAdmin):
    id: str
    public_id: str
    owner : showUserSignup
    class Config:
        orm_mode = True


#create staff profile schema
class CreateLect(BaseUser):
    pass

#displayable in create staff profile schema
class showCreateLect(CreateLect):
    staff_no: str
    owner : showUserSignup
    class Config:
        orm_mode = True