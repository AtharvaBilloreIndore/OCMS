from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from OCMSdb import get_db
from OCMSmodels import Student, Enrollment, Enrollment_Create
from schemas import Student_Create,Student_Update
router = APIRouter()

@router.get("", summary="List all students")
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@router.post("", summary="Register student")
def create_student(student_data:Student_Create,db: Session = Depends(get_db)):
    with db.begin():
        student = Student( name=student_data.name,
                           education=student_data.education,
                           email=student_data.email)
        db.add(student)
        db.flush() 
    return {
        "student_id": student.student_id,
        "name": student.name }

@router.patch("/{student_id}", summary= "Update Information")
def update_student(student_id:int,student_data:Student_Update,db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    update_data = student_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(student, key, value)
    
    db.commit()
    return student 

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id, Student.is_deleted == False).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student.is_deleted =True
    
    enrollments = db.query(Enrollment).filter(Enrollment.student_id == student_id)
    for enrollment in enrollments:
        enrollment.is_deleted = True
    
    db.commit()
    return {"message": "Student soft-deleted successfully"}