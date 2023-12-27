from fastapi import APIRouter, Depends, HTTPException, status
from schema.user_schema import showUserSignup, UserBase
from sqlalchemy.orm import Session
from service.utils import reusables_codes
from database.dbmodel import User

#access the fastapi attributes
user_app = APIRouter()

#STUDENT SIGNUP ROUTE
@user_app.post('/student_signup', response_model=showUserSignup, status_code=201)
async def student_signup(input:UserBase, db:Session=Depends(reusables_codes.get_db)):

    #checking if user is already registered
    get_users = db.query(User).filter(User.email == input.email)
    if get_users.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="E-MAIL TAKEN!!!")
    #checking if re-entered password matches
    if input.password != input.retype_password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="PASSWORD MISMATCH!!!")
    
    new_student = User(
        email = input.email, 
        password = input.password,
        user_type = "student" 
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


#STAFF SIGNUP ROUTE
@user_app.post('/staff_signup', response_model=showUserSignup, status_code=201)
async def staff_signup(input:UserBase, db:Session=Depends(reusables_codes.get_db)):

    #checking if user is already registered
    get_users = db.query(User).filter(User.email == input.email)
    if get_users.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="E-MAIL TAKEN!!!")
    #checking if re-entered password matches
    if input.password != input.retype_password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="PASSWORD MISMATCH!!!")
    
    new_staff = User(
        email = input.email, 
        password = input.password,
        user_type = "staff"
    )
    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)
    return new_staff

#ADMIN SIGNUP ROUTE
@user_app.post('/admin_signup', response_model=showUserSignup, status_code=201)
async def admin_signup(input:UserBase, db:Session=Depends(reusables_codes.get_db)):

    #checking if user is already registered
    get_users = db.query(User).filter(User.email == input.email)
    if get_users.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="E-MAIL TAKEN!!!")
    #checking if re-entered password matches
    if input.password != input.retype_password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="PASSWORD MISMATCH!!!")
        
    new_admin = User(
        email = input.email, 
        password = input.password,
        user_type = "admin" 
    )
    
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin