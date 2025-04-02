from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from OCMSdb import get_db
import OCMSmodels

import os
from dotenv import load_dotenv
from datetime import datetime
from routers import courses, instructors, students, enrollments

app = FastAPI()

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")


app.include_router(courses.router, prefix="/courses", tags=["Courses"])
app.include_router(instructors.router, prefix="/instructors", tags=["Instructors"])
app.include_router(students.router, prefix="/students", tags=["Students"])
app.include_router(enrollments.router, prefix="/enrollments", tags=["Enrollments"])

@app.get("/")
def read_root():
    return {"message": "FastAPI"}
