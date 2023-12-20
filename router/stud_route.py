from fastapi import APIRouter, Depends, HTTPException, status
from schema.user_schema import CreateStudent, EditUser, ShowUser, ShowCourses
from schema.course_schema import CourseRegister
from sqlalchemy.orm import Session
from service.utils import reusables_codes
from database.dbmodel import Students, Courses, Student_course, Grading, Lecturers
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
    find_course= db.query(Student_course).all()
    for row in find_course:
        if row.student == get_student.id:
            if row.courses == input.courses:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"COURSE ALREADY REGISTERED AS >>> {input.courses.upper()} : {get_lect.course_name.upper()} <<<")
    
    #saving if not previously registered.
    new_student = Student_course(
        **input.model_dump(), 
        student = get_student.id,
        lecturer = get_lect.lecturer_id,
        status = "Registered"
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return f"COURSE >> {input.courses} : {get_lect.course_name} << SUCCESSFULLY REGISTERED"
    
    
#VIEW REGISTERED COURSES BY STUDENT
@stud_app.get('/my_courses')
async def my_courses(db:Session=Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    
    #verify student's matric_no.
    get_student = db.query(Students).filter(Students.owner_id == user.id).first()
    
    #verify student's matric_no.
    view_course = db.query(Student_course).filter(Student_course.student == get_student.id)
    if not view_course.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="COURSE LIST IS EMPTY")
    
    return {
        "Message": f"Welcome {get_student.last_name}",
        "Registered Courses": view_course.all(),
    }
    
#VIEW COURSE DETAIL BY STUDENT
@stud_app.get('/course_detail')
async def check_course_detail(course_code: str, db:Session=Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    
    #verify course code.
    get_code = db.query(Courses).filter(Courses.course_code == course_code)
    
    if not get_code.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="INVALID INPUT or COURSE NOT YET CREATED")
    
    return {
        "Courses Lecturer": get_code.first()
    }
    
#VIEW LECTURERS DETAIL BY STUDENT
@stud_app.get('/my_lecturer_id')
async def check_lecturer_id(lecturer_id: int, db:Session=Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    
    #verify lecturers' id.
    get_lecturer = db.query(Lecturers).filter(Lecturers.id == lecturer_id)
    
    if not get_lecturer.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="INVALID LECTURER ID")
    
    return {
        "Courses Lecturer": get_lecturer.first()
    }
    
#VIEW GRADE OF COURSES TAKEN BY STUDENT
@stud_app.get('/results')
async def my_results(db:Session=Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    #get lecturers id of logged in lecturer
    get_userid  = db.query(Students).filter(Students.owner_id == user.id).first()
    if not get_userid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="USER IS NOT A SUTDENT!!!")       

    #get id of logged in student
    get_studentid = db.query(Grading).filter(Grading.student == get_userid.id)
    if not get_studentid.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NO RESULTS FOUND, TRY AGAIN LATER")    
    
    return {
        "message": f"Welcome {get_userid.last_name}", 
        "Result" : get_studentid.all()
    }
    
#VIEW CGPA BY STUDENT
@stud_app.get('/cgpa')
async def my_cgpa(db:Session=Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    
    #gverify id of logged in student
    get_userid  = db.query(Students).filter(Students.owner_id == user.id).first()
    if not get_userid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="USER IS NOT ON STUDENT LIST!!!")       

    #verify that all courses have been recorded
    ##get length of courses offered by students
    offered_courses = db.query(Student_course).filter(Student_course.student == get_userid.id)
    if not offered_courses.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NO RESULTS FOUND, TRY AGAIN LATER")    
    
    registered_c_length = len(offered_courses.all())
    print(registered_c_length)
    
    #get number of results published
    get_result = db.query(Grading).filter(Grading.student == get_userid.id)
    if not get_result.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NO RESULTS FOUND, TRY AGAIN LATER")    
    
    graded_c_length = len(get_result.all())
    print(graded_c_length)
    
    if graded_c_length < registered_c_length:
        raise HTTPException(status_code=status.HTTP_206_PARTIAL_CONTENT, detail="GRADING IS ONGOING, TRY LATER")    
    
    my_cgpa = 0
        
    for results in get_result.all():
        my_cgpa = my_cgpa + results.grade_point
    
    my_cgpa = my_cgpa/graded_c_length
    my_class =reusables_codes.convert_cgpa_to_class(my_cgpa)
    
    return {
        "message": f"Welcome {get_userid.last_name}", 
        "CGPA" : (my_cgpa),
        "class": my_class
    }

#DELETE A REGISTERED COURSE BY STUDENT
@stud_app.delete('/delete_my_course')
async def delete_my_courses(course_id: str, password: str, db:Session=Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    
    #password verification is needed to perform this action.
    if password != user.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "PASSWORD IS INCORRECT")
    
    #verify student's matric_no.
    get_student = db.query(Students).filter(Students.owner_id == user.id).first()
    
    #verify student's matric_no.
    view_course = db.query(Student_course).filter(Student_course.student == get_student.id)
    
    for data in view_course.all():
        if (data.courses == course_id) and (data.student == get_student.id) is True:
            db.delete(data)
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_202_ACCEPTED, 
                detail= f"COURSE {data.courses} DELETED SUCCESSFULLY"
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail= "COURSE NOT PREVIOUSLY REGISTERED"
    )

