from jose import jwt
from fastapi import HTTPException, status
from database.dbmodel import User
from database.database import sessionLocal
from typing import Generator
from core.config import setting


class reusables_codes:
    #this block of codes recieves an encoded token(which carries some relevant data like email address of the user),
    # decodes it, then returns the username/email address.
    #Afterwards, it performs some validation with the decoded email against the email address on the database
    
    def get_user_from_token(db, token):
        try:
            payload = jwt.decode(token, setting.SECRET_KEY, algorithms =[setting.ALGORITHM])
            username:str = payload.get("sub") #"sub" is a field holding the username/email address
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Invalid Email credentials")
            
            #Querry the sub(email) from to token against the stored email
            user = db.query(User).filter(User.email==username).first()
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="User is not authorized")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Unable to verify credentials")
        
        #if successful, return the user as authenticated, for further processing.
        return user
    
    
    @staticmethod
    def get_db() -> Generator:
        try:
            db = sessionLocal()
            yield db
        finally:
            db.close()
    
    @staticmethod
    def gen_matric_no(id):
        
        matric_no = ''.join(f"{setting.matric_no}{1000+id}")
        return matric_no
    
    @staticmethod
    def gen_staff_id(id):
        
        staff_no = ''.join(f"{setting.staff_initials}{500+id}")
        return staff_no
    
    @staticmethod
    def get_letter_grade(percent_grade):
        if percent_grade >= 90:
            return 'A'
        elif percent_grade < 90 and percent_grade >= 80:
            return 'B'
        elif percent_grade < 80 and percent_grade >= 70:
            return 'C'
        elif percent_grade < 70 and percent_grade >= 60:
            return 'D'
        elif percent_grade < 60 and percent_grade >= 50:
            return 'E'
        else:
            return 'F'
        
    def convert_grade_to_gpa(letter_grade):
        if letter_grade == 'A':
            return 4.0
        elif letter_grade == 'B':
            return 3.3
        elif letter_grade == 'C':
            return 2.3
        elif letter_grade == 'D':
            return 1.3
        else:
            return 0