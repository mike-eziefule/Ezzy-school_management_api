from fastapi import APIRouter, Depends, HTTPException, status
from schema.user_schema import CreateLect, EditUser, ShowUser
from schema.course_schema import CourseModel, GradeModel
from sqlalchemy.orm import Session
from service.utils import reusables_codes
from database.dbmodel import Lecturers, Courses, Grading
from router.auth_route import oauth2_scheme


#access the fastapi attributes
lect_app = APIRouter()

#STAFF REGISTRATION ROUTE
@lect_app.post('/register')  #response_model = ShowUser
async def register_staff(profile: CreateLect, db:Session=Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    
    #authentication
    if user.user_type != "staff":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"ACCESS_DENIED!!! ONLY STAFF CAN REGISTER HERE")
    
    #checking if student is already registered
    get_staff = db.query(Lecturers).filter(user.id == Lecturers.owner_id)
    
    if not get_staff.first():    
        new_staff = Lecturers(**profile.model_dump(), staff_no = reusables_codes.gen_staff_id(user.id), owner_id = user.id)
        
        db.add(new_staff)
        db.commit()
        db.refresh(new_staff)
        return new_staff
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"ALREADY REGISTERED AS >>> {user.user_type.upper()} <<<")

#REGISTER NEW COURSE BY COURSE LECTURER
@lect_app.post('/add_course')
async def new_course(input: CourseModel, db:Session=Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    
    #authentication
    if user.user_type != "staff":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"ACCESS_DENIED!!! ONLY STAFF CAN REGISTER COURSE")
    
    #checking if course is already registered
    get_course = db.query(Courses).filter(Courses.course_code == input.course_code)
    
    if not get_course.first():    
        new_course = Courses(**input.model_dump(), lecturer_id = user.id)
        
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
        return new_course
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"COURSE ALREADY REGISTERED AS >>> {input.course_code.upper()} <<<")


#GRADE A STUDENT BY COURSE LECTURER
@lect_app.post('/grade_students')
async def grade_students(input: GradeModel, db:Session=Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    
    #authentication
    if user.user_type != "staff":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"ACCESS_DENIED!!! ONLY STAFF CAN REGISTER COURSE")
    
    #checking if course is already graded
    get_grade = db.query(Grading).filter(Grading.student_matric_no == input.student_matric_no)
    
    #checking if course lecturer status is true
    get_course = db.query(Courses).filter(Courses.lecturer_id == user.id).first()
    if not get_course:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"ACCESS_DENIED!!! ONLY COURSE LECTURER CAN GRADE STUDENT")
    
    if not get_grade.first():    
        new_course = Grading(**input.model_dump(), letter_grade = "A", course_code = get_course, lecturer_id = user.id)
        
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
        return new_course
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"GRADE ALREADY REGISTERED FOR >>> {input.student_matric_no.upper()} <<<")
