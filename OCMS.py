from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from OCMSdb import get_db
from pydantic import BaseModel
import OCMSmodels
from OCMSmodels import Enrollment
app = FastAPI()
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
print("Secret Key:", SECRET_KEY)

@app.get("/")
def read_root():
    return {"message": "FastAPI"}


class Course_Create(BaseModel):
    course_id:int
    title:str
    description:str
    instructor_id:int

class Instructor_Create(BaseModel):
    instructor_id:int
    name:str
    email:str
    expertise:str

class Student_Create(BaseModel):
    student_id:int
    name:str
    education:str
    email:str
    course_id:int

class Enrollment_Create(BaseModel):
    enrollment_id:int
    enrollment_date:datetime

@app.get("/courses/all")
def get_course(db: Session = Depends(get_db)):
    return db.query(OCMSmodels.Course).all()


@app.get("/instructors")
def get_instructor(db: Session = Depends(get_db)):
    return db.query(OCMSmodels.Instructor).all()


@app.get("/students/all")
def get_student(db: Session = Depends(get_db)):
    return db.query(OCMSmodels.Student).all()

@app.post("/create/courses")
def create_course(course_data:Course_Create,db: Session = Depends(get_db)):
    course = OCMSmodels.Course(course_id=course_data.course_id,
                                 title=course_data.title,
                                 description=course_data.description,
                                 instructor_id=course_data.instructor_id)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

@app.post("/instructors/register")
def create_instructor(instructor_data:Instructor_Create,db: Session = Depends(get_db)):
    instructor = OCMSmodels.Instructor(instructor_id=instructor_data.instructor_id,
                                 name=instructor_data.name,
                                 email=instructor_data.email,
                                 expertise=instructor_data.expertise)
    db.add(instructor)
    db.commit()
    db.refresh(instructor)
    return instructor

@app.post("/students/joining", response_model=Enrollment_Create)
def create_student(student_data:Student_Create,db: Session = Depends(get_db)):
    student = OCMSmodels.Student(student_id=student_data.student_id,
                                 name=student_data.name,
                                 education=student_data.education,
                                 email=student_data.email,
                                 course_id=student_data.course_id)
    db.add(student)
    db.flush()
        
    enrollment = OCMSmodels.Enrollment(student_id=student.student_id, course_id=student.course_id)
    db.add(enrollment)
    db.commit()
        
    return {
        "enrollment_id": enrollment.enrollment_id,
        "enrollment_date": enrollment.enrollment_date
        }
    
@app.get("/enrollments/{student_id}", response_model=Enrollment_Create)
def get_enrollment(student_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(Enrollment).filter_by(student_id=student_id).first()

    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    return {
        "enrollment_id": enrollment.enrollment_id,
        "enrollment_date": enrollment.enrollment_date
    }
