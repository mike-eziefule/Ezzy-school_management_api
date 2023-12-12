from pydantic import EmailStr, BaseModel
from datetime import date


class Auth(BaseModel):
    email : EmailStr
    password : str
    
# class Credentials(Auth):
#     retype_password : str
#     user_type: str = "admin/staff/student"
    
class Base(BaseModel):
    first_name: str
    last_name: str
    gender: str = "M/F"

class CreateUser(Auth):
    retype_password : str
    user_type: str = "admin/staff/student"
    
class CreateStudent(Base):
    dob: date
    origin: str

class CreateAdmin(BaseModel):
    username: str
    designation: str

class CreateLect(Base):
    pass

class EditUser(BaseModel):
    firstname: str
    lastname: str
    
class ShowUser(CreateUser):
    id : int
    class Config:
        orm_mode = True

class ShowCourses(BaseModel):
    student : str
    courses: str
    lecturer : list[str] = []
    status: str
    class Config:
        orm_mode = True