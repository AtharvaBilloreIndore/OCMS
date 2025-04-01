from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from OCMSdb import get_db
from OCMSmodels import Student, Student_Create, Enrollment, Enrollment_Create

router = APIRouter()

@router.get("", summary="List all students")
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@router.post("/joining",response_model=Enrollment_Create, summary="Register student")
def create_student(student_data:Student_Create,db: Session = Depends(get_db)):
    student = Student(student_id=student_data.student_id,
                                 name=student_data.name,
                                 education=student_data.education,
                                 email=student_data.email,
                                 course_id=student_data.course_id)
    db.add(student)
    db.flush()
        
    enrollment = Enrollment(student_id=student.student_id, course_id=student.course_id)
    db.add(enrollment)
    db.commit()
        
    return {
        "enrollment_id": enrollment.enrollment_id,
        "enrollment_date": enrollment.enrollment_date
        }
