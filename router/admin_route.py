from fastapi import APIRouter, Depends, HTTPException, status
from schema.user_schema import CreateAdmin, showAdmin, showCreateLect, showCreateStudent
from schema.course_schema import showResultModel, showNewCourse
from sqlalchemy.orm import Session
from service.utils import reusables_codes
from database.dbmodel import Admin, Lecturers, Students, Courses, Grading
from router.auth_route import oauth2_scheme


#access the fastapi attributes
adm_app = APIRouter()

#STAFF REGISTRATION ROUTE
@adm_app.post('/register', response_model=showAdmin, status_code= 201)

async def register_admin(profile:CreateAdmin, db:Session=Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    
    #authentication
    if user.user_type != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f"ACCESS_DENIED!!! ONLY ADMINS CAN REGISTER HERE"
        )
    
    #checking if admin is already registered
    get_admin = db.query(Admin).filter(user.id == Admin.owner_id)
    
    #get length of admin users
    get_admin_all = len(db.query(Admin).all())
    
    if not get_admin.first():    
        new_admin = Admin(
            **profile.model_dump(), 
            public_id = reusables_codes.gen_admin_id(get_admin_all + 1), 
            owner_id = user.id
        )
        
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return new_admin
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail=f"ALREADY REGISTERED AS >>> {user.user_type.upper()} <<<"
    )
    

#SEE ALL PROVISIONAL COURSES BY ADMIN
@adm_app.get('/all_courses', response_model= list[showNewCourse], status_code=202)
async def all_courses(db:Session=Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    
    #authentication
    if user.user_type != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f"ACCESS_DENIED!!! ONLY ADMINS CAN REGISTER HERE"
        )
    
    #checking if admin is already registered
    get_admin = db.query(Admin).filter(user.id == Admin.owner_id)
    if not get_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Unknown Administrator, Kindly Register your Account"
        )
    
    #get all students
    all_courses = db.query(Courses).all()
    if not all_courses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"NO STUDENT RECORD FOUND")      
    return all_courses

#SEE ALL STUDENTS ADMIN
@adm_app.get('/all_students', response_model= list[showCreateStudent], status_code=202)
async def all_students(db:Session=Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    
    #authentication
    if user.user_type != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f"ACCESS_DENIED!!! ONLY ADMINS CAN REGISTER HERE"
        )
    
    #checking if admin is already registered
    get_admin = db.query(Admin).filter(user.id == Admin.owner_id)
    if not get_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Unknown Administrator, Kindly Register your Account"
        )
    
    #get all students
    all_students = db.query(Students).all()
    if not all_students:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"NO STUDENT RECORD FOUND")      
    return all_students


#SEE ALL STAFF BY ADMIN
@adm_app.get('/view_all_staff', response_model= list[showCreateLect], status_code=202)
async def all_staff(db:Session=Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    
    #authentication
    if user.user_type != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f"ACCESS_DENIED!!! ONLY ADMINS CAN REGISTER HERE"
        )
    
    #checking if admin is already registered
    get_admin = db.query(Admin).filter(user.id == Admin.owner_id)
    if not get_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Unknown Administrator, Kindly Register your Account"
        )
    
    #get all staff
    all_staff = db.query(Lecturers).all()
    if not all_students:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"NO LECTURER RECORD FOUND")      
    return all_staff

#VIEW LECTURERS DETAIL BY ADMIN
@adm_app.get('/view_lecturer_info', response_model= showCreateLect, status_code=202)
async def check_staff_no(staff_no: str = "EZ-S501", db:Session=Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    
    #authentication
    if user.user_type != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f"ACCESS_DENIED!!! ONLY ADMINS CAN ACCESS HERE"
        )
    
    get_admin = db.query(Admin).filter(Admin.owner_id == user.id).first()
    if not get_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Unknown Administrator, Kindly Register your Account"
        )
    
    #verify lecturers' staff_no.
    get_lecturer = db.query(Lecturers).filter(Lecturers.staff_no == staff_no)
    
    if not get_lecturer.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="NO RECORD OR INVALID LECTURER ID ENTERED")
    
    return get_lecturer.first()


#Views students performance.
@adm_app.get('/view_student_result', response_model= list[showResultModel], status_code=202)
async def view_student_result(
    matric_no: str,
    db:Session=Depends(reusables_codes.get_db), 
    token:str=Depends(oauth2_scheme)
):

    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    
    #authentication
    if user.user_type != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f"ACCESS_DENIED!!! ONLY ADMINS CAN ACCESS HERE"
        )

    get_admin = db.query(Admin).filter(Admin.owner_id == user.id).first()
    if not get_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Unknown Administrator, Kindly Register your Account"
        )
    
    #match mat_no with student id   
    get_student = db.query(Students).filter(Students.matric_no == matric_no).first()
    if not get_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Not found or Incorrect Matric Number"
        )
        
    get_student_result = db.query(Grading).filter(Grading.student == get_student.id).all()
    return get_student_result


#EDIT GRADE BY ADMIN ONLY
@adm_app.put('/edit_result', response_model= showResultModel, status_code=202)
async def edit_student_result(
    matric_no: str,
    course_code: str,
    new_grade: float,
    db:Session=Depends(reusables_codes.get_db), 
    token:str=Depends(oauth2_scheme)
):

    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    
    #authentication
    if user.user_type != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f"ACCESS_DENIED!!! ONLY ADMINS CAN ACCESS HERE"
        )
        
    get_admin = db.query(Admin).filter(Admin.owner_id == user.id).first()
    if not get_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Unknown Administrator, Kindly Register your Account"
        )
    
    #match mat_no with student id   
    get_student = db.query(Students).filter(Students.matric_no == matric_no).first()
    if not get_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Not found or Incorrect Matric Number"
        )
    #match entered course code with course id
    get_course = db.query(Courses).filter(Courses.course_code == course_code).first()
    if not get_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Not found or Incorrect Course Code"
        )
    
    get_grade = db.query(Grading).filter(Grading.student == get_student.id, Grading.course == get_course.id)
    if not get_grade.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No Previous Result Found"
        )
    
    get_grade.update(
        {
            'percent_grade' : new_grade,
            'letter_grade' : reusables_codes.get_letter_grade(new_grade),
            'grade_point' : reusables_codes.convert_grade_to_gpa(reusables_codes.get_letter_grade(new_grade))
        }, synchronize_session='fetch'
    )
    db.commit()
    raise HTTPException(
        status_code=status.HTTP_202_ACCEPTED,
        detail='Course Information updated successfully'
    )