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
        if percent_grade >= 70:
            return 'A'
        elif percent_grade >= 60 and percent_grade < 70:
            return 'B'
        elif percent_grade >= 50 and percent_grade < 60:
            return 'C'
        elif percent_grade >= 45 and percent_grade < 50:
            return 'D'
        elif percent_grade >=40 and percent_grade < 45:
            return 'E'
        else:
            return 'F'
        
    def convert_grade_to_gpa(letter_grade):
        if letter_grade == 'A':
            return 5.0
        elif letter_grade == 'B':
            return 4.0
        elif letter_grade == 'C':
            return 3.0
        elif letter_grade == 'D':
            return 2.0
        elif letter_grade == 'E':
            return 1.0
        else:
            return 0
    
    def convert_cgpa_to_class(cgpa):
        if cgpa >= 4.5 and cgpa <= 5.0:
            return "FIRST CLASS"
        elif cgpa >= 3.5 and cgpa < 4.5:
            return "SECOND CLASS UPPER" 
        elif cgpa >= 2.5 and cgpa < 3.5:
            return "SECOND CLASS LOWER"
        elif cgpa >= 1.5 and cgpa < 2.5:
            return "THIRD CLASS"
        else:
            return "PASS"