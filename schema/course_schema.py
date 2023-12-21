from pydantic import BaseModel

class CourseModel(BaseModel):
    course_title : str
    course_code : str = "PHY 101"
    
class Display(BaseModel):
    course_title : str
    course_code : str = "PHY 101"
    

class GradeModel(BaseModel):
    course_code : str
    student_matric_no : str
    percent_grade : float = 65.0
    
class CourseRegister(BaseModel):
    courses : str = "MTH 101"
