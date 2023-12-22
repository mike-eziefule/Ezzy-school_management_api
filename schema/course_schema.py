from pydantic import BaseModel
from schema.user_schema import showCreateLect, showCreateStudent

class newCourse(BaseModel):
    course_title : str
    course_code : str = "PHY 101"

#displayable in new course register schema
class showNewCourse(newCourse):
    owner: showCreateLect
    class Config:
        orm_mode : True
    
class GradeModel(BaseModel):
    student_matric_no : str
    course_code : str
    percent_grade : float = 65.0

class showGradeModel(BaseModel):
    owner2 : showNewCourse
    percent_grade:float
    letter_grade: str
    grade_point: float
    class Config:
        orm_mode : True


class registerCourse(BaseModel):
    courses : str = "MTH 101"

class showregisterCourse(BaseModel):
    # owner_1 : showCreateStudent
    owner_2: showNewCourse
    status: str
    class Config:
        orm_mode = True

