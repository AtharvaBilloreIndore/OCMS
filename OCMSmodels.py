from sqlalchemy import Column, String, ForeignKey, Date, Table
from sqlalchemy.orm import relationship
from OCMSdb import Base,engine
from typing import List
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


sce_association = Table("sce",Base.metadata,
        Column ("student_id", ForeignKey("Students.student_id"), primary_key=True),
        Column ("course_id", ForeignKey("Courses.course_id"), primary_key=True),
        Column ("enrollment_id", ForeignKey("Enrollments.enrollment_id"), primary_key=True)
)


class Course(Base):
    __tablename__ = "Courses"
    
    course_id: Mapped[int]= mapped_column(primary_key=True, index=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    description = Column(String(150), nullable=False)
    instructor_id: Mapped[int] = mapped_column(ForeignKey("Instructors.instructor_id"), nullable=False)
    
    itrs: Mapped[List["Instructor"]]= relationship("Instructor", back_populates="crs")
    ems: Mapped["Enrollment"]= relationship("Enrollment", secondary=sce_association, back_populates="crs")
      
class Instructor(Base):
    __tablename__ = "Instructors"
    
    instructor_id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    expertise = Column(String(150), nullable=False)

    crs: Mapped[List["Course"]]= relationship("Course", back_populates="itrs")

class Student(Base):
    __tablename__ = "Students"
    
    student_id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)
    education = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)

    ems: Mapped["Enrollment"] = relationship(secondary=sce_association, back_populates="stds")
    
class  Enrollment(Base):
    __tablename__ = "Enrollments"
    
    enrollment_id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("Students.student_id"), nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("Courses.course_id"), nullable=False)
    enrollment_date= Column(Date)
    
    stds: Mapped[List["Student"]] = relationship("Student",secondary= sce_association, back_populates="ems")
    crs: Mapped[List["Course"]]= relationship("Course",back_populates="ems")
    
Base.metadata.create_all(bind=engine)

