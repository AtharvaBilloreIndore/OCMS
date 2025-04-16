from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from OCMSdb import get_db
from OCMSmodels import Instructor,Instructor_Create,Instructor_Update,Course,Reference

router = APIRouter()

@router.get("", summary="List all instructors")
def get_instructors(db: Session = Depends(get_db)):
    return db.query(Instructor).all()

@router.get("/{course_id}", summary="Fetch instructors")
def fetch_instructor(course_id: int, db: Session = Depends(get_db)):

    course = db.query(Course).filter(Course.course_id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    reference =db.query(Reference).filter(Reference.course_id == course_id).all()
    
    if not reference:
        return {"message": "No instructors assigned to this course", "course_id":course_id}
    
    instructor_ids = [ref.instructor_id for ref in reference]

    return {"course_id":course_id, "instructors":instructor_ids}

@router.post("/register", summary="Register instructor")
def create_instructor(instructor_data:Instructor_Create,db: Session = Depends(get_db)):
    with db.begin():
        instructor = Instructor(name=instructor_data.name,
                                 email=instructor_data.email,
                                 expertise=instructor_data.expertise)
        db.add(instructor)
        db.flush()
        db.refresh(instructor)
    return {
        "instructor_id": instructor.instructor_id,
        "name": instructor.name }

@router.patch("/{instructor_id}", summary="Update instructor")
def update_instructor(instructor_id: int, instructor_data:Instructor_Update,db: Session = Depends(get_db)):
    instructor = db.query(Instructor).filter(Instructor.instructor_id == instructor_id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    
    update_data = instructor_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(instructor, key, value)
    
    db.commit()
    db.refresh(instructor)
    return instructor

@router.delete("/{instructor_id}")
def delete_instructor(instructor_id: int, db: Session = Depends(get_db)):
    instructor = db.query(Instructor).filter(Instructor.instructor_id == instructor_id, Instructor.is_deleted == False).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")

    instructor.is_deleted =True
    
    references = db.query(Reference).filter(Reference.instructor_id == instructor_id)
    for ref in references:
        ref.is_deleted = True
    
    db.commit()
    return {"message": "Instructor soft-deleted successfully"}