from fastapi import APIRouter, Depends, HTTPException, status
from schema.user_schema import CreateLect, showCreateLect
from schema.course_schema import newCourse, showNewCourse, GradeModel, showregisterStudents,showResultModel
from sqlalchemy.orm import Session
from service.utils import reusables_codes
from database.dbmodel import Lecturers, Courses, Grading, Students, Student_course
from router.auth_route import oauth2_scheme


#access the fastapi attributes
lect_app = APIRouter()

#STAFF REGISTRATION ROUTE
@lect_app.post('/register', response_model=showCreateLect, status_code=201)
async def register_staff(profile: CreateLect, db:Session=Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    
    #authentication
    if user.user_type != "staff":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"ACCESS_DENIED!!! ONLY STAFF CAN REGISTER HERE")
    
    #checking if staff is already registered
    get_staff = db.query(Lecturers).filter(user.id == Lecturers.owner_id).first()
    
    get_staff_all = db.query(Lecturers).all()
    
    if not get_staff:    
        new_staff = Lecturers(
            **profile.model_dump(), 
            staff_no = reusables_codes.gen_staff_id(len(get_staff_all)+ 1), 
            owner_id = user.id
        )
        
        db.add(new_staff)
        db.commit()
        db.refresh(new_staff)
        return new_staff
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"ALREADY REGISTERED WITH STAFF NUMBER >>> {get_staff.staff_no.upper()} <<<")

#REGISTER NEW COURSE BY COURSE LECTURER
@lect_app.post('/create_course', response_model=showNewCourse, status_code=201)
async def add_new_course(input: newCourse, db:Session=Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    
    #authentication
    if user.user_type != "staff":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"ACCESS_DENIED!!! ONLY STAFF CAN REGISTER COURSE")
    
    #checking if course is already registered
    get_course = db.query(Courses).filter(Courses.course_code == input.course_code)
    
    #getting lecturer information or id
    get_lecturer = db.query(Lecturers).filter(Lecturers.owner_id == user.id).first()
    if not get_lecturer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"STAFF INFORMATION NOT FOUND, KINDLY COMPLETE YOUR PROFILE")
    
    if not get_course.first():    
        new_course = Courses(
            **input.model_dump(), 
            lecturer = get_lecturer.id
        )
        
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
        return new_course
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail=f"COURSE ALREADY REGISTERED AS >>> {input.course_code.upper()} <<<")


#GRADE A STUDENT BY COURSE LECTURER
@lect_app.post('/grade_students', response_model=showResultModel, status_code=202)
async def grade_students(input:GradeModel, db:Session=Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    
    if input.percent_grade > 100:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="GRADE CANNOT EXCEED 100 %")

    #Check if the students matric number exists.
    get_student =  db.query(Students).filter(Students.matric_no == input.student_matric_no).first()
    if not get_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"MATRIC_NUMBER INCORRECT OR UNREGISTERED!!!")
    
    #get signed in user.
    get_lecturer = db.query(Lecturers).filter(Lecturers.owner_id == user.id).first()
    if not get_lecturer:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="DENIED!!! KINDLY REGISTER AS A LECTURER.")
    
    #checking if course lecturer is grading his/her course.
    get_course = db.query(Courses).filter(Courses.course_code == input.course_code).first()
    if not get_course:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="COURSE-CODE IS INCORRECT OR UNREGISTERED, TRY LATER")
    
    if get_course.lecturer != get_lecturer.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"ACCESS_DENIED!!! YOU ARE NOT THE COURSE LECTURER")
    
    #checking if course is already graded by authenticated lecturer
    get_student_grade = db.query(Grading).filter(Grading.student == get_student.id, Grading.course == get_course.id)
    for row in get_student_grade:
        if get_student_grade:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail = f"MATRIC NO.:{get_student.matric_no.upper()} ALREADY GRADED WITH {row.percent_grade}% IN {get_course.course_code}"
                )
        
    #Check if the students is taking the course.
    get_reg_student = db.query(Student_course).filter(Student_course.student == get_student.id, Student_course.courses == get_course.id)
        
    if get_reg_student.first():
        new_course = Grading(
            course = get_course.id,
            student = get_student.id,
            percent_grade = input.percent_grade,
            letter_grade = reusables_codes.get_letter_grade(input.percent_grade), 
            lecturer = get_lecturer.id, 
            grade_point = reusables_codes.convert_grade_to_gpa(reusables_codes.get_letter_grade(input.percent_grade))
        )
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
        return new_course
    
    raise HTTPException (
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"STUDENT DID NOT REGISTER FOR THIS COURSE"
    )


#VIEW MY COURSES BY LECTURER
@lect_app.get('/my_courses', response_model= list[newCourse], status_code= 202)
async def my_courses(db:Session=Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    
    #verify logged-in user.
    get_staff = db.query(Lecturers).filter(Lecturers.owner_id == user.id).first()
    if not get_staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="ONLY LECTURERS ARE ALLOWED")

    #verify student's matric_no.
    view_course = db.query(Courses).filter(Courses.lecturer == get_staff.id)
    if not view_course.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="LIST IS EMPTY, KINDLY REGISTER A COURSE")
    
    return  view_course.all()


#SEE STUDENTS TAKING A COURSE BY COURSE LECTURER
@lect_app.get('/my_students', response_model= list[showregisterStudents], status_code=202)
async def my_students(course_code: str, db:Session=Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    #get lecturers id of logged-in USER
    get_userid  = db.query(Lecturers).filter(Lecturers.owner_id == user.id).first()
    if not get_userid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED, YOU ARE NOT A LECTURER!") 
    
    #CONVERT course code to course id
    check_course_code = db.query(Courses).filter(Courses.course_code == course_code).first()
    if not check_course_code:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="COURSE CODE IS INCORRECT OR UNPUBLISHED, TRY AGAIN")      
    
    #get id of logged in lecturer
    get_lectid = db.query(Student_course).filter(Student_course.lecturer == get_userid.id, Student_course.courses == check_course_code.id)
    if not get_lectid.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"NO STUDENT RECORD FOUND FOR {check_course_code.course_title}")      

    return get_lectid.all()


#VIEW MY STUDENT RESULT AND GRADE B LECTURER
@lect_app.get('/student_result', response_model=list[showResultModel], status_code=202)
async def my_student_result(course_code:str, db:Session=Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    
    #verify logged-in user and retreive staff id.
    get_staff = db.query(Lecturers).filter(Lecturers.owner_id == user.id).first()
    if not get_staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="ONLY LECTURERS ARE ALLOWED")

    #CONVERT course code to course id
    check_course_code = db.query(Courses).filter(Courses.course_code == course_code).first()
    if not check_course_code:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="COURSE CODE IS INCORRECT OR UNPUBLISHED, TRY AGAIN")      

    #get student record by filtering course id and lecturer id
    results = db.query(Grading).filter(Grading.course == check_course_code.id, Grading.lecturer == get_staff.id)
    if not results.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NO RESULTS FOUND, TRY AGAIN LATER")    
    
    return results.all()

#EDIT COURSE BY LECTURER
@lect_app.put('/edit_course_detail', response_model=list[showregisterStudents], status_code=202)
async def edit_my_course(course_id:int, input:newCourse, db:Session=Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    
    #verify logged-in user.
    get_staff = db.query(Lecturers).filter(Lecturers.owner_id == user.id).first()
    if not get_staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="ONLY LECTURERS ARE ALLOWED")

    modify_course = db.query(Courses).filter(Courses.id == course_id)
    if not modify_course.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND, KINDLY ADD COURSE"
        )

    if modify_course.first().lecturer != get_staff.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='ONLY COURSE OWNER CAN MODIFY'
        )
    
    modify_course.update(input.model_dump())
    db.commit()
    raise HTTPException(
        status_code=status.HTTP_202_ACCEPTED,
        detail='Course Information updated successfully'
    )
    

