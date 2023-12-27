from pydantic import BaseModel
from schema.user_schema import showCreateLect, showCreateStudent

class newCourse(BaseModel):
    course_title : str
    course_code : str = "PHY 101"

#displayable in new course register schema
class showNewCourse(newCourse):
    lecturer_info: showCreateLect
    class Config:
        orm_mode : True
    
class GradeModel(BaseModel):
    student_matric_no : str
    course_code : str
    percent_grade : float = 65.0

class showGradeModel(BaseModel):
    course_info : showNewCourse
    percent_grade:float
    letter_grade: str
    grade_point: float
    class Config:
        orm_mode : True

class showResultModel(BaseModel):
    student_info : showCreateStudent
    percent_grade:float
    letter_grade: str
    grade_point: float
    class Config:
        orm_mode : True

class registerCourse(BaseModel):
    courses : str = "MTH 101"

class showregisterCourse(BaseModel):
    course_info: showNewCourse
    status: str
    class Config:
        orm_mode = True
        
class showregisterStudents(BaseModel):
    student_info : showCreateStudent
    status: str
    class Config:
        orm_mode = True

