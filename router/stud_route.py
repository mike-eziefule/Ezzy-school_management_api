from fastapi import APIRouter, Depends, HTTPException, status
from schema.user_schema import CreateAdmin, CreateStudent, EditUser, ShowUser
from schema.course_schema import CourseRegister
from sqlalchemy.orm import Session
from service.utils import reusables_codes
from database.dbmodel import User, Students, Courses, Student_course, Lecturers
from router.auth_route import oauth2_scheme



#access the fastapi attributes
stud_app = APIRouter()

#STUDENT REGISTRATION ROUTE
@stud_app.post('/register')  #response_model = ShowUser
async def register_student(profile: CreateStudent, db:Session=Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    if user.user_type != "student":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"ACCESS_DENIED!!! ONLY STUDENTS CAN REGISTER HERE")
    
    #checking if student is already registered
    get_student = db.query(Students).filter(user.id == Students.owner_id).first()
    get_all_student = db.query(Students).all()
    
    if not get_student:    
        new_student = Students(
            **profile.model_dump(), 
            matric_no = reusables_codes.gen_matric_no(len(get_all_student) + 1), 
            owner_id = user.id)
        
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
    
        return new_student
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"ALREADY REGISTERED AS >>> {get_student.matric_no.upper()} <<<")


#REGISTER FOR A COURSE BY STUDENT
@stud_app.post('/course_registration')
async def new_course(input: CourseRegister, db:Session=Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    
    #authentication
    if user.user_type != "student":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"ACCESS_DENIED!!! ONLY STUDENTS CAN REGISTER FOR A COURSE")
    
    #finding course Lecturer
    get_lect = db.query(Courses).filter(Courses.course_code == input.courses).first()
    if not get_lect:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"COURSE DOES NOT EXIST YET, TRY LATER.")
    
    #finding students matric_no.
    get_student = db.query(Students).filter(Students.owner_id == user.id).first()
    if not get_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"STUDENT DATA NOT FOUND, KINDLY REGISTER.")
    
    #checking if course is already registered by authenticated student
    get_matno = db.query(Student_course).all()
    for row in get_matno:
        if row.student == get_student.matric_no:
            if row.courses == input.courses:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"COURSE ALREADY REGISTERED AS >>> {input.courses.upper()} : {get_lect.course_name.upper()} <<<")
    
    #saving if not previously registered.
    new_student = Student_course(
        **input.model_dump(), 
        student = get_student.matric_no,
        lecturer = get_lect.lecturer_id,
        status = "Registered",
    )
        
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return f"COURSE >> {input.courses} : {get_lect.course_name} << SUCCESSFULLY REGISTERED"
    
