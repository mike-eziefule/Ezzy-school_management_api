from pydantic import EmailStr, BaseModel

class CourseModel(BaseModel):
    course_name : str
    course_code : str = "PHY 101"

class GradeModel(BaseModel):
    course_code : str
    student_matric_no : str
    percent_grade : float = 95.5
    
class CourseRegister(BaseModel):
    courses : str = "MTH 101"
