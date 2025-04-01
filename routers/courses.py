from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from OCMSdb import get_db
from OCMSmodels import Course,Course_Create,Instructor,Reference

router = APIRouter()

@router.get("", summary="List all courses")
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

@router.post("", summary="Create course")
def create_course(course_data:Course_Create, db: Session = Depends(get_db)):
    
    existing_instructors = db.query(Instructor).filter(Instructor.instructor_id.in_(course_data.instructor_ids)).all()
    existing_instructor_ids = {instructor.instructor_id for instructor in existing_instructors}

    missing_instructors = set(course_data.instructor_ids) - existing_instructor_ids
    if missing_instructors:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Instructors {missing_instructors} not found")
    
    course = Course(title=course_data.title,
                                 description=course_data.description
                                )
    
    db.add(course)
    db.commit()
    db.refresh(course)
    
    try:
        for instructor_id in existing_instructor_ids:
            reference_entry = Reference(course_id=course.course_id, instructor_id=instructor_id)
            db.add(reference_entry)

        db.commit()
    except IntegrityError:
            db.rollback() 
            raise HTTPException(status_code=500, detail="Database error: Failed to create instructor-course references")

    return {
        "message": "Course created successfully",
        "course_id": course.course_id,
        "instructor_ids": list(existing_instructor_ids)
}