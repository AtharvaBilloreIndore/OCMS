from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from OCMSdb import get_db
from OCMSmodels import Enrollment,Enrollment_Create
from datetime import datetime
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
