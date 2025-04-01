from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from OCMSdb import get_db
import OCMSmodels

import os
from dotenv import load_dotenv
from datetime import datetime
from routers import courses, instructors, students, enrollments

app = FastAPI()

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")


app.include_router(courses.router, prefix="/courses", tags=["Courses"])
app.include_router(instructors.router, prefix="/instructors", tags=["Instructors"])
app.include_router(students.router, prefix="/students", tags=["Students"])
app.include_router(enrollments.router, prefix="/enrollments", tags=["Enrollments"])

@app.get("/")
def read_root():
    return {"message": "FastAPI"}


# @app.get("/fetch-instructor/{course_id}")
# def fetch_instructor(course_id: int, db: Session = Depends(get_db)):

#     course = db.query(OCMSmodels.Course).filter(OCMSmodels.Course.course_id == course_id).first()
#     if not course:
#         raise HTTPException(status_code=404, detail="Course not found")

#     reference =db.query(OCMSmodels.Reference).filter(OCMSmodels.Reference.course_id == course_id).all()
    
#     if not reference:
#         return {"message": "No instructors assigned to this course", "course_id":course_id}
    
#     instructor_ids = [ref.instructor_id for ref in reference]

#     return {"course_id":course_id, "instructors":instructor_ids}

# @app.get("/courses/all")
# def get_course(db: Session = Depends(get_db)):
#     return db.query(OCMSmodels.Course).all()


# @app.get("/instructors")
# def get_instructor(db: Session = Depends(get_db)):
#     return db.query(OCMSmodels.Instructor).all()


# @app.get("/students/all")
# def get_student(db: Session = Depends(get_db)):
#     return db.query(OCMSmodels.Student).all()

# @app.post("/create/courses")
# def create_course(course_data:OCMSmodels.Course_Create, db: Session = Depends(get_db)):
    
#     existing_instructors = db.query(OCMSmodels.Instructor).filter(OCMSmodels.Instructor.instructor_id.in_(course_data.instructor_ids)).all()
#     existing_instructor_ids = {instructor.instructor_id for instructor in existing_instructors}

#     missing_instructors = set(course_data.instructor_ids) - existing_instructor_ids
#     if missing_instructors:
#         db.rollback()
#         raise HTTPException(status_code=400, detail=f"Instructors {missing_instructors} not found")
    
#     course = OCMSmodels.Course(title=course_data.title,
#                                  description=course_data.description
#                                 )
    
#     db.add(course)
#     db.commit()
#     db.refresh(course)
    
#     try:
#         for instructor_id in existing_instructor_ids:
#             reference_entry = OCMSmodels.Reference(course_id=course.course_id, instructor_id=instructor_id)
#             db.add(reference_entry)

#         db.commit()
#     except IntegrityError:
#             db.rollback() 
#             raise HTTPException(status_code=500, detail="Database error: Failed to create instructor-course references")

#     return {
#         "message": "Course created successfully",
#         "course_id": course.course_id,
#         "instructor_ids": list(existing_instructor_ids)
# }

# @app.post("/instructors/register")
# def create_instructor(instructor_data:OCMSmodels.Instructor_Create,db: Session = Depends(get_db)):
#     instructor = OCMSmodels.Instructor(name=instructor_data.name,
#                                  email=instructor_data.email,
#                                  expertise=instructor_data.expertise)
#     db.add(instructor)
#     db.commit()
#     db.refresh(instructor)
#     return instructor

# @app.post("/students/joining", response_model=OCMSmodels.Enrollment_Create)
# def create_student(student_data:OCMSmodels.Student_Create,db: Session = Depends(get_db)):
#     student = OCMSmodels.Student(student_id=student_data.student_id,
#                                  name=student_data.name,
#                                  education=student_data.education,
#                                  email=student_data.email,
#                                  course_id=student_data.course_id)
#     db.add(student)
#     db.flush()
        
#     enrollment = OCMSmodels.Enrollment(student_id=student.student_id, course_id=student.course_id)
#     db.add(enrollment)
#     db.commit()
        
#     return {
#         "enrollment_id": enrollment.enrollment_id,
#         "enrollment_date": enrollment.enrollment_date
#         }
    
# @app.get("/enrollments/{student_id}", response_model=OCMSmodels.Enrollment_Create)
# def get_enrollment(student_id: int, db: Session = Depends(get_db)):
#     enrollment = db.query(OCMSmodels.Enrollment).filter_by(student_id=student_id).first()

#     if not enrollment:
#         raise HTTPException(status_code=404, detail="Enrollment not found")

#     return {
#         "enrollment_id": enrollment.enrollment_id,
#         "enrollment_date": enrollment.enrollment_date
#     }
