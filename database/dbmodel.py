from database.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String(8), nullable= False, unique=True)
    password = Column(String, nullable= False)
    user_type = Column(String(15), nullable= False)
    
    #relationship
    admin = relationship("Admin", back_populates= "owner")
    lecturers = relationship("Lecturers", back_populates= "owner")
    students = relationship("Students", back_populates= "owner")

class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(String, nullable= False)
    username = Column(String(50), nullable= False)
    designation = Column(String(50), nullable= False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    #relationship
    owner = relationship("User", back_populates="admin")

class Lecturers(Base):
    __tablename__ = 'lecturers'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable= False)
    last_name = Column(String(50), nullable= False)
    gender = Column(String(1), nullable= False, default="M")
    staff_no = Column(String, nullable= False)
    owner_id = Column(Integer, ForeignKey("users.id")) 
    
    #relationship
    owner = relationship("User", back_populates="lecturers")
    courses = relationship("Courses", back_populates= "owner")
    lec_grade = relationship("Grading", back_populates= "owner3")
    lec_course = relationship("Student_course", back_populates= "owner_3")

class Students(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable= False)
    last_name = Column(String(50), nullable= False)
    gender = Column(String(1), nullable= False, default="M")
    dob = Column(DateTime, nullable= False)
    origin = Column(String, nullable= True)
    matric_no= Column(String, nullable= False, unique=True)
    owner_id = Column(Integer, ForeignKey("users.id"), unique=True)
    
    #relationship
    owner = relationship("User", back_populates="students")
    stu_grade = relationship("Grading", back_populates= "owner1")
    stu_course = relationship("Student_course", back_populates= "owner_1")
    stu_finance = relationship("Finances", back_populates= "owner")

class Courses(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    course_title = Column(String(50), nullable= False)
    course_code = Column(String(20), nullable=False)
    lecturer = Column(Integer, ForeignKey("lecturers.id"))
    
    #relationship
    owner = relationship("Lecturers", back_populates="courses")
    cou_grade = relationship("Grading", back_populates= "owner2")
    cou_course = relationship("Student_course", back_populates= "owner_2")
    
class Grading(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    lecturer = Column(Integer, ForeignKey("lecturers.id"), nullable=False)
    student = Column(String, ForeignKey("students.id"), nullable=False)
    course = Column(String, ForeignKey("courses.id"), nullable=False)
    percent_grade = Column(Float, nullable= False)
    letter_grade = Column(String(2), nullable= False)
    grade_point = Column(Float, nullable= False)
    
    #relationship
    owner1 = relationship("Students", back_populates="stu_grade")
    owner2 = relationship("Courses", back_populates="cou_grade")
    owner3 = relationship("Lecturers", back_populates="lec_grade")

class Student_course(Base):
    __tablename__ = 'student_course'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    student = Column(Integer, ForeignKey("students.id"), nullable=False)
    courses = Column(Integer, ForeignKey("courses.id"), nullable=False)
    lecturer = Column(Integer, ForeignKey("lecturers.id"), nullable=False)
    status = Column(String(50), nullable= False, default="Registered")
    
    #relationship
    owner_1 = relationship("Students", back_populates="stu_course")
    owner_2 = relationship("Courses", back_populates="cou_course")
    owner_3 = relationship("Lecturers", back_populates="lec_course")

class Finances(Base):
    __tablename__ = 'finances'
    
    id = Column(Integer, unique=True, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    payment_status= Column(String, nullable= False, default="Unpaid")
    DateTime = Column(DateTime, nullable= False)
    
    #relationship
    owner = relationship("Students", back_populates="stu_finance")

