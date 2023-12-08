from fastapi import APIRouter, Depends, HTTPException, status
from schema.user_schema import CreateUser
from sqlalchemy.orm import Session
from service.utils import reusables_codes
from database.dbmodel import User

#access the fastapi attributes
user_app = APIRouter()

#CREATE PROFILE ROUTE
@user_app.post('/signup')
async def signup(input:CreateUser, db:Session=Depends(reusables_codes.get_db)):

    #checking if user is already registered
    get_users = db.query(User).filter(User.email == input.email)
    if get_users.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="E-MAIL TAKEN!!!")
    #checking if re-entered password matches
    if input.password != input.retype_password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="PASSWORD MISMATCH!!!")
    
    new_user = User(email = input.email, 
                    password = input.password, 
                    user_type = input.user_type)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user