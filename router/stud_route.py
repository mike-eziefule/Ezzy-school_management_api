from fastapi import APIRouter, Depends, HTTPException, status
from schema.user_schema import CreateAdmin, CreateStudent, EditUser, ShowUser
from sqlalchemy.orm import Session
from service.utils import reusables_codes
from database.dbmodel import User, Students
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
    get_student = db.query(Students).filter(user.id == Students.owner_id)
    
    if not get_student.first():    
        new_student = Students(**profile.model_dump(), matric_no = reusables_codes.gen_matric_no(user.id), owner_id = user.id)
        
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
    
        return new_student
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"ALREADY REGISTERED AS >>> {user.user_type.upper()} <<<")

