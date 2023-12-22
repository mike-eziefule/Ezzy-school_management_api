from fastapi import APIRouter, Depends, HTTPException, status
from schema.user_schema import CreateAdmin, showAdmin
from sqlalchemy.orm import Session
from service.utils import reusables_codes
from database.dbmodel import Admin
from router.auth_route import oauth2_scheme


#access the fastapi attributes
adm_app = APIRouter()

#STAFF REGISTRATION ROUTE
@adm_app.post('/register',response_model=showAdmin, status_code= 201)  #

async def register_admin(profile: CreateAdmin, db:Session=Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    
    #authentication
    if user.user_type != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"ACCESS_DENIED!!! ONLY ADMINS CAN REGISTER HERE")
    
    #checking if student is already registered
    get_admin = db.query(Admin).filter(user.id == Admin.owner_id)
    
    if not get_admin.first():    
        new_admin = Admin(**profile.model_dump(), public_id = reusables_codes.gen_staff_id(user.id), owner_id = user.id)
        
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return new_admin
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"ALREADY REGISTERED AS >>> {user.user_type.upper()} <<<")