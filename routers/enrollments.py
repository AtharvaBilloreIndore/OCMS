from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from OCMSdb import get_db
from OCMSmodels import Enrollment,Student,Course
from datetime import datetime
from schemas import Enrollment_Create,Enrollment_Request
router = APIRouter()

@router.get("/{student_id}",response_model=Enrollment_Create, summary="Enrolled students")
def get_enrollment(student_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(Enrollment).filter_by(student_id=student_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    return {
        "enrollment_id": enrollment.enrollment_id,
        "enrollment_date": enrollment.enrollment_date
    }

@router.post("", summary="Enroll Course")
def enroll_student(enrollment_data: Enrollment_Request, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == enrollment_data.student_id).first()
    course = db.query(Course).filter(Course.course_id == enrollment_data.course_id, Course.is_deleted == False).first()
    try:
        with db.begin():
            if not student:
                raise HTTPException(status_code=404, detail="Student not found")
            if not course:
                raise HTTPException(status_code=404, detail="Course not found")

            existing_enrollment = db.query(Enrollment).filter(
            Enrollment.student_id == enrollment_data.student_id,
            Enrollment.course_id == enrollment_data.course_id).first()
    
            if existing_enrollment:
                raise HTTPException(status_code=409, detail="Enrollment already exists")

            enrollment = Enrollment(
            student_id=enrollment_data.student_id,
            course_id=enrollment_data.course_id
            )
            db.add(enrollment)
            db.commit()
        return {
                "enrollment_id": enrollment.enrollment_id,
                "student_id": enrollment.student_id,
                "course_id": enrollment.course_id,
                "enrollment_date": enrollment.enrollment_date
                }
    except Exception as e:
        return JSONResponse(
        status_code=500,
        content={
                "message":"Unexpected error occured"
            }
    )