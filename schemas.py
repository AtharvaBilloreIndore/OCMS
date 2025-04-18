from pydantic import BaseModel, Field, EmailStr, StringConstraints
from typing import List, Optional, Annotated
from datetime import datetime
import re
class Course_Create(BaseModel):
    title:str
    description:str
    instructor_ids:List[int] = Field(..., min_items=1)

class Instructor_Create(BaseModel):
    name: Annotated[
        str,
        StringConstraints(min_length=1, strip_whitespace=True),
        re.compile(r"(?=.*[a-zA-Z]).*")
    ]
    email: EmailStr = Field(..., description="Valid email with '@' and '.com'")
    expertise: Annotated[
        str,
        StringConstraints(min_length=1, strip_whitespace=True),
        re.compile(r"(?=.*[a-zA-Z]).*")
    ]

class Student_Create(BaseModel):
    name:Annotated[
        str,
        StringConstraints(min_length=1, strip_whitespace=True),
        re.compile(r"(?=.*[a-zA-Z]).*")
    ]
    education:Annotated[
        str,
        StringConstraints(min_length=1, strip_whitespace=True),
        re.compile(r"(?=.*[a-zA-Z]).*")
    ]
    email:EmailStr = Field(..., description="Valid email with '@' and '.com'")

class Enrollment_Create(BaseModel):
    enrollment_id:int
    enrollment_date:datetime

pattern = re.compile(r"(?=.*[a-zA-Z]).*")

class Instructor_Update(BaseModel):
    expertise: Optional[str] = Field(..., min_length=1)

class Student_Update(BaseModel):
    education: Optional[str] = Field(..., min_length=2)
    email: Optional[EmailStr] = None

class Enrollment_Request(BaseModel):
    student_id: Optional[int] = None
    course_id: Optional[int] = None