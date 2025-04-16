from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from OCMSdb import get_db
from OCMSmodels import Course,Course_Create,Instructor,Reference,Student,Enrollment

router = APIRouter()

@router.get("", summary="List all courses")
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).filter(Course.is_deleted == False).all()

@router.post("", summary="Create course")
def create_course(course_data: Course_Create, db: Session = Depends(get_db)):
    try:
        with db.begin():
            existing_instructors = db.query(Instructor).filter(
                Instructor.instructor_id.in_(course_data.instructor_ids)).all()
            existing_instructor_ids = {instructor.instructor_id for instructor in existing_instructors}

            missing_instructors = set(course_data.instructor_ids) - existing_instructor_ids
            if missing_instructors:
                raise HTTPException(status_code=400, detail=f"Instructors {missing_instructors} not found")

            
            course = Course(title=course_data.title, description=course_data.description)
            db.add(course)
            db.flush()  

            for instructor_id in existing_instructor_ids:
                reference_entry = Reference(course_id=course.course_id, instructor_id=instructor_id)
                db.add(reference_entry)
        
        return {
            "message": "Course created successfully",
            "course_id": course.course_id,
            "instructor_ids": list(existing_instructor_ids)
        }
    except IntegrityError: 
        raise HTTPException(status_code=500, detail="Database error: Failed to create course or instructor references")

@router.put("/{course_id}")
def update_course(course_id:int, course_data:Course_Create, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.course_id == course_id,Course.is_deleted == False).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    course.title = course_data.title
    course.description = course_data.description
    db.commit()
    db.refresh(course)
    return {
        "message": "Course updated successfully",
        "course": {
            "title": course.title,
            "description": course.description
        }
    }

@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.course_id == course_id, Course.is_deleted == False).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    course.is_deleted =True
    
    enrollments = db.query(Enrollment).filter(Enrollment.course_id == course_id)
    for enrollment in enrollments:
        enrollment.is_deleted = True
    
    references = db.query(Reference).filter(Reference.course_id == course_id)
    for ref in references:
        ref.is_deleted = True
    
    db.commit()
    return {"message": "Course soft-deleted successfully"}