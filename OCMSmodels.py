from sqlalchemy import Column, String, ForeignKey,Date, DateTime, func
from sqlalchemy.orm import relationship,Mapped,mapped_column
from OCMSdb import Base,engine
from typing import List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel

def utc_now():
    return datetime.now(timezone.utc)

class Course(Base):
    __tablename__ = "Courses"
    
    course_id: Mapped[int]= mapped_column(primary_key=True, index=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    description = Column(String(150), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    
    created_date = Column(DateTime(timezone=True), default=utc_now)
    last_updated_date = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    
    ems: Mapped["Enrollment"]= relationship("Enrollment",back_populates="crs")
    rfs: Mapped[list["Reference"]]= relationship("Reference", back_populates="crs")

class Instructor(Base):
    __tablename__ = "Instructors"
    
    instructor_id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    expertise = Column(String(150), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    
    created_date = Column(DateTime(timezone=True), default=utc_now)
    last_updated_date = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    rfs: Mapped[list["Reference"]]= relationship("Reference", back_populates="itrs")

class Student(Base):
    __tablename__ = "Students"
    
    student_id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)
    education = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(default=False)

    created_date = Column(DateTime(timezone=True), default=utc_now)
    last_updated_date = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    
    ems: Mapped[List["Enrollment"]] = relationship(back_populates="stds")
    
class  Enrollment(Base):
    __tablename__ = "Enrollments"
    
    enrollment_id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("Students.student_id"), nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("Courses.course_id"), nullable=False)
    enrollment_date= Column(Date, default=datetime.now(timezone.utc))
    is_deleted: Mapped[bool] = mapped_column(default=False)
    
    created_date = Column(DateTime(timezone=True), default=utc_now)
    last_updated_date = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    
    crs: Mapped[List["Course"]]= relationship("Course",back_populates="ems")
    stds: Mapped[List["Student"]] = relationship("Student", back_populates="ems")

class Reference(Base):
    __tablename__ = "References"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("Courses.course_id"), nullable=False)
    instructor_id: Mapped[int] = mapped_column(ForeignKey("Instructors.instructor_id"), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    
    crs: Mapped["Course"]= relationship("Course", back_populates="rfs")
    itrs: Mapped["Instructor"]= relationship("Instructor", back_populates="rfs")

Base.metadata.create_all(bind=engine)

class Course_Create(BaseModel):
    title:str
    description:str
    instructor_ids:List[int]

class Instructor_Create(BaseModel):
    name:str
    email:str
    expertise:str

class Student_Create(BaseModel):
    name:str
    education:str
    email:str

class Enrollment_Create(BaseModel):
    enrollment_id:int
    enrollment_date:datetime

class Instructor_Update(BaseModel):
    expertise: Optional[str] = None

class Student_Update(BaseModel):
    education: Optional[str] = None
    email: Optional[str] = None

class Enrollment_Request(BaseModel):
    student_id: Optional[int] = None
    course_id: Optional[int] = None