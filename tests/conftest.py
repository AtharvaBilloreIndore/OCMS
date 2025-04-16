import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sqlalchemy import create_engine,inspect
from sqlalchemy.orm import sessionmaker
from OCMSdb import get_db
from OCMSmain import app
from OCMSmodels import Instructor, Course, Student, Enrollment, Reference
from OCMSdb import get_db, Base
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_debug.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    print("\n🚀 [TEST SETUP] Creating all tables...")
    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("✅ [TEST SETUP] Tables created successfully!")