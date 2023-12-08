from pydantic import EmailStr, BaseModel

class CourseModel(BaseModel):
    course_name : str
    course_code : str = "PHY_101"

class GradeModel(BaseModel):
    student_matric_no : str
    percent_grade : float = 95.5
