from database.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    firstname = Column(String(50), nullable= False)
    firstname = Column(String(50), nullable= False)
    email = Column(String(50), nullable= False, unique=True)
    password = Column(String, nullable= False)
    user_type = Column(String(20), nullable= False)
    
    user_admin = relationship("Admin", back_populates= "admin_user")
    user_lect = relationship("Lecturers", back_populates="user")
    user_stud = relationship("Students", back_populates="user")


class Admin(Base):
    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    #relations:
    admin_user = relationship("User", back_populates="user_admin")


class Lecturers(Base):
    __tablename__ = 'lecturers'
    
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    courses = Column(String, nullable= False)
    #relations:
    user = relationship("User", back_populates="user_lect")
    teacher_conn = relationship("Courses", back_populates="teacher_owner")
    
class Students(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    matric_no= Column(String, nullable= False, unique=True)
    #relations:
    user = relationship("User", back_populates="user_stud")
    Student_owner = relationship("Student_course", back_populates="students")
    
class Student_course(Base):
    __tablename__ = 'student_course'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    student_id= Column(Integer, ForeignKey("students.id"))
    courses_id= Column(Integer, ForeignKey("courses.id"))
    #relations:
    courses = relationship("Courses", back_populates="courses_owner")
    students = relationship("Students", back_populates="Student_owner")

class Courses(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    course_name = Column(String(100), nullable= False)
    course_code = Column(String(20))
    teacher = Column(Integer, ForeignKey("lecturers.id"))
    
    # courses_details = relationship("Admin", back_populates="admin_id")
    courses_owner = relationship("Courses", back_populates="user_stud")
    teacher_owner = relationship("Lecturers", back_populates="teacher_conn")

    
class Finances(Base):
    __tablename__ = 'finances'
    
    id = Column(Integer, unique=True, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    payment_status= Column(String, nullable= False, default="Unpaid")


